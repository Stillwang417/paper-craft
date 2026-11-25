# paper-craft

一套写和改学术论文（中英文）的规矩，做成 Claude Code 的 skill（Agent Skills 格式）。核心两件事：

- **包装**：把方法中真实属于作者的工作写足、写清：建立在哪项已有工作之上（给出引用），改了什么，为什么改，带来什么。常规或借用的部分注明出处，一句带过，不写成新的。
- **创新点凝练**：把做过的工作归纳成几个创新点，每一点说清针对什么问题、提出了什么、怎么构建的、在什么条件下得到什么。

另外还有：摘要（先写长版再压短版，英文先写，中文用书面语）、引言与结论的结构、科学化而非工程化的写法、中文书面语、术语与数字、处理作者和导师的批注、为定位创新点检索文献，以及四个检查小程序。规矩用中文写成。

> 包装不是夸大。本 skill 的优先次序里，事实与学术诚信排在第一位，高于任何改写要求：借来的结果不称新；“优于”只在做过比较时写；性质带着命题的前提；写“首次”之前先检索并留记录（见 `SKILL.md` 第二节、`references/01_包装.md` 第三节）。本 skill 协助作者修改稿件，稿件的内容和定稿由作者负责。

## 安装

skill 就是一个文件夹，不含钩子，也不改任何设置。

个人使用（所有项目都可用）：

```bash
git clone https://github.com/Stillwang417/paper-craft.git ~/.claude/skills/paper-craft
```

只在某个项目里用：把仓库放到该项目的 `.claude/skills/paper-craft/`。

如果已经有同名的 skill，换一个文件夹名，并把 `SKILL.md` 开头的 `name` 一并改掉。

## 用法

在 Claude Code 里直接说要做的事，例如：

- “按 paper-craft 改这段摘要，先写长版”
- “处理这份批注稿”（附上 Word 文件）
- “帮我凝练方法的创新点”

Claude 会按 `SKILL.md` 第三节，先读该类工作的必读文件再动笔。

## 为每篇论文建一份 profile

复制 `profiles/_template.md`，改名为 `profiles/<论文简称>.md`，填入用词表、已定的名字、作者亲笔的保护文字、保护限定语、关键数字、待定事项和文风样本。`profiles/示例_电池寿命.md` 是一份虚构的填写示例。

profile 里通常有未发表的内容。本仓库的 `.gitignore` 默认不提交模板和示例以外的 profile；如果你 fork 了本仓库并公开，请保留这条规则。

## 检查程序

只用 Python 3 标准库，不需要安装别的包。在 skill 文件夹里运行，稿件写完整路径，例如：

```bash
cd ~/.claude/skills/paper-craft
python3 -I scripts/count_words.py /path/to/abstract_en.txt --limit 250
```

| 程序 | 作用 |
|---|---|
| `scripts/count_words.py 文件 --limit <上限>` | 英文词数、汉字数，并与上限比较（上限以 profile 为准） |
| `scripts/register_scan.py 文件 --profile profiles/<论文>.md` | 扫中文稿里的括号注释、“它”、口语、工程腔、绝对化的说法、本篇的禁用词与限用词（只给候选，要人读过再定） |
| `scripts/number_parity.py 英文文件 中文文件` | 两份文字里的数字是否一一对应 |
| `scripts/extract_marks.py 批注稿.docx` | 取出 Word 批注稿里标了颜色、高亮和删除线的文字（正文、文本框、脚注、尾注、页眉页脚），以及修订和批注栏里的评论 |

每个程序的报告都有一行状态：CHECKED、PARTIAL 或 NOT CHECKED；后两种的退出码是 2。

## 目录

```
SKILL.md        入口：什么时候用、优先次序、必读文件、最重要的十五条
references/     十份规矩（01 包装、02 创新点凝练是核心）
profiles/       每篇论文一份设定：模板与虚构示例
examples/       改前改后的虚构例子
scripts/        四个检查程序
tests/          程序的测试；仓库的隐私检查
CHANGELOG.md    更新记录
```

## 维护

- 版本号写在 `SKILL.md` 开头的 `metadata.version`；每次更新，同时在 `CHANGELOG.md` 记一条。
- 规矩有编号（如 PACK-04、CN-15）。新增的规矩接着编号；被推翻的不删，标“已作废”，写明原因和取代的条目。
- 改了程序之后运行下面两项；每次推送，GitHub Actions 也会自动运行。

```bash
python3 -I tests/run_tests.py
python3 -I tests/check_hygiene.py
```

## 致谢

本 skill 的部分组织方式（规矩编号、常见错误表、结论强度分级、保护限定语清单、批注对照表、检查程序如实报告状态）参考了 [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) 中 academic-paper skill 的做法；文字是本仓库自己写的。

## 贡献者

- [Stillwang417](https://github.com/Stillwang417)
- Claude（Anthropic）

## 许可

MIT，见 `LICENSE`。

## English summary

paper-craft is a Claude Code skill with rules for writing and revising research papers in English and Chinese. Its core is *packaging*: presenting the authors' real contributions in the method fully, each with the cited prior work it builds on, what was changed, why, and what it brings, while routine or borrowed parts are cited and stated briefly, never presented as new. The other core part is *distilling innovation points* with a six-slot sentence: problem, name, what is modelled as which distribution, its parameters, derivation under constraints, and property under conditions. Facts and research integrity come first in the skill's order of priority. The skill also covers abstracts, introductions and conclusions, scientific rather than engineering style, formal written Chinese, terms and numbers, handling marked-up drafts, and literature search, plus four small checking scripts that use only the Python standard library. The rules are written in Chinese. The skill helps authors revise their manuscripts; the authors remain responsible for the content.

Install: `git clone https://github.com/Stillwang417/paper-craft.git ~/.claude/skills/paper-craft`. Licence: MIT.
