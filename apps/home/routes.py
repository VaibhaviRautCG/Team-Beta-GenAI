from flask import render_template
import traceback
from apps.home import blueprint
from apps.home.forms import  ChatForm
import openai
import os
from apps.config import Config

openai.api_key = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

@blueprint.route('/',methods=['GET','POST'])
def index():
    # return "Hello, Flask! This is the first dummy page."
    return render_template('home/index.html')


@blueprint.route('/chatbot',methods=['GET', 'POST'])
def chatbot():
    form = ChatForm()
    chat_history = []

    if request.method == 'POST':
        
        user_message = form.message.data
        chat_history = session.get('chat_history', [])
        chat_history.append({"role": "user", "content": user_message})
        
        try:
            return render_template('home/chatbot.html', segment='chatbot')
        except Exception as err:
            print("Exception or Error at Chatbot page: ",err)
            traceback.print_exc()


@blueprint.route('/simple_chatbot',methods=['GET', 'POST'])
def simple_chatbot():
    form = ChatForm()
    chat_history = []

    if request.method == 'POST' and form.validate_on_submit():
        user_message = form.user_message.data
        try:
            bot_response = generate_response(user_message)
            return render_template(
                "home/simple_chatbot.html",
                segment='simple_chatbot',
                form=form,
                bot_response=bot_response
            )
        except Exception as err:
            print("An Error has occurred! Error: ", err)
            traceback.print_exc()
    
    return render_template("home/simple_chatbot.html",segment='simple_chatbot', form=form, bot_response=None)

def generate_response(user_message):
    prompt = f"User: {user_message}\nBot:"
    response = openai.Completion.create(
        engine="text-davinci-002",  # Change to the desired GPT-3 engine
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response.choices[0].text.strip()