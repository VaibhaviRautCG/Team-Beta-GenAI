from flask import Flask, render_template, request, jsonify
from .simple_chatbot import get_response  # Import your chatbot function


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['user_message']
    bot_response = get_response(user_message)
    return jsonify({'bot_response': bot_response})

# simple_chatbot.py

def get_response(user_input):
    # Your chatbot logic here
    return "Bot's response"


if __name__ == '__main__':
    app.run(debug=True)
