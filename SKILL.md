---
name: paper-craft
description: "Rules for writing and revising research papers in English and Chinese. Core: packaging (包装: present the authors' real contributions in the method fully, each with the cited prior work it builds on, what was changed, why, and what it brings; routine or borrowed parts are cited and stated briefly, never presented as new) and distilling innovation points (创新点凝练: a six-slot sentence of problem, name, what is modelled as which distribution, its parameters, derivation under constraints, property under conditions). Also covers abstracts (long version first, English first, formal Chinese version), introductions and conclusions, scientific rather than engineering style, formal written Chinese, terms and numbers, handling an author's or advisor's marks, and literature search for positioning, with four small checking scripts. Use when writing or revising a paper's abstract, introduction, innovation paragraphs, contribution list or Chinese version, or when asked for paper-craft, 包装, 凝练创新点, 处理批注."
license: MIT
metadata:
  version: "1.0.0"
  last_updated: "2026-11-25"
---

# paper-craft：论文打磨（包装与创新点凝练）

本 skill 是一套写和改学术论文（中英文）的规矩。核心两件事：**写作就是包装**，把真实属于作者的工作写足、写清；**创新点要凝练**，把做过的工作归纳成几个说得清的创新点。包装不是夸大：借来的结果不称新，“优于”只在做过比较时写，“首次”先检索（第二节第 1 条）。规矩分三级：**必守**、**建议**、**自问**（见 `references/01_包装.md` 开头）。还没有定下的写法不写成规矩，记在 profile 的“待定事项”里。

文中“作者”指论文的作者，“导师”指给作者提修改意见的导师或合作者；规矩和例句里的“我们”指论文的作者。本 skill 协助作者修改稿件，稿件的内容和定稿由作者负责。“profile”指每篇论文一份的设定文件 `profiles/<论文>.md`（见第八节）。

## 一、什么时候用，什么时候不用

用：写或改论文的摘要、引言、方法中的创新点、贡献列表、结论、中文对照稿；处理作者或导师的批注；为某个创新点检索并核对已有工作。

| 情形 | 改用 |
|---|---|
| 与论文无关的通用写作 | 通用写作类 skill |
| 模拟严格审稿、找论文的弱点 | 审稿类 skill |
| 核查参考文献是否真实 | 文献核查工具 |
| 画数据图、论文配图 | 作图类 skill |
| 日常对话 | 不用本 skill |

## 二、优先次序

1. **事实与学术诚信**：数字、单位、命题的前提、期刊的硬性上限；借来的结果不称新，“优于”须有比较，性质带着前提，“首次”须先检索。凡涉及出处、引用原文、新颖性和所报事实的规矩都属于这一类，例如 PACK-13 至 PACK-16、INNOV-08、ABS-07、ABS-10、ABS-11、ABS-14、LIT-01 至 LIT-06、LIT-09、NUM-01 至 NUM-05、SCI-04、SCI-08、SCI-09。任何改写、任何要求都不得违背；有冲突时当场说明。
2. **作者和导师最近一次的明确要求**。与先前的要求或样稿冲突时，当场指出，按后来的做，记下来（CMT-05）。
3. **本 skill 的其他规矩**（必守高于建议）。
4. 通用写作建议。

## 三、按工作类型，动笔前必读

| 工作 | 必读 | 用到的程序 |
|---|---|---|
| 凝练创新点、写贡献列表 | 02 创新点凝练、01 包装、profile | — |
| 写或改方法中的创新点段落 | 01 包装、02 创新点凝练、05 科学化写法 | register_scan（中文稿） |
| 摘要 | 03 摘要、02、01、06 中文书面语、profile | count_words、register_scan、number_parity |
| 引言、相关工作、题目、结论 | 04 引言与结论、02、01 | — |
| 中文稿 | 06 中文书面语、07 术语与数字、profile | register_scan、number_parity |
| 处理批注 | 09 批注处理、10 常见错误、profile | extract_marks，以及上面各项 |
| 为创新点检索文献 | 08 文献检索、02 的 INNOV-07 | — |

读不到必读文件时，先说明哪一份没读到，再动笔。切换工作类型，或对话被压缩之后，重读该类工作的必读文件。

## 四、最重要的十五条（括号里是编号；细节见各文件）

