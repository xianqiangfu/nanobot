import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { Composer } from "@/components/Composer";
import { MessageList } from "@/components/MessageList";
import { useClient } from "@/providers/ClientProvider";
import { useNanobotStream } from "@/hooks/useNanobotStream";
import { useSessionHistory } from "@/hooks/useSessions";
import type { ChatSummary } from "@/lib/types";

interface ChatPaneProps {
  session: ChatSummary | null;
  /** 配置新聊天并将其标记为活动。返回新的 chat_id 或 null。 */
  onNewChat: () => Promise<string | null>;
}

/**
 * 聊天界面：顶部是持久化历史记录，底部是实时流和固定在底部的编辑器。
 * 当没有活动会话时，我们渲染一个居中的欢迎卡片，带有完全功能的编辑器
 * — 输入第一条消息会安静地配置新聊天并将消息路由到其中。
 */
export function ChatPane({ session, onNewChat }: ChatPaneProps) {
  const chatId = session?.chatId ?? null;
  const historyKey = session?.key ?? null;
  const { messages: historical, loading, hasPendingToolCalls } = useSessionHistory(historyKey);
  const { client } = useClient();
  const [booting, setBooting] = useState(false);
  const pendingFirstRef = useRef<string | null>(null);

  const initial = useMemo(() => historical, [historical]);
  const { messages, isStreaming, send, setMessages } = useNanobotStream(
    chatId,
    initial,
    hasPendingToolCalls,
  );

  useEffect(() => {
    if (!loading && chatId) setMessages(historical);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loading, chatId, historical]);

  // 一旦会话变为活动状态，刷新欢迎编辑器中暂存的任何第一条消息，
  // 以便用户的按键"直接发送"。
  useEffect(() => {
    if (!chatId) return;
    const pending = pendingFirstRef.current;
    if (!pending) return;
    pendingFirstRef.current = null;
    client.sendMessage(chatId, pending);
    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: "user",
        content: pending,
        createdAt: Date.now(),
      },
    ]);
    setBooting(false);
  }, [chatId, client, setMessages]);

  const handleWelcomeSend = useCallback(
    async (content: string) => {
      if (booting) return;
      setBooting(true);
      pendingFirstRef.current = content;
      const newId = await onNewChat();
      if (!newId) {
        // Creation failed — release the lock so the user can retry.
        pendingFirstRef.current = null;
        setBooting(false);
      }
    },
    [booting, onNewChat],
  );

  if (!session) {
    return (
      <section className="flex min-h-0 flex-1 flex-col">
        <div className="flex flex-1 flex-col items-center justify-center gap-8 px-4 pb-6">
          <div className="flex flex-col items-center gap-4 animate-in fade-in-0 slide-in-from-bottom-2 duration-500">
            <h1 className="text-xl font-medium tracking-tight text-foreground/90">
              What can I do for you?
            </h1>
            <p className="max-w-md text-center text-sm text-muted-foreground">
              Your conversations are persisted locally under the nanobot
              workspace. Start typing and I'll open a new chat.
            </p>
          </div>
          <div className="w-full animate-in fade-in-0 slide-in-from-bottom-2 duration-500">
            <Composer
              compact
              disabled={booting}
              onSend={handleWelcomeSend}
              placeholder={
                booting ? "Opening a new chat…" : "Ask anything..."
              }
            />
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="relative flex min-h-0 flex-1 flex-col">
      <MessageList messages={messages} isStreaming={isStreaming} />
      <Composer
        onSend={send}
        disabled={!chatId}
        placeholder="Type your message…"
      />
    </section>
  );
}
