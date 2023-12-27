from flask import jsonify, render_template, request
from apps import create_app
from apps.simple_chatbot import get_response  # Import your chatbot function
import os

app = create_app()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    # Assuming that the incoming data is in JSON format
    data = request.json
    
    # Extract the user's message from the JSON payload
    user_message = data['user_message']
    
    # Pass the user's message to the chatbot function to get a response
    bot_response = get_response(user_message)
    
    # Optionally, you can save the conversation history or perform additional processing
    
    # Return the chatbot's response in JSON format
    return jsonify({'bot_response': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
