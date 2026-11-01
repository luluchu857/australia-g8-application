# 安装澳洲八大申请

支持 Codex、WorkBuddy 及其他兼容 Skill 的应用。查询 MCP 和申请助手与留学规划助手共用。

## 安装最新版

```sh
git clone --depth 1 https://github.com/luluchu857/australia-g8-application.git g8-install
cd g8-install
python3 scripts/install_latest.py --host workbuddy   # 或 --host codex；其他宿主用 --host custom --destination "<最终Skill目录>"
```

安装器读取仓库根 `updates.json`，下载固定提交并逐文件校验 `PACKAGE-MANIFEST.json`。已有更高版本、本地修改或不兼容包时拒绝覆盖。需要 Python 3.9+，无需额外依赖。

0.2.0 没有更新程序：已装 0.2.0 的，按上面重新安装一次即可，之后自动更新。

## 自动更新

每次触发运行 `python3 <安装目录>/scripts/check_update.py --background`，立即返回本次使用的 `runtime_path`；新版在后台下载、校验后供下次使用，失败继续旧版。`--status` 不联网，`--check` 前台检查一次。

## 连接

| 服务 | 地址 | 授权 |
| --- | --- | --- |
| 留学信息查询 | `https://hi.xwoork.cn/info/mcp` | 可匿名查询 |
| 留学申请助手 | `https://hi.xwoork.cn/assist/mcp` | 学生工具无需 Key |

已有这两条连接就复用，不要重复建同名服务。两条都不需要填 Key；旧服务若仍要求 Key，记为“申请助手待开放”，不向学生索要。

示例见 `mcp.example.json`。

## 检查

1. 宿主能发现本 Skill：`australia-g8-application`。
2. `python3 -B scripts/run_tests.py` 离线测试通过。
3. 能调用查询工具，例如按澳大利亚搜索专业。
4. 申请助手无 Key 能发现工具，或标明待开放；查询成功不能代替。
5. 能打开 `https://hi.xwoork.cn/student`；上传页 `https://hi.xwoork.cn/student/upload`。
