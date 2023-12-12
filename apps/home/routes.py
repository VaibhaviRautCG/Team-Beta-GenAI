from flask import render_template
import traceback

from apps.home import blueprint

@blueprint.route('/',methods=['GET','POST'])
def index():
    # return "Hello, Flask! This is the first dummy page."
    return render_template('home/index.html')


@blueprint.route('/chatbot',methods=['GET', 'POST'])
def chatbot():
    try:
        return render_template('home/chatbot.html', segment='chatbot')
    except Exception as err:
        print("Exception or Error at Chatbot page: ",err)
        traceback.print_exc()