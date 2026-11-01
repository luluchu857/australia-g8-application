# 安装澳洲八大申请

支持 Codex、WorkBuddy 及其他兼容 Skill 的应用。查询 MCP 和申请助手与留学规划助手共用。

## 连接

| 服务 | 地址 | 授权 |
| --- | --- | --- |
| 留学信息查询 | `https://hi.xwoork.cn/info/mcp` | 可匿名查询 |
| 留学申请助手 | `https://hi.xwoork.cn/assist/mcp` | 学生工具无需 Key |

已有这两条连接就复用，不要重复建同名服务。两条都不需要填 Key；旧服务若仍要求 Key，记为“申请助手待开放”，不向学生索要。

示例见 `mcp.example.json`。

## 检查

1. 宿主能发现本 Skill：`australia-g8-application`。
2. 能调用查询工具，例如按澳大利亚搜索专业。
3. 申请助手无 Key 能发现工具，或标明待开放；查询成功不能代替。
4. 能打开 `https://hi.xwoork.cn/student`；上传页 `https://hi.xwoork.cn/student/upload` 以当时页面是否上线为准，未上线要如实说。
