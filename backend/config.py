NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "11040011"  # 替换为您的 Neo4j 数据库密码
# 实体类型和属性映射
ENTITY_TYPES = {
    "领域分类": "分类名称",
    "省市": "省市名称",
    "关键词": "关键词文本",
    "成果": "标题",
    "完成单位": "单位名称",
    "联系单位": "单位名称",
    "应用行业": "行业名称"
}
RELATION_TYPES = {
    "位于": ["成果", "省市"],
    "应用于": ["成果", "应用行业"],
    "由完成": ["成果", "完成单位"],
    "由联系": ["成果", "联系单位"],
    "属于": ["成果", "领域分类"],
    "包含关键词": ["成果", "关键词"]
}
# 问句分类相关配置
QUESTION_CLASSIFICATION_CONFIG = {
    "division": ['jie', 'men', 'gang', 'mu', 'ke', 'shu'],
    "brief_info_qwds": ['简介', '信息', '资料', '介绍', '表现'],
    "result_time_qwds": ['什么时候', '时间', '年份', '何时'],
    "result_category_qwds": ['属于什么领域', '领域', '分类', '类别'],
    "result_place_qwds": ['位于哪里', '位置', '所在地', '分布'],
    "result_keyword_qwds": ['关键词', '关键点', '主要词', '核心技术'],
    "result_applied_qwds": ['应用于', '应用在', '使用于', '应用于哪些'],
    "result_unit_qwds": ['由谁完成', '完成单位', '完成方', '开发单位'],
    "result_related_qwds": ['相关成果', '类似成果', '相关技术', '关联成果'],
    "unit_results_qwds": ['成果', '主要成就', '代表成果', '技术成果'],
    "province_results_qwds": ['成果', '技术成果', '先进技术', '有哪些技术成果', '有哪些成果', '有什么技术成果'],
    "industry_results_qwds": ['使用的技术', '应用的技术', '采用的技术'],
    "keyword_results_qwds": ['相关成果', '涉及的技术', '相关成果'],
    "category_results_qwds": ['包含哪些成果', '主要成果', '代表性成果'],
    "result_info_qwds": ['详情', '详细介绍', '详细信息'],
    "positive_qwds": ['是', '属于', '正确', '对', '正确吗'],
    "unit_address_qwds": ['地址', '位置', '在哪里', '在哪', '坐标的'],
    "post_code_qwds": ['邮政编码', '邮编', '编码'],
    "keyword_search_qwds": ['关键词', '关键字', '包含', '含有'],
    "statistic_qwds": ['多少', '数量', '统计', '共有', '总数'],
    "negative_qwds": ['不是', '不属于', '错误', '错', '错误吗']
}