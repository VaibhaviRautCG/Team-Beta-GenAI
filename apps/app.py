from flask import Flask, render_template, request, jsonify
from simple_chatbot import get_response  # Import your chatbot function

app = Flask(__name__)

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
