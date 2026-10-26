# NJUPT-lab-report

南京邮电大学《电工电子实验技术》预习报告 / 实验报告助手，是一个通用的 Agent Skill（`SKILL.md` 格式，支持 skills 的编程 agent 都能用）：读课本扫描页、做理论计算和预期波形、用 [multisim-cli](https://github.com/1naruto-1/multisim-cli) 搭电路并截取真实的 Multisim 仪器面板、插入手绘电路图和波形照片，按学校官方模板生成 docx 和 pdf。

## 原则

这是交给老师评分的作业，skill 里写死了几条规则：

- 仿真截图只来自 Multisim 的真实截取，截不到就请你手动截，不用代码画假面板。
- 电路图、实测波形只用你手绘拍照的照片，缺了就留占位并提醒。
- 测量数据、实验现象、故障经历只来自你提供的记录，不编造。
- 理论值用 Python 计算。

它帮你整理和排版，实验得自己做、数据得自己测。

## 环境

- Windows（导出 pdf 用 Word；没有 Word 时用 LibreOffice 的 `soffice`）
- Python 3.10+：`pip install python-docx lxml Pillow PyMuPDF pywin32 matplotlib`
- [pandoc](https://pandoc.org/)（公式转成 Word 原生公式）
- 需要仿真时：NI Multisim 14 + [multisim-cli](https://github.com/1naruto-1/multisim-cli)

## 安装

```powershell
git clone https://github.com/1naruto-1/NJUPT-lab-report "$env:USERPROFILE\.agents\skills\ee-lab-report"
cd "$env:USERPROFILE\.agents\skills\ee-lab-report"
copy config.example.json config.json   # 填写班级、学号、姓名、指导教师等，用于封面和文件命名
```

默认放在 `~/.agents/skills/`。如果你用的 agent 只读自己的 skills 目录，建一个目录联接过去即可，例如 Claude Code：

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\ee-lab-report" -Target "$env:USERPROFILE\.agents\skills\ee-lab-report"
```

之后对 agent 直接说“帮我写实验四的预习报告，课本扫描件是……”即可，流程见 `SKILL.md`。

## 目录

```
SKILL.md                  skill 主说明（工作流程与原则）
config.example.json       学生信息模板（复制为 config.json，不入库）
assets/report_template.docx  学校发布的电子报告官方格式（已清空个人信息）
references/               课程安排、预习报告/实验报告结构、Multisim 用法
scripts/build_report.py   Markdown → 官方模板 docx/pdf
scripts/pdf_pages.py      课本扫描 PDF 渲染、旋转、拆跨页
scripts/prep_image.py     手绘照片摆正、裁剪、提亮
```

`references/course.md` 里的授课计划和页码对应 2026-2027 学年第 1 学期、常春耘等《电工电子实验技术（上册）（第二版）》，其他学期或班级请按自己的计划表修改。

## 许可

代码和文档为 MIT，见 `LICENSE`。`assets/report_template.docx` 是南京邮电大学电工电子教学实验中心发布的报告格式，校徽等版权归学校所有，仅为方便同学使用而附带，不在 MIT 授权范围内。
