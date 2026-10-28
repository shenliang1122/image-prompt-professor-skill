# 输出约定

## 默认交付

先提供 JSON 代码块，再给中文拆解表；需要解释补充细节或图像无法确认的属性时，用简短中文说明。JSON 内部保持英文关键词，中文说明不混入 `prompt`。

JSON 沿用用户示例的嵌套结构，补齐场景与质量字段，并调整显示顺序以服务六维分析。JSON 对象本身不依赖键顺序；六维顺序必须体现在最终 `prompt` 和表格中。

单张图片或单个主题返回一个对象。明确要求多图分别分析时返回对象数组，并用中文按图片顺序标注对应表格。用户指定“只要 JSON”时返回无围栏的原始 JSON，不附表格或说明。

## 完整示例

以下仅示范“庭院中的成年女性水彩肖像”的格式，不是每次都要使用的人物、细节或风格。

```json
{
  "character_features": {
    "subject": "1woman, garden portrait",
    "proportions": "natural adult proportions",
    "pose": "seated pose, relaxed shoulders",
    "facial_features": "beautiful detailed eyes, defined nose, beautiful detailed lips, detailed eyelashes, extremely detailed face",
    "clothing": "cream linen dress, woven straw hat"
  },
  "scene_features": {
    "setting": "quiet garden courtyard",
    "environment": "climbing roses, weathered stone bench",
    "additional_details": "cream linen dress, woven straw hat, climbing roses, weathered stone bench, scattered petals"
  },
  "color_palette": {
    "dominant_colors": "sage green, warm cream, dusty rose",
    "saturation": "muted colors",
    "contrast": "gentle contrast"
  },
  "lighting_and_atmosphere": {
    "lighting": "soft morning light, dappled sunlight",
    "shadows": "soft leaf shadows",
    "atmosphere": "serene atmosphere"
  },
  "composition_and_perspective": {
    "composition": "three quarter portrait",
    "arrangement": "off center subject",
    "perspective": "eye level view",
    "depth_of_field": "soft background",
    "framing": "vertical composition, 3 by 4 aspect ratio"
  },
  "image_quality": {
    "resolution": "fine detail",
    "focus": "clear facial features",
    "rendering_quality": "delicate brushwork"
  },
  "style_theme": {
    "primary_style": "watercolor illustration",
    "mood": "serene",
    "theme": "garden portrait",
    "visual_vibe": "lyrical realism"
  },
  "typography_and_layout_potential": {
    "aesthetic_category": "editorial portrait",
    "text_space": "not applicable"
  },
  "prompt": "1woman, garden portrait, natural adult proportions, seated pose, relaxed shoulders, beautiful detailed eyes, defined nose, beautiful detailed lips, detailed eyelashes, extremely detailed face, cream linen dress, woven straw hat, quiet garden courtyard, climbing roses, weathered stone bench, scattered petals, sage green, warm cream, dusty rose, muted colors, gentle contrast, soft morning light, dappled sunlight, soft leaf shadows, serene atmosphere, three quarter portrait, off center subject, eye level view, soft background, vertical composition, 3 by 4 aspect ratio, fine detail, clear facial features, delicate brushwork, watercolor illustration, lyrical realism,"
}
```

## 字段含义

| 字段 | 用途 |
| --- | --- |
| `character_features` | 所有主题的主体信息；`subject` 总是描述真实主体，非人物仅将不适用字段填为 `not applicable` |
| `scene_features` | 场景、环境与至少五处具体细节 |
| `color_palette` | 色彩、饱和度与对比度，归入场景维度 |
| `lighting_and_atmosphere` | 光线、阴影、氛围 |
| `composition_and_perspective` | 构图、布局、视角、景深与画幅 |
| `image_quality` | 细节、焦点、完成度；不能冒充实际像素信息 |
| `style_theme` | 风格、媒介、情绪和主题；重复信息不再次拼入提示词 |
| `typography_and_layout_potential` | 美学类别及实际可用留白；不适用时用 `not applicable`，不据此自动添加文字 |
| `prompt` | 全部内容汇成单行英文关键词，严格按六维顺序组织 |

每个字段都保留，叶子值为非空字符串。`unknown` 只用于确实无法判断的重要属性。不要将占位词、重复主题、排版用途标签机械拼入最终提示词。

机器结构见 [schema.json](schema.json)。它检查字段与字符串格式；关键词语言、顺序和与原图的忠实程度还需要人工判断。

## 中文拆解表

使用四列：`顺序`、`组成部分`、`英文提示词`、`中文说明`。

固定六行，依次为主题内容、场景特征、环境光照、画幅视角、画面质量、画面风格与材质。每行的英文提示词应完整对应最终 `prompt` 中该维度的片段，顺序一致，不额外引入新设定。中文说明简要解释视觉效果；合理补充的内容在这里标明。

表格不是 JSON 的一部分。需要机器解析时，只复制 JSON 代码块，或直接要求“只要 JSON”。

## 交付检查

- JSON 可解析，无注释、重复键或结构尾逗号；每个要求的字段都存在。
- 英文关键词值无冒号、句点、换行或中文标点。
- 最终 `prompt` 单行、不分段、无标签，最后一个字符为半角逗号。
- 人物的眼睛、鼻子、嘴唇、睫毛与面部描述符合可见性，出现在人物字段和最终提示词里。
- 五处不同的具体细节出现在 `additional_details` 和最终提示词中。
- 六维顺序正确，表格与 JSON 表达同一画面；非人物主题保留真正的主体。
- 默认有中文表格；仅在用户要求精简输出时省略。
