# Web Workers

本目录包含 WebUI 的 Web Workers。

## Worker 说明

### imageEncode.worker.ts

图片编码 Worker，负责：
- 将图片文件转换为 base64 格式
- 生成图片预览 URL
- 处理大图片的编码

## 为什么使用 Web Workers

- **避免阻塞 UI** - 编码大图片可能需要较长时间
- **保持响应性** - 主线程保持响应，不阻塞用户操作
- **并行处理** - 多个编码任务可以并行执行

## 使用示例

```ts
import ImageEncodeWorker from './workers/imageEncode.worker.ts?worker';

const worker = new ImageEncodeWorker();

worker.postMessage({ file: imageFile });

worker.onmessage = (event) => {
  const { base64, previewUrl } = event.data;
  // 处理编码结果
};

worker.onerror = (error) => {
  // 处理错误
};
```

## Worker 通信

### 主线程 → Worker

发送需要编码的文件：

```ts
worker.postMessage({ file: File });
```

### Worker → 主线程

返回编码结果：

```ts
{
  base64: string;      // base64 编码的图片数据
  previewUrl: string;   // 预览 URL
}
```

## 注意事项

- Worker 不能直接访问 DOM
- Worker 不能访问 React Context
- Worker 和主线程之间只能通过消息传递通信
- 使用完毕后应终止 Worker 释放资源
