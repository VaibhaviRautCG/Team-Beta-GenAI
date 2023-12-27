from flask import render_template, redirect, request, url_for
import traceback
from apps.home import blueprint
from apps.home.chat.chat import ChatMessage
from apps.home.forms import  ChatForm
import openai
import os
from apps.config import Config
from apps import db

# from apps.api.cv_image_txt.txtAnalyser import image_to_text

openai.api_key = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# region image vision
# import azure.ai.vision as sdk
# service_options = sdk.VisionServiceOptions(os.environ["VISION_ENDPOINT"],
#                                         os.environ["VISION_KEY"])

# Image URL
# vision_source = sdk.VisionSource(
#     url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fkinsta.com%2Fblog%2F500-internal-server-error%2F&psig=AOvVaw0Bza2dyW7c-rDfkKq_a54A&ust=1703239008591000&source=images&cd=vfe&opi=89978449&ved=0CBAQjRxqFwoTCLj4xvShoIMDFQAAAAAdAAAAABAD"
# )
# url="https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png")

# Image File
# vision_source = sdk.VisionSource(filename="sample.jpg")

# analysis_options = sdk.ImageAnalysisOptions()

# analysis_options.features = (
#     sdk.ImageAnalysisFeature.CROP_SUGGESTIONS |
#     sdk.ImageAnalysisFeature.CAPTION |
#     sdk.ImageAnalysisFeature.DENSE_CAPTIONS |
#     sdk.ImageAnalysisFeature.OBJECTS |
#     sdk.ImageAnalysisFeature.PEOPLE |
#     sdk.ImageAnalysisFeature.TEXT |
#     sdk.ImageAnalysisFeature.TAGS
# )

# analysis_options.language = "en"
# analysis_options.gender_neutral_caption = True
# analysis_options.cropping_aspect_ratios = [0.9, 1.33]

# endregion


@blueprint.route('/',methods=['GET','POST'])
def index():
    # return "Hello, Flask! This is the first dummy page."
    return render_template('home/index.html')


@blueprint.route('/chatbot',methods=['GET', 'POST'])
def chatbot():
    form = ChatForm()
    chat_history = []

    # if request.method == 'POST':
        
        # user_message = form.message.data
        # chat_history = session.get('chat_history', [])
        # chat_history.append({"role": "user", "content": user_message})
        
    try:
        return render_template('home/chatbot.html', segment='chatbot')
    except Exception as err:
        print("Exception or Error at Chatbot page: ",err)
        traceback.print_exc()


# @blueprint.route('/simple_chatbot',methods=['GET', 'POST'])
# def simple_chatbot():
#     form = ChatForm()
#     chat_history = []
#     bot_response=''

#     if "submit" in request.form and request.method == 'POST':
#         user_message = form.user_message.data
#         # img_txt_res = image_to_text(service_options, vision_source, analysis_options)
#         # print("\nTEST: img_txt_res: ", img_txt_res)
#         bot_response = generate_response(user_message)
#         print("\nTEST: Bot_response: ", bot_response)

#         chat_message = ChatMessage(user_message=user_message, bot_response=bot_response)
#         db.session.add(chat_message)
#         db.session.commit()

#         form.user_message.data = ""

#     chat_history = get_chat_history()
#     return render_template(
#         "home/simple_chatbot.html",
#         segment='simple_chatbot',
#         form=form,
#         bot_response=bot_response,
#         chat_history=chat_history
#     )



@blueprint.route('/simple_chatbot',methods=['GET', 'POST'])
def simple_chatbot():
    form = ChatForm()
    chat_history = []
    bot_response=''

    if request.method == 'POST':
        if "submit" in request.form:
            user_message = form.user_message.data
            # img_txt_res = image_to_text(service_options, vision_source, analysis_options)
            # print("\nTEST: img_txt_res: ", img_txt_res)
            bot_response = generate_response(user_message,Config.OPENAI_GPT_ENGINE)
            print("\nTEST: Bot_response: ", bot_response)

            chat_message = ChatMessage(user_message=user_message, bot_response=bot_response)
            db.session.add(chat_message)
            db.session.commit()

            form.user_message.data = ""

        # elif "clearBtn" in request.form:
        elif form.clear.data: 
            # Clear chat history from the database
            ChatMessage.query.delete()
            db.session.commit()

    chat_history = get_chat_history()
    return render_template(
        "home/simple_chatbot.html",
        segment='simple_chatbot',
        form=form,
        bot_response=bot_response,
        chat_history=chat_history
    )



def generate_response(user_message, engine):
    print(f"User Message: {user_message}")
    prompt = f"User: {user_message}\nBot:"
    response = openai.Completion.create(
        engine=engine,  # Change to the desired GPT-3 engine
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response.choices[0].text.strip()


def get_chat_history():
    # Retrieve chat history from the database
    return ChatMessage.query.order_by(ChatMessage.timestamp).all()








# @blueprint.route('/imageTxt', methods=['POST'])
# def upload():
#     if 'image' not in request.files:
#         return redirect(url_for('index'))

#     image_file = request.files['image']
#     if image_file.filename == '':
#         return redirect(url_for('index'))

#     # Read the uploaded image
#     image_data = image_file.read()

#     # Analyze the image using Azure Computer Vision
#     results = computervision_client.analyze_image_in_stream(image_data, visual_features=['Categories', 'Description'])

#     # Extract relevant information from the results
#     description = results.description.captions[0].text

#     return render_template('result.html', description=description)