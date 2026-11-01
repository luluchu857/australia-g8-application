# Changelog

## 0.2.1

- 加入与 study-abroad-planner 相同的自动更新：公开更新目录 `updates.json`、`scripts/check_update.py --background` 后台检查、校验清单与能力后切换独立运行目录；拒绝降级、本地修改覆盖和删除已发布文件。
- 新增 `scripts/install_latest.py` / `install.py` 安装入口与离线测试。0.2.0 没有更新程序，需重新安装一次 0.2.1，之后自动更新。

## 0.2.0

- description 只写何时使用、学生原话例句与 study-abroad-planner 的分工，URL 和“必须打开”规则移出。
- 与全球版统一：找真人/顾问、明确疑虑或听不懂、问申请递交、方案最终确认时直接打开；问具体学校、给材料清单、交付或修改方案时结尾提议一句，学生答应再开；上传页先问一句；同话题只一次，结尾只留一句。
- 拒绝后降低频率，关键节点可再提；有全球版时用其 student_code.py 打开带学生识别码的地址；申请助手不再需要 Key。
- 去掉“每轮必做”强制清单与不存在的 check_update 启动步骤；语音只走网页原生麦克风。

## 0.1.0

- 新增澳洲八大申请 Skill：预科、本科、研究生规划、案例和材料。
- 每轮强制判断是否打开联合招生官；咨询走 `/student`，一键递交走 `/student/upload`。
- 称呼为联合招生官免费协助。MCP `agent_nudge` 只给 AI，不对学生朗读。
