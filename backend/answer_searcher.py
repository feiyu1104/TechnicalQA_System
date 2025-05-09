from py2neo import Graph
class AnswerSearcher:
    def __init__(self, uri, user, password):
        self.g = Graph(uri, auth=(user, password))
        self.num_limit = 20
    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers
    '''根据对应的question_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = ""
        if not answers:
            return "未找到相关信息。"
        if question_type == 'result_brief':
            desc = [i['m.成果简介'] for i in answers]
            subject = answers[0]['m.标题']
            final_answer = f"{subject}的简介：{'；'.join(list(set(desc))[:self.num_limit])}"
        elif question_type == 'result_time':
            times = [i['m.成果公布年份'] for i in answers]
            subject = answers[0]['m.标题']
            final_answer = f"{subject}的公布年份：{times[0]}"
        elif question_type == 'result_category':
            categories = [i['n.分类名称'] for i in answers]
            subject = answers[0]['m.标题']
            final_answer = f"{subject}属于领域：{'；'.join(list(set(categories))[:self.num_limit])}"
        elif question_type == '_placeresult':
            provinces = [i['n.省市名称'] for i in answers]
            subject = answers[0]['m.标题']
            final_answer = f"{subject}位于：{'；'.join(list(set(provinces))[:self.num_limit])}"
        elif question_type == 'result_keywords':
            keywords = [i['n.关键词文本'] for i in answers]
            subject = answers[0]['m.标题']
            final_answer = f"{subject}的关键词：{'；'.join(list(set(keywords))[:self.num_limit])}"
        elif question_type == 'result_applied':
            industries = [i['n.行业名称'] for i in answers]
            subject = answers[0]['m.标题']
            final_answer = f"{subject}应用于：{'；'.join(list(set(industries))[:self.num_limit])}"
        elif question_type == 'result_unit':
            units = [i['n.单位名称'] for i in answers]
            subject = answers[0]['m.标题']
            final_answer = f"{subject}由以下单位完成：{'；'.join(list(set(units))[:self.num_limit])}"
        elif question_type == 'unit_address':
            addresses = [i['m.联系地址'] for i in answers]
            subject = answers[0]['m.单位名称']
            final_answer = f"{subject}的地址：{addresses[0]}"
        elif question_type == 'post_code':
            post_codes = [i['m.邮政编码'] for i in answers]
            subject = answers[0]['m.单位名称']
            final_answer = f"{subject}的邮政编码：{post_codes[0]}"
        elif question_type == 'statistic':
            if not answers:
                final_answer = "未找到相关信息。"
            else:
                stats = {}
                for answer in answers:
                    category = answer['n.分类名称']
                    count = answer['count(m)']
                    stats[category] = count
                final_answer = "成果数量统计如下：\n"
                for category, count in stats.items():
                    final_answer += f"{category}：{count}项\n"
        elif question_type == 'keyword_search':
            results = [i['m.标题'] for i in answers]
            subject = answers[0]['n.关键词文本']
            final_answer = f"包含关键词'{subject}'的成果有：\n" + '\n'.join(list(set(results))[:self.num_limit])
        elif question_type == 'unit_results':
            results = [i['n.标题'] for i in answers]
            subject = answers[0]['m.单位名称']
            final_answer = f"{subject}的成果有：\n" + '\n'.join(list(set(results))[:self.num_limit])
        elif question_type == 'province_results':
            results = [i['n.标题'] for i in answers]
            subject = answers[0]['m.省市名称']
            final_answer = f"{subject}的成果有：\n" + '\n'.join(list(set(results))[:self.num_limit])
        elif question_type == 'industry_results':
            results = [i['n.标题'] for i in answers]
            subject = answers[0]['m.行业名称']
            final_answer = f"{subject}使用的技术成果有：\n" + '\n'.join(list(set(results))[:self.num_limit])
        elif question_type == 'keyword_results':
            results = [i['n.标题'] for i in answers]
            subject = answers[0]['m.关键词文本']
            final_answer = f"{subject}相关的技术成果有：\n" + '\n'.join(list(set(results))[:self.num_limit])
        elif question_type == 'category_results':
            results = [i['n.标题'] for i in answers]
            subject = answers[0]['m.分类名称']
            final_answer = f"{subject}领域的技术成果有：\n" + '\n'.join(list(set(results))[:self.num_limit])
        elif question_type == 'result_detail':
            if answers:
                properties = answers[0]['m']
                subject = properties['标题']
                details = f"成果名称：{subject}\n"
                details += f"成果简介：{properties.get('成果简介', '')}\n"
                details += f"公布年份：{properties.get('成果公布年份', '')}\n"
                details += f"成果类别：{properties.get('成果类别', '')}\n"
                details += f"完成单位：{properties.get('完成单位', '')}\n"
                details += f"所属领域：{properties.get('领域分类', '')}\n"
                details += f"应用行业：{properties.get('应用行业', '')}\n"
                details += f"关键词：{properties.get('关键词', '')}\n"
                final_answer = details
        elif question_type == 'result_related':
            industries = [i['n.行业名称'] for i in answers]
            subject = answers[0]['m.标题']
            final_answer = f"与{subject}相关的应用行业有：{'；'.join(list(set(industries))[:self.num_limit])}"
        elif question_type == 'result_unit_judge':
            if answers:
                final_answer = "是的，该成果由该单位完成。"
            else:
                final_answer = "抱歉，该成果并非由该单位完成。"
        elif question_type == 'result_province_judge':
            if answers:
                final_answer = "是的，该成果位于该省份。"
            else:
                final_answer = "抱歉，该成果并不在该省份。"
        elif question_type == 'result_industry_judge':
            if answers:
                final_answer = "是的，该成果应用于该行业。"
            else:
                final_answer = "抱歉，该成果并未应用于该行业。"
        elif question_type == 'result_keyword_judge':
            if answers:
                final_answer = "是的，该成果包含该关键词。"
            else:
                final_answer = "抱歉，该成果不包含该关键词。"
        elif question_type == 'result_category_judge':
            if answers:
                final_answer = "是的，该成果属于该领域。"
            else:
                final_answer = "抱歉，该成果不属于该领域。"
        return final_answer