1. **把真实的工作写足**：方法中属于我们的部分（推导、证明、为本任务做的改造、新定义的对象）要展开写足；确属常规或借用的部分注明出处，一句带过（PACK-01、PACK-02）。
2. **“在 X 的基础上，我们做了如下改进”**：X 给出引用；与 X 的区别织进描述，不单独成段（PACK-04、PACK-05）。
3. **先说为什么这样建模，好处写在引入处**；只写由构造或命题推出的好处（PACK-07）。
4. **引理、命题以我们推导的结论开头**，已有结果作为特例并注明出处（PACK-08）。
5. **每个新对象都有名字和含义**，按作用起名（PACK-09、INNOV-05）。
6. **创新点的六位句式**：针对……问题，提出……；将……建模为……分布，以……作为参数，在……约束下推导得到……，在……条件下达到……（INNOV-01）。
7. **不把功能或结论当创新点，不只给名字，要落到技术细节**（INNOV-03、INNOV-04）。
8. **全文一条主线**；挑战、缺陷、组件一一对应；各创新点的句式不雷同（INNOV-10、INNOV-11、INNOV-13）。
9. **守住事实**：“优于”须有比较；性质带着命题的前提；近似所得的结论不写成精确结果；借来的结果不称新；写“首次”之前先检索并留记录（PACK-13 至 PACK-16）。
10. **摘要先写长版再压短版，英文先写**；字数用程序数（ABS-01、ABS-12）。
11. **中文用书面语，以作者认可的文字为准**：不写括号注释，不写口语和工程腔，不写绝对化的要求，每一步推理写出理由，不用“它”（CN-01 至 CN-03、CN-06 至 CN-08）。
12. **口气肯定、与证据相称，不写防御性句子**；限定随它所限定的主张出现，同一处不重复（SCI-07、SCI-08）。
13. **每条批注当一类问题处理**，所有稿子、中英两种文字一起扫（CMT-02）。
14. **作者亲笔的文字不动**；有意见先说，作者同意再改（CMT-04）。
15. **事先约定哪些事要先问作者**，其余自己定、记下来（CMT-07）。

## 五、包装与凝练的做法（详见 01、02）

动笔前完成：
1. 写下主线：一个科学问题。
2. 列挑战—缺陷—组件对应表。
3. 每个组件填一行：已有方法 X（读过原文）→ 在我们的数据上怎么失败 → 我们的改动 → 去掉改动的消融。
4. 每个组件按六位句式写出要点；列出其中真正属于我们的部分，其余注明出处。
5. 起名；检查各创新点的句式是否有变化。
6. 先写长版，再压成摘要和贡献列表。

## 六、检查

程序在 `scripts/`，只用 Python 3 标准库，用 `python3 -I` 运行。每个检查程序的报告都有一行状态：CHECKED（读完了）、PARTIAL（有一部分没读到，列出来）或 NOT CHECKED（没读成，或参数不对）；后两种的退出码是 2。`tests/run_tests.py` 报告“tests: N failed”，全部通过时退出码为 0；`tests/check_hygiene.py` 检查仓库里有没有个人路径、邮箱、访问令牌和论文的 profile。**没跑成的检查不能说“通过”**；给作者的报告照抄状态行和要点。

| 程序 | 查什么 | 什么时候跑 | 查不了什么 |
|---|---|---|---|
| `count_words.py 文件 --limit <上限>` | 英文词数、汉字数；上限取自 profile | 每次改摘要后 | 期刊系统的计数差异 |
| `register_scan.py 文件 --profile profiles/<论文>.md` | 括号注释、“它”、“这一”、口语与工程腔清单、绝对化的说法、单独的“转化为”、不带括号的“即……”从句（候选）、本篇的禁用词与限用词 | 每次改中文稿后、交付前 | 意思对不对、理由好不好、啰嗦不啰嗦 |
| `number_parity.py 英文 中文` | 两份文字里的数字是否一一对应 | 中英文改完后、两轮之间 | 数字本身对不对 |
| `extract_marks.py 批注稿.docx` | Word 正文、文本框、脚注、尾注、页眉页脚里标了颜色、高亮和删除线的文字，修订（插入、删除），以及批注栏里的评论文字 | 每轮批注开始时 | 评论对应的是正文哪一段（只列评论本身） |
| `tests/run_tests.py` | 上面四个程序本身 | 改了程序之后 | — |

请子代理复核时：只读、不联网、不写文件；交给子代理的是本次要查的规矩编号和文字，不是整段对话；中文稿以作者认可的文字（profile 里的文风样本）和批注原话为标准。子代理报回来的每一条，自己核对后再用。

## 七、常见错误

动笔前读 `references/10_常见错误.md` 的前十条。其中三条尤其要注意：只改被批的那一句（ERR-01）；绝对量与相对变化没分清（ERR-02）；压缩时丢掉前提（ERR-04）。

## 八、每篇论文的设定

每篇论文一份 profile，照 `profiles/_template.md` 建：用词表（含程序读取的禁用词和限用词）、已定的名字、作者亲笔的保护文字、保护限定语、关键数字、待定事项、文风样本。待定事项不当作规矩执行。`profiles/示例_电池寿命.md` 是一份虚构的填写示例。

profile 里通常有未发表的内容，不要提交到公开的仓库。本仓库的 `.gitignore` 默认不提交模板和示例以外的 profile。

## 九、更新规矩

每轮修改后：新规矩补进对应文件（编号、级别）；被推翻的规矩不删，标“已作废”，写明原因和取代的条目；在 `CHANGELOG.md` 记一条。可为每条规矩记下来源，以便日后判断这条规矩有多硬。

## 十、文件

- `references/01_包装.md`　`02_创新点凝练.md`（核心）
- `references/03_摘要.md`　`04_引言与结论.md`　`05_科学化写法.md`　`06_中文书面语.md`　`07_术语与数字.md`　`08_文献检索.md`　`09_批注处理.md`　`10_常见错误.md`
- `profiles/_template.md`　`profiles/示例_电池寿命.md`　`examples/改前改后.md`
- `scripts/`　`tests/`　`CHANGELOG.md`
