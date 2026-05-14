import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

// 合并 Tailwind 类名的工具函数
// twMerge 确保后面的类覆盖前面的冲突类（例如 "px-2 px-4"）
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
