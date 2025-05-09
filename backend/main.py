from question_classifier import QuestionClassifier
from question_parser import QuestionPaser
from answer_searcher import AnswerSearcher
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, QUESTION_CLASSIFICATION_CONFIG
if __name__ == '__main__':
    # 初始化各个组件
    classifier = QuestionClassifier(config=QUESTION_CLASSIFICATION_CONFIG)
    parser = QuestionPaser()
    searcher = AnswerSearcher(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    print("欢迎使用中国先进技术问答系统！")
    print("请输入您的问题，或输入'退出'结束程序。")
    while True:
        question = input("\n您：")
        if question == "退出":
            print("感谢使用！再见！")
            break
        # 问题分类
        res_classify = classifier.classify(question)
        print(f"识别的问句类型：{res_classify['question_types']}")
        if not res_classify:
            print("系统：抱歉，我无法理解您的问题。")
            continue
        # 问句解析
        sqls = parser.parser_main(res_classify)
        if not sqls:
            print("系统：抱歉，我无法理解您的问题。")
            continue
        # 组合功能
        answers = searcher.search_main(sqls)
        if not answers:
            print("系统：抱歉，未找到相关信息。")
        else:
            print("系统：", answers[0])  # 这里简化处理，只返回第一个答案，实际应用中可根据需要调整