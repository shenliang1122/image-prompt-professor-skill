# 图像提示词教授 · Image Prompt Professor

将参考图片或文字主题整理为 **英文图像提示词、结构化 JSON 和中文拆解表**。以艺术与设计的视角分析主体、场景、光照、构图、质量和风格，适用于图片反推、视觉创作和生成模型提示词编写。

Skill 调用名：`$image-prompt-professor`。

## 快速体验

上传一张图片，然后输入：

```text
$image-prompt-professor 反推这张图片，输出 JSON 和中文拆解表
```

也可以从文字主题开始：

```text
$image-prompt-professor 写一组陶瓷茶壶静物摄影的提示词，米白色釉面，竹提手，柔和窗光
```

明确要求生成图片时，会衔接宿主环境中的图像生成工具：

```text
$image-prompt-professor 生成一张暖色水彩风格的森林小屋图片
```

## 安装

### 在 Codex 中安装

把下面这句话发送给 Codex：

```text
请使用 $skill-installer 安装 https://github.com/shenliang1122/image-prompt-professor-skill/tree/main/skills/image-prompt-professor
```

安装后可在下一条消息中调用 `$image-prompt-professor`。

### 手动安装

在 macOS 或 Linux 终端运行：

```bash
git clone https://github.com/shenliang1122/image-prompt-professor-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R image-prompt-professor-skill/skills/image-prompt-professor "${CODEX_HOME:-$HOME/.codex}/skills/"
```

以上命令用于首次安装。已有同名 Skill 时，先保留自己的修改，再替换目标文件夹。已通过个人插件安装时，更新该插件中的 Skill 即可。

也可以下载仓库 ZIP，将整个 `skills/image-prompt-professor/` 文件夹导入支持 Agent Skills 的产品；需要保留 `references/`、`scripts/` 和 `agents/`。

私有仓库的安装需要具有仓库访问权限的 GitHub 登录状态。其他支持 `SKILL.md` 的产品可复用指令与参考文件，具体调用语法和工具能力以宿主为准。

## 支持的用法

| 需求 | 调用示例 | 行为 |
| --- | --- | --- |
| 图片反推 | `$image-prompt-professor 反推这张图` | 查看实际图片，提取视觉关键词 |
| 文字主题 | `$image-prompt-professor 写一组雨夜未来城市的提示词` | 根据主题补足合理细节 |
| 指定变换 | `$image-prompt-professor 保留人物五官和衣服，改成可爱的婴儿比例，先给提示词` | 只调整指定属性，保留其他特征 |
| 多图分析 | `$image-prompt-professor 分别分析这三张图` | 按图片顺序输出 JSON 数组及对应表格 |
| 直接出图 | `$image-prompt-professor 生成一张水彩森林小屋图片` | 组织提示词后调用可用的图像生成工具 |
| 编辑原图 | `$image-prompt-professor 把这张图改成油画风格，保留构图` | 使用原图和明确的保留项执行编辑 |

仅上传图片并调用 Skill 时，默认反推提示词。说“生成提示词”会输出提示词；说“生成图片”才会执行出图。婴儿化是可选变换，不是默认效果。

## 输出示例

以下是“陶瓷茶壶静物摄影”的示例，展示单行 `prompt` 与对应的中文拆解表。完整的可解析 JSON 见 [examples/ceramic-teapot.json](examples/ceramic-teapot.json)。

```text
ceramic teapot, rounded body, glazed ceramic surface, curved spout, bamboo handle, fitted lid, minimal studio, linen backdrop, oak table, ivory white, warm beige, muted colors, gentle contrast, soft window light, soft cast shadow, calm atmosphere, centered composition, single object, eye level view, shallow depth of field, square composition, fine detail, sharp focus, realistic surface texture, product photography, minimalism,
```

