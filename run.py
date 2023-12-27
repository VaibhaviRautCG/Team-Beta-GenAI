from apps import create_app
import os
from apps import db

app = create_app()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

if __name__ == '__main__':
    # print(f"Current Working Directory: {os.getcwd()}")
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
