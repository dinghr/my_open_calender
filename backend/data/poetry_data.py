# 古诗数据库数据

此文件定义了小学1-6年级和初中7-9年级的必背古诗数据。

## 数据结构

每首古诗包含以下字段：
- id: 唯一标识
- title: 诗题
- title_pinyin: 诗题拼音
- author: 作者
- dynasty: 朝代
- lines: 诗句列表，每句包含text、pinyin和chars
- translation: 译文
- annotation: 注释
- grade: 适用年级 (1-9)
- semester: 学期
- category: 分类 (必背/选背/拓展)
- textbook: 教材版本