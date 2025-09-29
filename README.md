# 基于Neo4j的中国先进技术问答系统

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)[![Neo4j](https://img.shields.io/badge/Neo4j-5.2-black?logo=neo4j)](https://neo4j.com/)[![Vue](https://img.shields.io/badge/Vue-3-%234FC08D?logo=vue.js)](https://vuejs.org/)[![Flask](https://img.shields.io/badge/Flask-2.0-black?logo=flask)](https://flask.palletsprojects.com/)

---

一个基于 **Neo4j 图数据库** 与 **模板匹配机制** 构建的智能问答系统，专注于中国先进技术领域的知识图谱构建与语义查询。适用于科研机构、政府部门、企业及开发者快速获取结构化技术情报。

---

## 🌟 项目介绍

本项目使用 **Neo4j 图数据库** 与 **模板匹配机制**，收集近12000条中国先进技术相关知识，设计20类问题，基本涵盖了基于本数据库的所有内容。

核心特性包括：

- **知识图谱驱动**：基于 Neo4j 构建，包含 7 类节点、5 类关系，支持复杂关联查询。
- **高效问答引擎**：预设 20 类问题模板，结合 Aho-Corasick 多模式匹配算法，实现毫秒级响应。
- **多维度数据覆盖**：涵盖人工智能、生物医药、新材料、新能源等前沿领域，收录约 12,000 条技术成果。
- **现代化前端界面**：采用 Vue 3 + Vite 构建，响应式设计，适配桌面与移动端。
- **高度可扩展**：支持自定义问题模板、特征词库与图谱结构，便于二次开发与领域迁移。

---

## 🧠 系统架构

### 技术栈

|   模块   |        技术        |
| :------: | :----------------: |
|   前端   | Vue 3, Vite, Axios |
|   后端   |   Python, Flask    |
| 图数据库 |       Neo4j        |
| 查询语言 |       Cypher       |
| 匹配算法 |    Aho-Corasick    |

### 处理流程

```
用户提问
   ↓
问题分类器（基于关键词匹配）
   ↓
问题解析器（映射至 Cypher 模板）
   ↓
答案搜索器（执行 Neo4j 查询）
   ↓
返回结构化答案
```

---

## 📊 数据概览

- **数据集**：tech_data.xlsx
- **成果数量**：约 12,000 条
- **覆盖领域**：人工智能、生物医药、新材料、新能源、高端制造等
- 节点类型：
  - 成果（Research）
  - 完成单位（Institution）
  - 省市（Province/City）
  - 关键词（Keyword）
  - 行业（Industry）
  - 领域分类（Field）
  - 联系单位（Contact Unit）
  - 等等
- **关系类型**：由完成、位于、属于、包含、应用于 等

---

## ❓ 支持的问题类型（共 20 类）

|   类别   |                   示例问题                   |
| :------: | :------------------------------------------: |
|  简介类  |           “人工智能的简介是什么？”           |
|  时间类  |              “该成果何时发布？”              |
|  分类类  |           “这项技术属于哪个领域？”           |
|  地点类  |         “主要研究机构位于哪些省市？”         |
| 关键词类 |           “该成果的关键词有哪些？”           |
|  应用类  |          “深度学习应用于哪些行业？”          |
|  单位类  |           “哪些单位参与了该研究？”           |
|  成果类  |        “清华大学在AI领域有哪些成果？”        |
|  统计类  |         “生物医药领域共有多少成果？”         |
|  判断类  |       “量子计算属于新一代信息技术吗？”       |
|    …     | 更多模板详见`backend/question_classifier.py` |

---

## 🚀 快速部署

### 1. 克隆项目

```
git clone https://github.com/feiyu1104/TechnicalQA_System.git
cd TechnicalQA_System
```

### 2. 安装 Python 依赖

```
conda create -n techqa python=3.9
conda activate techqa
pip install -r requirements.txt
```

### 3. 部署 Neo4j

- 下载并安装 [Neo4j Desktop ](https://neo4j.com/download/)（推荐 v5.26）
- 启动数据库实例，确保服务运行于 `bolt://localhost:7687`
- 通过浏览器访问 `http://localhost:7474` 验证

### 4. 导入知识图谱数据

1. 将 `tech_data.xlsx` 转换为 `research_data.csv`（UTF-8 编码）
2. 将 CSV 文件放入 Neo4j 的 `import` 目录（路径因系统而异）
3. 在 Neo4j Browser 中执行 `data/import.cypher` 脚本：

```
// 创建索引（确保字段名与CSV列一致）
CREATE INDEX FOR (p:省市) ON (p.省市名称);
CREATE INDEX FOR (u:完成单位) ON (u.单位名称);
CREATE INDEX FOR (c:联系单位) ON (c.单位名称);
CREATE INDEX FOR (i:应用行业) ON (i.行业名称);
CREATE INDEX FOR (k:关键词) ON (k.关键词文本);
CREATE INDEX FOR (a:领域分类) ON (a.分类名称);
CREATE INDEX FOR (r:成果) ON (r.标题);

// 导入数据并创建节点
LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
MERGE (p:省市 {省市名称: row.省市})
MERGE (u:完成单位 {单位名称: row.完成单位})
MERGE (c:联系单位 {
  单位名称: row.联系单位名称,
  联系地址: row.联系单位地址,
  邮政编码: row.邮政编码
})
MERGE (i:应用行业 {
  行业名称: row.应用行业名称,
  行业码: row.应用行业码
})
MERGE (a:领域分类 {分类名称: row.领域类别})
MERGE (r:成果 {
  标题: row.标题,
  项目年度编号: row.项目年度编号,
  成果类别: row.成果类别,
  成果公布年份: TOINTEGER(row.成果公布年份),
  成果简介: row.成果简介,
  限制使用: row.限制使用
})
WITH row
WHERE row.关键词1 <> '' OR row.关键词2 <> '' OR row.关键词3 <> ''
MERGE (k1:关键词 {关键词文本: row.关键词1})
MERGE (k2:关键词 {关键词文本: row.关键词2})
MERGE (k3:关键词 {关键词文本: row.关键词3});

// 创建关系
LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
MATCH (r:成果 {标题: row.标题})
MATCH (p:省市 {省市名称: row.省市})
MERGE (r)-[:位于]->(p);

LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
MATCH (u:完成单位 {单位名称: row.完成单位})
MATCH (p:省市 {省市名称: row.省市})
MERGE (u)-[:位于]->(p);

LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
MATCH (c:联系单位 {单位名称: row.联系单位名称})
MATCH (p:省市 {省市名称: row.省市})
MERGE (c)-[:位于]->(p);

LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
MATCH (r:成果 {标题: row.标题})
MATCH (u:完成单位 {单位名称: row.完成单位})
MERGE (r)-[:由完成]->(u);

LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
MATCH (r:成果 {标题: row.标题})
MATCH (c:联系单位 {单位名称: row.联系单位名称})
MERGE (r)-[:由联系]->(c);

LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
MATCH (r:成果 {标题: row.标题})
MATCH (i:应用行业 {行业名称: row.应用行业名称})
MERGE (r)-[:应用于]->(i);

LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
MATCH (r:成果 {标题: row.标题})
MATCH (a:领域分类 {分类名称: row.领域类别})
MERGE (r)-[:属于]->(a);

LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
WITH row WHERE row.关键词1 <> ''
MATCH (r:成果 {标题: row.标题})
MATCH (k:关键词 {关键词文本: row.关键词1})
MERGE (r)-[:包含关键词]->(k);

LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
WITH row WHERE row.关键词2 <> ''
MATCH (r:成果 {标题: row.标题})
MATCH (k:关键词 {关键词文本: row.关键词2})
MERGE (r)-[:包含关键词]->(k);

LOAD CSV WITH HEADERS FROM "file:///research_data.csv" AS row
WITH row WHERE row.关键词3 <> ''
MATCH (r:成果 {标题: row.标题})
MATCH (k:关键词 {关键词文本: row.关键词3})
MERGE (r)-[:包含关键词]->(k);
```

> 💡 提示：确保 CSV 列名与 Cypher 脚本中的字段完全一致。 

### 5. 配置并启动后端

编辑 `backend/config.py`：

```
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password"  # 默认密码为 "neo4j"，首次登录需修改
```

启动服务：

```
cd backend
python app.py
# 默认监听 http://localhost:5000
```

### 6. 启动前端

```
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173` 即可使用系统。

```
langgraph_my/
├── backend/               # 后端服务
│   ├── app.py             # Flask 入口
│   ├── config.py          # 配置文件
│   ├── question_classifier.py  # 问题分类器
│   ├── question_parser.py     # 问题解析器
│   └── answer_searcher.py     # 答案生成器
├── frontend/              # 前端应用
│   ├── src/
│   └── package.json
├── tech_data.xlsx  # 原始数据
├── requirements.txt       # Python 依赖
├── LICENSE                # 开源许可证
└── README.md
```

---

## 🧪 示例运行

![演示图](./演示图.png)

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

- 如果你发现了 bug，请通过 Issue 反馈
- 如果你有新功能建议，也欢迎提出
- 提交 PR 前请确保代码已通过测试

---

## 🙏 致谢

本项目基于以下优秀开源技术构建，在此向其社区与维护者致以诚挚感谢：

- **Neo4j**：强大的原生图数据库，为知识图谱存储与查询提供核心支持
- **Vue 3** 与 **Vite**：现代化前端框架与构建工具，助力高效开发响应式界面
- **Flask**：轻量灵活的 Python Web 框架，支撑后端服务稳定运行
- **Aho-Corasick 算法**：高效的多模式字符串匹配方案，提升问题识别性能

感谢开源生态为本项目提供的坚实技术基础。

---

> 本系统所用数据来源于公开渠道整理的中国先进技术成果信息，涵盖人工智能、生物医药、新材料、新能源等领域，共计约 12,000 条记录。数据仅用于学术研究与技术演示，**不得用于商业用途**。本项目不对数据的完整性、准确性或时效性作任何明示或暗示的保证。任何基于本数据的使用均需遵守相关法律法规，并自行承担相应责任。
