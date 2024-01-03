from apps import create_app
import os
import sys
sys.dont_write_bytecode = True

app = create_app()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

if __name__ == '__main__':
    app.run(debug=True)
