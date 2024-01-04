
from flask import render_template, request
import traceback
from apps.home import blueprint
from apps.home.chat.chat import ChatMessage
from apps.home.forms import  ChatForm
import openai
import os
from werkzeug.utils import secure_filename
from apps.config import Config
from apps import db
from flask_wtf.file import FileAllowed

# region Computer Vision
# from PIL import Image
# import pytesseract

import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
# from azure.cognitiveservices.vision.computervision import TextOperationStatusCodes
# from azure.core.polling import TextOperationStatusCodes


subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]

# print("\nTEST: Engpoint: ", endpoint, "\t key: ", subscription_key)
credentials = CognitiveServicesCredentials(subscription_key)
computervision_client = ComputerVisionClient(endpoint, credentials)
# endregion

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

    # if request.method == 'POST':
        
        # user_message = form.message.data
        # chat_history = session.get('chat_history', [])
        # chat_history.append({"role": "user", "content": user_message})
        
    try:
        return render_template('home/chatbot.html', segment='chatbot')
    except Exception as err:
        print("Exception or Error at Chatbot page: ",err)
        traceback.print_exc()



@blueprint.route('/simple_chatbot',methods=['GET', 'POST'])
def simple_chatbot():
    form = ChatForm()
    chat_history = []
    bot_response=''

    allowed_extensions = get_allowed_extensions(form.image)

    if request.method == 'POST':
        if "submit" in request.form:

            print("\nTEST: Entire form Data: ",form.data)

            user_message = form.user_message.data

            # region Image Processing 
            image_file = request.files["image"]

            # if image_file.filename == "":
            #     return "No selected file"

            # Save the uploaded image
            # file_path = f'C:/Users/vaibraut/OneDrive - Capgemini/Documents/My Learning/Team Beta GenAI Hackathon/Team-Beta-GenAI/apps/home/images'
            # image_path = f"{file_path}/" + image_file.filename
            # image_file.save(image_path)

            # Extract text using Azure Computer Vision
            # text = extract_text_from_image(image_path)

            # print("\nTEST: Extracted Text from Image: ", text)
            # endregion

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

# def extract_text_from_image(image_path):
#     # Open the image using PIL (Python Imaging Library)
#     img = Image.open(image_path)

#     # Use pytesseract to extract text from the image
#     text = pytesseract.image_to_string(img)

#     return text.strip()

def extract_text_from_image(image_path):
    computervision_client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(subscription_key)
    )

    with open(image_path, "rb") as image_stream:
        result = computervision_client.recognize_printed_text_in_stream(image_stream)

    operation_location = result.headers["Operation-Location"]

    operation_id = operation_location.split("/")[-1]

    while True:
        get_operation_result = computervision_client.get_operation_status(operation_id)

        if get_operation_result.status not in [OperationStatusCodes.RUNNING, OperationStatusCodes.NOT_STARTED]:
            break

    if get_operation_result.status == OperationStatusCodes.SUCCEEDED:
        text = ""
        for region in get_operation_result.recognition_results:
            for line in region.lines:
                text += line.text + " "
        return text.strip()

    return "Text extraction failed"


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


# probably not working
def get_allowed_extensions(form_field):
    for validator in form_field.validators:
        if isinstance(validator, FileAllowed):
            return validator.upload_set
    return []
