import base64
from flask import render_template, redirect, request, url_for
import traceback
from apps.api.cv_image_txt.txtAnalyser import extract_text_from_image
from apps.home import blueprint
from apps.home.chat.chat import ChatMessage
from apps.home.forms import  ChatForm
import openai
import os
from werkzeug.utils import secure_filename
from apps.config import Config
from apps import db
from flask_wtf.file import FileAllowed

# from apps.api.cv_image_txt.txtAnalyser import image_to_text

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

            image = form.image.data
            print("\nTEST: image data from form: ", image)
            file = request.files['image']

            # If the user does not select a file, the browser submits an empty file without a filename
            if file.filename == '':
                return render_template('index.html', error='No selected file')

            # Check if the file is allowed based on the file extension (you can extend this check)
            allowed_extensions = {'png', 'jpg', 'jpeg'}
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                return render_template('index.html', error='Invalid file type. Please upload an image.')
            
            # Read the image data
            

            # Extract text from the image
            extracted_text = extract_text_from_image(file)

            # Check if a file is selected before accessing its attributes
            # if image:
            #     filename = secure_filename(image.filename)
            #     file_path = f'C:/Users/vaibraut/OneDrive - Capgemini/Documents/My Learning/Team Beta GenAI Hackathon/Team-Beta-GenAI/apps/home/images'
            #     image.save(file_path + f'/{filename}')
            #     print(f'Success! Image "{filename}" uploaded and processed.')
            # else:
            #     print('No file selected.')
            
            # if image:
            #     img_data = form.image.data.read()
            #     base64_encoded_image = base64.b64encode(img_data).decode('utf-8')
            #     print("\nTEST: img_data: ", img_data)
            #     img_result = read_txt_from_img(base64_encoded_image)    
            #     print("\nTEST: image Text: ", img_result)
            
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


# probably not working
def get_allowed_extensions(form_field):
    for validator in form_field.validators:
        if isinstance(validator, FileAllowed):
            return validator.upload_set
    return []
