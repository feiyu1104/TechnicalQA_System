import os
import ahocorasick
class QuestionClassifier:
    def __init__(self, config):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 特征词路径
        self.technology_path = os.path.join(cur_dir, 'dict/Technology.txt')  # 技术名称
        self.province_path = os.path.join(cur_dir, 'dict/Province.txt')  # 省份
        self.keyword_path = os.path.join(cur_dir, 'dict/Keyword.txt')  # 关键词
        self.result_path = os.path.join(cur_dir, 'dict/Result.txt')  # 成果
        self.unit_path = os.path.join(cur_dir, 'dict/Unit.txt')  # 单位
        self.industry_path = os.path.join(cur_dir, 'dict/Industry.txt')  # 行业
        self.category_path = os.path.join(cur_dir, 'dict/Category.txt')  # 领域分类
        # 加载特征词
        self.technology_wds = [i.strip() for i in open(self.technology_path, encoding='utf-8') if i.strip()]
        self.province_wds = [i.strip() for i in open(self.province_path, encoding='utf-8') if i.strip()]
        self.keyword_wds = [i.strip() for i in open(self.keyword_path, encoding='utf-8') if i.strip()]
        self.result_wds = [i.strip() for i in open(self.result_path, encoding='utf-8') if i.strip()]
        self.unit_wds = [i.strip() for i in open(self.unit_path, encoding='utf-8') if i.strip()]
        self.industry_wds = [i.strip() for i in open(self.industry_path, encoding='utf-8') if i.strip()]
        self.category_wds = [i.strip() for i in open(self.category_path, encoding='utf-8') if i.strip()]
        # 属性词融合
        self.region_words = set(self.technology_wds + self.province_wds + self.keyword_wds +
                                self.result_wds + self.unit_wds + self.industry_wds +
                                self.category_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.brief_info_qwds = config['brief_info_qwds']
        self.result_time_qwds = config['result_time_qwds']
        self.result_category_qwds = config['result_category_qwds']
        self.result_place_qwds = config['result_place_qwds']
        self.result_keyword_qwds = config['result_keyword_qwds']
        self.result_applied_qwds = config['result_applied_qwds']
        self.result_unit_qwds = config['result_unit_qwds']
        self.result_related_qwds = config['result_related_qwds']
        self.unit_results_qwds = config['unit_results_qwds']
        self.province_results_qwds = config['province_results_qwds']
        self.industry_results_qwds = config['industry_results_qwds']
        self.keyword_results_qwds = config['keyword_results_qwds']
        self.category_results_qwds = config['category_results_qwds']
        self.result_info_qwds = config['result_info_qwds']
        self.positive_qwds = config['positive_qwds']
        self.negative_qwds = config['negative_qwds']
        self.unit_address_qwds = config['unit_address_qwds']
        self.post_code_qwds = config['post_code_qwds']
        self.keyword_search_qwds = config['keyword_search_qwds']
        self.statistic_qwds = config['statistic_qwds']
        self.division = config['division']
        self.tmp_dict_buff = {}
    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.technology_wds:
                wd_dict[wd].append('technology')
            if wd in self.province_wds:
                wd_dict[wd].append('province')
            if wd in self.keyword_wds:
                wd_dict[wd].append('keyword')
            if wd in self.result_wds:
                wd_dict[wd].append('result')
            if wd in self.unit_wds:
                wd_dict[wd].append('unit')
            if wd in self.industry_wds:
                wd_dict[wd].append('industry')
            if wd in self.category_wds:
                wd_dict[wd].append('category')
        return wd_dict
    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree
    '''问句过滤'''
    def check_tech(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        return final_dict
    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False
    '''分类主函数'''
    def classify(self, question):
        data = {}
        tech_dict = self.check_tech(question)
        if not tech_dict:
            return {}
        data['args'] = tech_dict
        self.tmp_dict_buff = tech_dict
        types = []
        for type_ in tech_dict.values():
            types += type_
        question_type = 'others'
        question_types = []
        if self.check_words(self.brief_info_qwds, question) and ('result' in types):
            question_type = 'result_brief'
            question_types.append(question_type)
        if self.check_words(self.result_time_qwds, question) and ('result' in types):
            question_type = 'result_time'
            question_types.append(question_type)
        if self.check_words(self.result_category_qwds, question) and ('result' in types):
            question_type = 'result_category'
            question_types.append(question_type)
        if self.check_words(self.result_place_qwds, question) and ('result' in types):
            question_type = '_placeresult'
            question_types.append(question_type)
        if self.check_words(self.result_keyword_qwds, question) and ('result' in types):
            question_type = 'result_keywords'
            question_types.append(question_type)
        if self.check_words(self.result_applied_qwds, question) and ('result' in types):
            question_type = 'result_applied'
            question_types.append(question_type)
        if self.check_words(self.result_unit_qwds, question) and ('result' in types):
            question_type = 'result_unit'
            question_types.append(question_type)
        if self.check_words(self.result_related_qwds, question) and ('result' in types):
            question_type = 'result_related'
            question_types.append(question_type)
        if self.check_words(self.unit_results_qwds, question) and ('unit' in types):
            question_type = 'unit_results'
            question_types.append(question_type)
        if self.check_words(self.province_results_qwds, question) and ('province' in types):
            question_type = 'province_results'
            question_types.append(question_type)
        if self.check_words(self.industry_results_qwds, question) and ('industry' in types):
            question_type = 'industry_results'
            question_types.append(question_type)
        if self.check_words(self.keyword_results_qwds, question) and ('keyword' in types):
            question_type = 'keyword_results'
            question_types.append(question_type)
        if self.check_words(self.category_results_qwds, question) and ('category' in types):
            question_type = 'category_results'
            question_types.append(question_type)
        if self.check_words(self.result_info_qwds, question) and ('result' in types):
            question_type = 'result_detail'
            question_types.append(question_type)
        if self.check_words(self.unit_address_qwds, question) and ('unit' in types):
            question_type = 'unit_address'
            question_types.append(question_type)
        if self.check_words(self.post_code_qwds, question) and ('unit' in types):
            question_type = 'post_code'
            question_types.append(question_type)
        if self.check_words(self.keyword_search_qwds, question) and ('keyword' in types):
            question_type = 'keyword_search'
            question_types.append(question_type)
        if self.check_words(self.statistic_qwds, question) and ('category' in types):
            question_type = 'statistic'
            question_types.append(question_type)
        if self.check_words(self.positive_qwds + self.negative_qwds, question):
            if 'result' in types and 'unit' in types:
                question_type = 'result_unit_judge'
                question_types.append(question_type)
            elif 'result' in types and 'province' in types:
                question_type = 'result_province_judge'
                question_types.append(question_type)
            elif 'result' in types and 'industry' in types:
                question_type = 'result_industry_judge'
                question_types.append(question_type)
            elif 'result' in types and 'keyword' in types:
                question_type = 'result_keyword_judge'
                question_types.append(question_type)
            elif 'result' in types and 'category' in types:
                question_type = 'result_category_judge'
                question_types.append(question_type)
        data['question_types'] = question_types
        return data