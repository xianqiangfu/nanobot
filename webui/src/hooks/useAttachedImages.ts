import { useCallback, useEffect, useRef, useState } from "react";

import { encodeImage, type EncodeFailure } from "@/lib/imageEncode";

/** 一个附件的生命周期阶段：
 *
 * - ``encoding``  — posted to the Worker; chip shows a spinner
 * - ``ready``     — ``dataUrl`` available; safe to submit
 * - ``error``     — validation / decode failure; chip shows inline error
 */
export type AttachmentStatus = "encoding" | "ready" | "error";

export interface AttachedImage {
  id: string;
  file: File;
  /** Optimistic ``blob:`` preview URL; revoked on ``remove`` / ``clear`` /
   * unmount. */
  previewUrl: string;
  status: AttachmentStatus;
  /** Populated when ``status === "ready"``. */
  dataUrl?: string;
  /** Size of the final encoded payload (base64 bytes decoded). */
  encodedBytes?: number;
  /** Whether the Worker re-encoded the image to hit the size budget. */
  normalized?: boolean;
  /** Human-readable validation / encoding error when ``status === "error"``. */
  error?: AttachmentError;
}

/** 机器可读的拒绝原因，显示为内联芯片错误。
 *
 * Callers localize these via the ``composer.imageRejected.*`` i18n table. */
export type AttachmentError =
  | "unsupported_type"   // server whitelist excludes this MIME
  | "too_many_images"    // per-message cap (4) reached before enqueue
  | "magic_mismatch"     // extension lies about the real content
  | "decode_failed"      // Worker couldn't decode / re-encode
  | "too_large"          // even after normalization we exceed the budget
  | "io";                // file read failed at the browser layer

export const MAX_IMAGES_PER_MESSAGE = 4;

/** MIME whitelist — mirrors the server's and the ``<input accept>`` attr. */
const ACCEPTED_MIMES: ReadonlySet<string> = new Set([
  "image/png",
  "image/jpeg",
  "image/webp",
  "image/gif",
]);

function uuid(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return (crypto as Crypto).randomUUID();
  }
  return `img-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

function mapEncodeFailure(reason: EncodeFailure["reason"]): AttachmentError {
  switch (reason) {
    case "invalid_mime":
    case "magic_mismatch":
      return "magic_mismatch";
    case "too_large_after_normalize":
      return "too_large";
    case "io":
      return "io";
    case "decode_failed":
    default:
      return "decode_failed";
  }
}

export interface UseAttachedImagesApi {
  images: AttachedImage[];
  /** 入队新文件。返回被拒绝的文件列表，以便调用者显示内联错误。
   * 客户端拒绝的文件（错误的 MIME、限制）*不会*添加到 ``images`` 中
   * — 只有可恢复的编码错误才会显示为错误芯片。 */
  enqueue: (files: Iterable<File>) => {
    rejected: Array<{ file: File; reason: AttachmentError }>;
  };
  remove: (id: string) => { nextFocusId: string | null };
  /** 撤销所有暂存的 blob URL 并删除所有附件。在成功提交后调用
   * — 乐观气泡保持独立的 ``data:`` URL，因此在这里删除 blob
   * 预览是安全的。 */
  clear: () => void;
  /** 当至少有一张图片仍在编码时为 ``true`` — Send 应该等待。 */
  encoding: boolean;
  /** 当我们达到 ``MAX_IMAGES_PER_MESSAGE`` 时为 ``true``。 */
  full: boolean;
}

/** 管理附加到编辑器的图片的生命周期。
 *
 * Responsibilities in one place:
 *   - validation (MIME whitelist, count cap)
 *   - blob URL creation + revocation
 *   - Worker orchestration
 *   - focus bookkeeping so keyboard delete doesn't strand the user
 */
export function useAttachedImages(): UseAttachedImagesApi {
  const [images, setImages] = useState<AttachedImage[]>([]);
  // Ref mirror so ``enqueue`` can see the authoritative length when invoked
  // multiple times in a single tick (rapid file selection, drag of many
  // files, paste storms). ``state`` is stale for that second + call.
  const imagesRef = useRef<AttachedImage[]>([]);
  imagesRef.current = images;

  const setEntry = useCallback((id: string, patch: Partial<AttachedImage>) => {
    setImages((prev) => {
      const next = prev.map((img) => (img.id === id ? { ...img, ...patch } : img));
      imagesRef.current = next;
      return next;
    });
  }, []);

  const enqueue = useCallback(
    (files: Iterable<File>) => {
      const rejected: Array<{ file: File; reason: AttachmentError }> = [];
      const toAdd: AttachedImage[] = [];
      let slot = MAX_IMAGES_PER_MESSAGE - imagesRef.current.length;

      for (const file of files) {
        if (!ACCEPTED_MIMES.has(file.type)) {
          rejected.push({ file, reason: "unsupported_type" });
          continue;
        }
        if (slot <= 0) {
          rejected.push({ file, reason: "too_many_images" });
          continue;
        }
        slot -= 1;
        toAdd.push({
          id: uuid(),
          file,
          previewUrl: URL.createObjectURL(file),
          status: "encoding",
        });
      }

      if (toAdd.length > 0) {
        const next = [...imagesRef.current, ...toAdd];
        imagesRef.current = next;
        setImages(next);
        // Fire the Worker after the commit so chips render first (good INP).
        for (const entry of toAdd) {
          queueMicrotask(() => {
            encodeImage(entry.file).then(
              (result) => {
                if (result.ok) {
                  setEntry(entry.id, {
                    status: "ready",
                    dataUrl: result.dataUrl,
                    encodedBytes: result.bytes,
                    normalized: result.normalized,
                  });
                } else {
                  setEntry(entry.id, {
                    status: "error",
                    error: mapEncodeFailure(result.reason),
                  });
                }
              },
              () => {
                setEntry(entry.id, {
                  status: "error",
                  error: "decode_failed",
                });
              },
            );
          });
        }
      }
      return { rejected };
    },
    [setEntry],
  );

  const remove = useCallback((id: string) => {
    let nextFocusId: string | null = null;
    setImages((prev) => {
      const idx = prev.findIndex((img) => img.id === id);
      if (idx === -1) return prev;
      const target = prev[idx];
      try {
        URL.revokeObjectURL(target.previewUrl);
      } catch {
        // No-op: previewUrl revocation is best-effort.
      }
      const next = [...prev.slice(0, idx), ...prev.slice(idx + 1)];
      imagesRef.current = next;
      // Prefer moving focus to the chip at the same index, else previous.
      const candidate = next[idx] ?? next[idx - 1];
      nextFocusId = candidate?.id ?? null;
      return next;
    });
    return { nextFocusId };
  }, []);

  const clear = useCallback(() => {
    setImages((prev) => {
      for (const img of prev) {
        try {
          URL.revokeObjectURL(img.previewUrl);
        } catch {
          // revoke is best-effort
        }
      }
      imagesRef.current = [];
      return [];
    });
  }, []);

  // Final safety net: revoke any outstanding blob URLs on unmount. Safe
  // under StrictMode double-invoke because revoked blob URLs are only
  // referenced from in-hook chip state, which is rebuilt on remount.
  useEffect(() => {
    return () => {
      for (const img of imagesRef.current) {
        try {
          URL.revokeObjectURL(img.previewUrl);
        } catch {
          // best-effort cleanup on unmount
        }
      }
    };
  }, []);

  const encoding = images.some((img) => img.status === "encoding");
  const full = images.length >= MAX_IMAGES_PER_MESSAGE;

  return { images, enqueue, remove, clear, encoding, full };
}
