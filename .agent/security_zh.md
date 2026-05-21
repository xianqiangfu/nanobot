# 安全边界

代理具有强大的功能（文件系统、shell、网络访问）。修改相关代码时，不得绕过以下安全防护措施。

## 工作区限制

文件系统工具（`read_file`、`write_file`、`edit_file`、`list_dir`）通过 `_resolve_path`（`agent/tools/filesystem.py`）解析路径，该函数强制要求解析后的路径必须位于 `allowed_dir`（通常是配置的工作区）之下，以及媒体上传目录（`get_media_dir()`）和任何 `extra_allowed_dirs` 中。

Shell 执行（`ExecTool`、`agent/tools/shell.py`）也遵守 `restrict_to_workspace`：如果启用且 `working_dir` 在工作区之外，命令将在执行前被拒绝。

**规则**：任何新的路径处理逻辑都必须通过 `_resolve_path` 或执行等效的 `allowed_dir` 检查。

## SSRF 保护

从代理工具发出的所有出站 HTTP 请求都必须通过 `validate_url_target`（`security/network.py`）。默认情况下，它会阻止 RFC1918 私有地址、链路本地范围和云元数据端点（包括 `169.254.169.254`）。

唯一的例外是 `configure_ssrf_whitelist(cidrs)`，它会在加载时从 `config.tools.ssrf_whitelist` 读取白名单。

**规则**：不要在工具中添加直接的 `httpx.get` / `requests.get` 调用。通过现有的 web 获取工具或复制 `validate_url_target` 检查来路由请求。

## Shell 沙箱

`tools/sandbox.py` 提供可选的命令包装功能。目前唯一提供的后端是 `bwrap`（bubblewrap），专为容器化部署设计。在 Windows 和没有 `bwrap` 的裸机 Linux 上，命令在原生 shell 中运行，工作区限制是唯一的防护措施。

**规则**：如果添加新的沙箱后端，请实现 `_wrap_<name>(command, workspace, cwd) -> str` 并在 `_BACKENDS` 中注册。