| 顺序 | 组成部分 | 英文提示词 | 中文说明 |
| --- | --- | --- | --- |
| 1 | 主题内容 | ceramic teapot, rounded body, glazed ceramic surface, curved spout, bamboo handle, fitted lid | 陶瓷茶壶的形体与材料，突出釉面、弯曲壶嘴、竹提手和壶盖。 |
| 2 | 场景特征 | minimal studio, linen backdrop, oak table, ivory white, warm beige, muted colors, gentle contrast | 亚麻背景与橡木桌面，米白和暖米色形成柔和的静物环境。 |
| 3 | 环境光照 | soft window light, soft cast shadow, calm atmosphere | 柔和窗光和落影，营造安静的气氛。 |
| 4 | 画幅视角 | centered composition, single object, eye level view, shallow depth of field, square composition | 单个主体居中，平视、浅景深、方形构图。 |
| 5 | 画面质量 | fine detail, sharp focus, realistic surface texture | 清晰对焦，表现真实表面纹理。 |
| 6 | 画面风格与材质 | product photography, minimalism | 极简产品摄影。 |

人物图像会根据可见性加入眼睛、鼻子、嘴唇、睫毛和面部细节。产品、风景、抽象图形等主题保留真实主体，不添加无关人物。

## 格式约定

默认输出 **一个 JSON 代码块和一张中文拆解表**：

- JSON 字段名与提示词值使用英文，值为关键词或短语；中文用于表头和说明。
- `prompt` 为连续单行，按“主题 → 场景 → 光照 → 画幅视角 → 质量 → 风格与媒介”的顺序排列。
- 关键词使用英文半角逗号分隔，`prompt` 字符串末尾恰好一个英文逗号。
- 英文关键词值不包含冒号、句点或分段标签；JSON 结构必需的冒号正常保留。
- 至少包含五处不同、与主题协调的具体细节；图片反推中的创作补充会在中文说明中标明。
- JSON 对象和数组不使用尾随逗号；比例写作 `3 by 4 aspect ratio` 等英文短语。

按需要在请求末尾追加：

| 指令 | 输出 |
| --- | --- |
| `只要 JSON` | 可直接解析的原始 JSON，无 Markdown 围栏和表格 |
| `只要提示词` | 单行英文关键词 |
| `只要图片` | 生成或编辑后的图片 |

完整字段说明见 [输出约定](skills/image-prompt-professor/references/output-contract.md)，机器可读定义见 [JSON Schema](skills/image-prompt-professor/references/schema.json)。

## 运行条件

| 能力 | 条件 |
| --- | --- |
| 从文字生成提示词 | 宿主能够加载 Skill 指令 |
| 图片反推 | 宿主能够查看用户提供的图片 |
| 生成或编辑图片 | 宿主提供图像生成或编辑工具；在支持的 Codex 环境优先使用内置工具 |
| 校验 JSON 输出 | Python 3.9 或更高版本，无第三方 Python 依赖 |

Skill 本身不内置视觉模型、图片生成服务或 API 客户端。普通提示词分析不需要配置 API Key；实际图像生成使用宿主提供的能力与额度。没有生成工具时，仍可交付提示词。

图像提示词可以描述海报的字体、层级和布局；精确文案应在请求中单独指定。关键词不能保证每次都生成完全相同的画面或文字。

## 校验输出

在仓库根目录运行示例校验：

```bash
python3 skills/image-prompt-professor/scripts/validate_output.py examples/ceramic-teapot.json
```

将实际输出中的 JSON 单独保存为 `output.json`，再执行：

```bash
python3 skills/image-prompt-professor/scripts/validate_output.py output.json
```

也支持标准输入：

```bash
python3 skills/image-prompt-professor/scripts/validate_output.py < output.json
```

校验器检查字段结构、重复 JSON 键、关键词字符与标点、末尾逗号、重复关键词、至少五处细节，以及人物五官词类别。它不能判断视觉忠实度、英文语义或六维排列是否正确，这些仍需结合图片审核。

## 文件结构

```text
image-prompt-professor-skill/
├── README.md
├── examples/
│   └── ceramic-teapot.json
└── skills/
    └── image-prompt-professor/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        │   ├── prompt-rules.md
        │   ├── output-contract.md
        │   ├── transformations.md
        │   └── schema.json
        └── scripts/
            └── validate_output.py
```

## 许可证

本仓库尚未指定开源许可证。
