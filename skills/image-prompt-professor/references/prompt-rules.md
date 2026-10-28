# 提示词规则

## 六个维度

始终按以下顺序构建最终 `prompt` 和中文拆解表，同一维度内优先放核心关键词。

| 顺序 | 维度 | 描述范围 |
| --- | --- | --- |
| 1 | 主题内容 | 主体、数量、外观、表情、服装、姿态、动作、物体材质 |
| 2 | 场景特征 | 空间、前景、背景、道具、具体细节、配色 |
| 3 | 环境光照 | 光源、方向、软硬、明暗、阴影、氛围 |
| 4 | 画幅视角 | 景别、构图、机位、视角、画幅、景深 |
| 5 | 画面质量 | 对焦、纹理表现、细节程度、渲染完成度 |
| 6 | 画面风格与材质 | 摄影、插画、油画、水彩、三维渲染、艺术风格 |

## 依据与细节

- 图片反推以实际可见内容为准，不把猜测写成观察结果。文字主题模式可以补充合理的创作细节。
- 在核心主体之外选至少五处不同的具体细节，放入 `scene_features.additional_details`，并纳入最终 `prompt` 的相应维度。主体细节也可收录在此字段。
- 优先选择姿势、衣服纹理、材质、道具、背景结构、反射、色彩、光线、构图等可用于复现画面的内容；`masterpiece` 等泛化质量词不计入五处细节。
- 简单图像优先观察形状、位置、边缘、表面和配色，不为凑数新增人物或道具。若确实不足五处，可补充不改变构图的细节，并在中文说明中标为“合理补充”；不得宣称它们是原图已有内容。
- 固定用户明确的主题、数量、颜色、服装、保留项和修改项。不要每次套用婴儿、奢侈品或时装主题。

## 人物

- 用可支持的数量和人物类别，例如 `1girl`、`2girls`、`1boy`、`1woman`、`1man`、`2people`。不把成年女性一律写成 `1girl`，无法确定数量时用 `crowd` 等词。
- 面部可见时，必须包含眼睛、鼻子和嘴唇的描述；可用 `beautiful detailed eyes, defined nose, beautiful detailed lips, detailed eyelashes, extremely detailed face`，也可根据原图改成更准确的短语。
- 眼睛颜色、鼻型、唇形、睫毛长短应遵循图片或主题，不能统一替换为某种理想化五官。此类词是生成辅助线索，不保证消除模型的面部变形。
- 对背影、遮挡、剪影或极远人物，不虚构可见五官；可用 `hidden eyes, hidden nose, hidden lips, obscured eyelashes, concealed face`，同时保留 `rear view` 等构图线索。
- 对非人物主题，`character_features.subject` 仍必须写真实主体，如 `ceramic teapot` 或 `mountain lake`。仅将不适用的人物字段写为 `not applicable`；这些占位词不进入最终 `prompt`。
- 不推断敏感身份或健康状况。只写与画面有关的可见特征或用户明确给出的设定。

## 风格、材质与质量

- 区分物体材料与创作媒介：例如茶壶的 `glazed ceramic` 属于主体，作品的 `oil painting` 属于第六维度。
- 选择匹配画面的媒介，例如 `photography`、`digital illustration`、`oil painting`、`watercolor`、`anime illustration`、`concept art`、`3D render`。
- `HDR`、`UHD`、`sharp focus`、`physically based rendering`、`extreme detail`、`vivid colors`、`bokeh` 按需要选择，不全部堆叠。水彩或模糊风格不强行写成锐利摄影。
- `studio lighting` 属于第三维度，`bokeh` 和景深属于第四维度；不要因为它们出现在质量词示例里而放错顺序。
- 不把 `UHD` 或 `8K` 宣称为已验证的源图分辨率。未知实际像素时可描述观感，如 `fine detail`；用户要求生成高分辨率时可把它作为目标质量。

## 关键词与标点

- 英文值用独立词语或简短名词、形容词短语，如 `garden portrait`、`soft morning light`，不用完整说明句。
- 提示词仅以半角逗号分隔，不用中文逗号、分号、项目符号或换行；不加 `subject`、`lighting`、`medium` 等分段标签。
- 英文关键词值里不写冒号或句点；画幅用 `3 by 4 aspect ratio`，不要用带冒号的比例写法；避免带小数点的光圈写法。
- `prompt` 末尾一个半角逗号，其他字符串无需追加尾逗号。不要重复关键词，也不要将 `unknown`、`not applicable` 直接拼入 `prompt`。
