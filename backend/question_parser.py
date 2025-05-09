class QuestionPaser:
    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict
    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'result_brief':
                sql = self.sql_transfer(question_type, entity_dict.get('result'))
            elif question_type == 'result_time':
                sql = self.sql_transfer(question_type, entity_dict.get('result'))
            elif question_type == 'result_category':
                sql = self.sql_transfer(question_type, entity_dict.get('result'))
            elif question_type == '_placeresult':
                sql = self.sql_transfer(question_type, entity_dict.get('result'))
            elif question_type == 'result_keywords':
                sql = self.sql_transfer(question_type, entity_dict.get('result'))
            elif question_type == 'result_applied':
                sql = self.sql_transfer(question_type, entity_dict.get('result'))
            elif question_type == 'result_unit':
                sql = self.sql_transfer(question_type, entity_dict.get('result'))
            elif question_type == 'result_related':
                sql = self.sql_transfer(question_type, entity_dict.get('result'))
            elif question_type == 'unit_results':
                sql = self.sql_transfer(question_type, entity_dict.get('unit'))
            elif question_type == 'unit_address':
                sql = self.sql_transfer(question_type, entity_dict.get('unit'))
            elif question_type == 'post_code':
                sql = self.sql_transfer(question_type, entity_dict.get('unit'))
            elif question_type == 'province_results':
                sql = self.sql_transfer(question_type, entity_dict.get('province'))
            elif question_type == 'industry_results':
                sql = self.sql_transfer(question_type, entity_dict.get('industry'))
            elif question_type == 'keyword_results':
                sql = self.sql_transfer(question_type, entity_dict.get('keyword'))
            elif question_type == 'keyword_search':
                sql = self.sql_transfer(question_type, entity_dict.get('keyword'))
            elif question_type == 'category_results':
                sql = self.sql_transfer(question_type, entity_dict.get('category'))
            elif question_type == 'result_detail':
                sql = self.sql_transfer(question_type, entity_dict.get('result'))
            elif question_type == 'statistic':
                sql = self.sql_transfer(question_type, entity_dict.get('category'))
            elif question_type == 'result_unit_judge':
                sql = self.sql_transfer(question_type, entity_dict.get('result'), entity_dict.get('unit'))
            elif question_type == 'result_province_judge':
                sql = self.sql_transfer(question_type, entity_dict.get('result'), entity_dict.get('province'))
            elif question_type == 'result_industry_judge':
                sql = self.sql_transfer(question_type, entity_dict.get('result'), entity_dict.get('industry'))
            elif question_type == 'result_keyword_judge':
                sql = self.sql_transfer(question_type, entity_dict.get('result'), entity_dict.get('keyword'))
            elif question_type == 'result_category_judge':
                sql = self.sql_transfer(question_type, entity_dict.get('result'), entity_dict.get('category'))
            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
        return sqls
    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities, related_entities=None):
        if not entities:
            return []
        # 查询语句
        sql = []
        # 查询成果简介
        if question_type == 'result_brief':
            sql = ["MATCH (m:成果) where m.标题 = '{0}' return m.标题, m.成果简介".format(i) for i in entities]
        # 查询成果时间
        elif question_type == 'result_time':
            sql = ["MATCH (m:成果) where m.标题 = '{0}' return m.标题, m.成果公布年份".format(i) for i in entities]
        # 查询成果领域分类
        elif question_type == 'result_category':
            sql = ["MATCH (m:成果)-[r:属于]->(n:领域分类) where m.标题 = '{0}' return m.标题, n.分类名称".format(i) for i in entities]
        # 查询成果分布地区
        elif question_type == '_placeresult':
            sql = ["MATCH (m:成果)-[r:位于]->(n:省市) where m.标题 = '{0}' return m.标题, n.省市名称".format(i) for i in entities]
        # 查询成果关键词
        elif question_type == 'result_keywords':
            sql = ["MATCH (m:成果)-[r:包含关键词]->(n:关键词) where m.标题 = '{0}' return m.标题, n.关键词文本".format(i) for i in entities]
        # 查询成果应用行业
        elif question_type == 'result_applied':
            sql = ["MATCH (m:成果)-[r:应用于]->(n:应用行业) where m.标题 = '{0}' return m.标题, n.行业名称".format(i) for i in entities]
        # 查询成果完成单位
        elif question_type == 'result_unit':
            sql = ["MATCH (m:成果)-[r:由完成]->(n:完成单位) where m.标题 = '{0}' return m.标题, n.单位名称".format(i) for i in entities]
        # 查询相关成果
        elif question_type == 'result_related':
            sql = ["MATCH (m:成果)-[r:应用于]->(n:应用行业) where m.标题 = '{0}' return m.标题, n.行业名称".format(i) for i in entities]
        #查询单位邮政编码
        elif question_type == 'post_code':
            sql = ["MATCH (m:联系单位) where m.单位名称 = '{0}' return m.单位名称, m.邮政编码".format(i) for i in entities]
        # 查询单位成果
        elif question_type == 'unit_results':
            sql = ["MATCH (m:完成单位) WHERE m.单位名称='{0}' OPTIONAL MATCH (m)<-[:由完成]-(n:成果) RETURN m.单位名称, n.标题".format(i) for i in entities]
        # 查询省份成果
        elif question_type == 'province_results':
            sql = ["MATCH (m:省市) WHERE m.省市名称='{0}' OPTIONAL MATCH (m)<-[:位于]-(n:成果) RETURN m.省市名称, n.标题".format(i) for i in entities]
        # 查询行业技术
        elif question_type == 'industry_results':
            sql = ["MATCH (m:应用行业) WHERE m.行业名称='{0}' OPTIONAL MATCH (m)<-[:应用于]-(n:成果) RETURN m.行业名称, n.标题".format(i) for i in entities]
        # 查询关键词相关成果
        elif question_type == 'keyword_results':
            sql = ["MATCH (m:关键词) WHERE m.关键词文本='{0}' OPTIONAL MATCH (m)<-[:包含关键词]-(n:成果) RETURN m.关键词文本, n.标题".format(i) for i in entities]
        # 查询领域技术成果
        elif question_type == 'category_results':
            sql = ["MATCH (m:领域分类) WHERE m.分类名称='{0}' OPTIONAL MATCH (m)<-[:属于]-(n:成果) RETURN m.分类名称, n.标题".format(i) for i in entities]
        #通过关键词查询
        elif question_type == 'keyword_search':
            sql = ["MATCH (m:成果)-[r:包含关键词]->(n:关键词) where n.关键词文本 = '{0}' return n.关键词文本, m.标题".format(i) for i in entities]
        #查询单位的位置
        elif question_type == 'unit_address':
            sql = ["MATCH (m:联系单位) where m.单位名称 = '{0}' return m.单位名称, m.联系地址".format(i) for i in entities]
        # 查询成果详细信息
        elif question_type == 'result_detail':
            sql = ["MATCH (m:成果) where m.标题 = '{0}' return m".format(i) for i in entities]
        #统计类问题
        elif question_type == 'statistic':
            sql = ["MATCH (m:成果)-[r:属于]->(n:领域分类) where n.分类名称 = '{0}' return n.分类名称, count(m)".format(i) for i in entities]
        # 判断性问题 - 成果与单位关系
        elif question_type == 'result_unit_judge':
            sql = ["MATCH (m:成果)-[r:由完成]->(n:完成单位) where m.标题 = '{0}' and n.单位名称 = '{1}' return m.标题, n.单位名称".format(entities[0], related_entities[0]) if related_entities else []]
        # 判断性问题 - 成果与省份关系
        elif question_type == 'result_province_judge':
            sql = ["MATCH (m:成果)-[r:位于]->(n:省市) where m.标题 = '{0}' and n.省市名称 = '{1}' return m.标题, n.省市名称".format(entities[0], related_entities[0]) if related_entities else []]
        # 判断性问题 - 成果与行业关系
        elif question_type == 'result_industry_judge':
            sql = ["MATCH (m:成果)-[r:应用于]->(n:应用行业) where m.标题 = '{0}' and n.行业名称 = '{1}' return m.标题, n.行业名称".format(entities[0], related_entities[0]) if related_entities else []]
        # 判断性问题 - 成果与关键词关系
        elif question_type == 'result_keyword_judge':
            sql = ["MATCH (m:成果)-[r:包含关键词]->(n:关键词) where m.标题 = '{0}' and n.关键词文本 = '{1}' return m.标题, n.关键词文本".format(entities[0], related_entities[0]) if related_entities else []]
        # 判断性问题 - 成果与领域分类关系
        elif question_type == 'result_category_judge':
            sql = ["MATCH (m:成果)-[r:属于]->(n:领域分类) where m.标题 = '{0}' and n.分类名称 = '{1}' return m.标题, n.分类名称".format(entities[0], related_entities[0]) if related_entities else []]
        return sql