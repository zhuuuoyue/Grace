# Create

通过模板创建文本文件。

相关概念

- 模板：定义文本文件内容如何生成。
- 创建解决方案：多个模板的集合，定义了一次创建如何生成各种文件，如文件路径、文件编码、模板参数等。

数据库定义

- 文件编码表 `ent_encoding`

|列名|名称|主键|唯一|类型|
|-|-|-|-|-|
|`id`|文件编码 ID|是|是|`int`|
|`name`|文件编码名称||是|`str`|

- 模板表 `ent_template`

|列名|名称|主键|唯一|类型|
|-|-|-|-|-|
|`id`|模板 ID|是|是|`int`|
|`name`|模板名称||是|`str`|
|`content`|模板内容|||`str`|

- 生成模板表 `ent_creation_template`

|列名|名称|主键|唯一|类型|
|-|-|-|-|-|
|`id`|生成模板 ID|是|是|`int`|
|`template_id`|模板 ID|||`int`|
|`relative_path`|模板名称||是|`str`|
|`encoding_id`|文件编码 ID|||`int`|

- 创建解决方案表 `ent_creation_solution`

|列名|名称|主键|唯一|类型|
|-|-|-|-|-|
|`id`|模板 ID|是|是|`int`|
|`name`|模板名称||是|`str`|

- 创建解决方案-模板关系表 `rel_creation_solution_and_templates`

|列名|名称|主键|唯一|类型|
|-|-|-|-|-|
|`id`|模板 ID|是|是|`int`|
|`creation_solution_id`||||`int`|
|`creation_template_id`||||`int`|
