import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";
import "./globals.css";
import "./i18n";

// 在安全上下文（HTTPS 或 localhost）中才定义 `crypto.randomUUID`。
// 通过纯 HTTP 的 LAN 访问会使其未定义，这会导致生成客户端消息 ID 的组件崩溃。
// 添加一个 v4 风格的回退实现，确保在安全和非安全上下文中调用站点保持一致。
if (typeof globalThis.crypto !== "undefined" && !("randomUUID" in globalThis.crypto)) {
  Object.defineProperty(globalThis.crypto, "randomUUID", {
    value: () =>
      "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      }),
    configurable: true,
  });
}

// React 18+ 使用 createRoot 而非 render，以启用并发特性
const root = document.getElementById("root");
if (!root) throw new Error("root element missing");

ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
