from flask import Flask, request, jsonify
from flask_cors import CORS
from question_classifier import QuestionClassifier
from question_parser import QuestionPaser
from answer_searcher import AnswerSearcher
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, QUESTION_CLASSIFICATION_CONFIG

app = Flask(__name__)
CORS(app)  # 添加 CORS 支持

# 初始化问答系统组件
classifier = QuestionClassifier(config=QUESTION_CLASSIFICATION_CONFIG)
parser = QuestionPaser()
searcher = AnswerSearcher(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)


def process_message(user_message):
    """处理用户消息并返回响应"""
    # 调用问题分类器
    res_classify = classifier.classify(user_message)

    # 调用问句解析器
    sqls = parser.parser_main(res_classify)

    # 调用答案搜索器
    answers = searcher.search_main(sqls)

    # 如果有多个答案，只取第一个
    if answers:
        return answers[0]
    else:
        return "未找到相关信息。"


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"response": "请输入有效消息"}), 400

        # 处理用户消息并生成响应
        bot_response = process_message(user_message)

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"response": "服务器出现错误，请稍后再试"}), 500


if __name__ == '__main__':
    app.run(debug=True)