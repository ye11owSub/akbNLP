from flask import Flask, request, json, render_template
from answerSearch import bot_answer
from config import *
import vk

app = Flask(__name__)


def text_for_vk(matrix):
    text = "Результаты поиска\n\n"
    for row in matrix:
        text += "Расстояние: {0}\nСхожий вопрос: {1}\n Ответ: {2}".format(*row) + "\n\n"
    return text


@app.route('/')
def page():
    from answerSearch import bot_answer
    question = request.args.get("question")
    try:
        count = int(request.args.get("count"))
        answers = bot_answer(question, count)
    except:
        if question is None:
            return render_template("info.html")
        answers = bot_answer(question)
    return render_template("answer.html", answers=answers)


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data.decode('utf8'))
    print(data)
    if data["secret"] != secret_key:
        return 'not vk'
    elif data['type'] == 'confirmation':
        return confirm_key
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v=5.0)
        user_id = data['object']['user_id']
        message = data['object']['body']
        answer = bot_answer(message)
        api.messages.send(access_token=token, user_id=str(user_id), message=text_for_vk(answer))
        return "ok"


if __name__ == '__main__':
    app.run()
