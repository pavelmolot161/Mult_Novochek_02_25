
from flask import Flask, render_template, request, jsonify
from flasgger import Swagger
import logging

app = Flask(__name__)
swagger = Swagger(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)  # Уровень логирования
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    logger.info("User accessed the home page.")
    return render_template('index.html')

@app.route('/call/<phone>', methods=['POST'])
def make_call(phone):
    try:
        # Логика для совершения звонка
        logger.info(f"User made a call to {phone}.")
        return jsonify({"message": f"Calling {phone}..."}), 200
    except Exception as e:
        logger.error(f"Error making a call to {phone}: {str(e)}")
        return jsonify({"error": "Failed to make a call."}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        # Логика для входа пользователя
        username = request.json.get('username')
        password = request.json.get('password')
        logger.info(f"User {username} logged in.")
        return jsonify({"message": "Logged in successfully."}), 200
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "Login failed."}), 500

@app.route('/logout', methods=['POST'])
def logout():
    try:
        # Логика для выхода пользователя
        logger.info("User logged out.")
        return jsonify({"message": "Logged out successfully."}), 200
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({"error": "Logout failed."}), 500

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True) ### - Для доступа телефона







# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# def home():
#     return render_template('index.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)
