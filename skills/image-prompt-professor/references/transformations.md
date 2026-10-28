# 参考图变换

仅在用户明确要求改变参考图时使用，忠实反推模式不默认应用变换。

## 保留项与修改项

先区分需保留的五官特征、服装设计、发型、姿态、配饰、构图、色彩和环境，以及明确要求改变的属性。只改变指定项，其余保持一致。

提示词描述目标画面的结果状态，例如 `scaled original clothing design`，不使用 `convert this image`、`please change` 等说明句。真正调用编辑工具时，另外明确传递保留和修改约束，并提供原图，不能仅靠文字声称保留身份。

## 年龄与比例

仅在用户要求成人转儿童或婴儿时，使用 `stylized toddler, soft baby fat, small child body proportions, slightly enlarged head, chubby cheeks` 等词。婴儿化只是用户原始示例，不是默认风格。

尽可能保留用户指定的五官特征和衣服款式，按目标体型调整尺寸，使用适龄服饰和姿态。不要承诺精确保留面部身份或百分之百复现。

## 风格与媒介

只调整目标媒介、笔触、质感、渲染和光线表现；除非用户要求，不改变主体数量、服装、空间关系和核心构图。不要为了增加细节而堆叠互相冲突的风格。

## 构图与画幅

把目标视角和画幅写入 `composition_and_perspective` 和最终提示词。使用 `full body vertical portrait`、`cinematic wide shot`、`centered square composition`、`3 by 4 aspect ratio` 等结果短语，避免在英文值内使用冒号。

生成或编辑时把画幅要求一并传给工具，并保持重要主体处于画面内。
