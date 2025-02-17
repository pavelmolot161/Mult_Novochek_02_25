
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
    logger.info("User accessed the home page. (Пользователь получил доступ к домашней странице)")
    return render_template('index.html')

@app.route('/call/<phone>', methods=['POST'])
def make_call(phone):
    """
    Совершить звонок
    ---
    parameters:
      - name: phone
        in: path
        type: string
        required: true
        description: Номер телефона для звонка
    responses:
      200:
        description: Успешный вызов
      500:
        description: Ошибка при вызове
    """
    try:
        # Логика для совершения звонка
        logger.info(f"User made a call to (Пользователь позвонил.){phone}.")
        return jsonify({"message": f"Calling (Вызов.){phone}..."}), 200
    except Exception as e:
        logger.error(f"Error making a call to (Ошибка вызова при звонке.){phone}: {str(e)}")
        return jsonify({"error": "Failed to make a call. (Не удалось позвонить.)"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        # Логика для входа пользователя
        username = request.json.get('username')
        password = request.json.get('password')
        logger.info(f"User {username} logged in.")
        return jsonify({"message": "Logged in successfully. (Вписался успешно.)"}), 200
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "Login failed. (Ошибка входа.)"}), 500

@app.route('/logout', methods=['POST'])
def logout():
    try:
        # Логика для выхода пользователя
        logger.info("User logged out.")
        return jsonify({"message": "Logged out successfully. (Зарегистрировано успешно.)"}), 200
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({"error": "Logout failed. (Выход не удался)"}), 500

if __name__ == '__main__':
    # app.run(debug=True)           ### - ???
    # app.run(host='0.0.0.0', port=5000, debug=True) ### - Для доступа телефона в целях настройки
    # app.run(host='0.0.0.0', port=443) ### - внесения изменений так как на этом порту находятся домены
    app.run(host='127.0.0.1', port=8080) ### - внесения изменений для работы через Nginx











### - Работает и выгружено на хостинг до 11.00 16.02.25

# from flask import Flask, render_template, request, jsonify
# from flasgger import Swagger
# import logging
#
# app = Flask(__name__)
# swagger = Swagger(app)
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO)  # Уровень логирования
# logger = logging.getLogger(__name__)
#
# @app.route('/')
# def home():
#     logger.info("User accessed the home page. (Пользователь получил доступ к домашней странице)")
#     return render_template('index.html')
#
# @app.route('/call/<phone>', methods=['POST'])
# def make_call(phone):
#     """
#     Совершить звонок
#     ---
#     parameters:
#       - name: phone
#         in: path
#         type: string
#         required: true
#         description: Номер телефона для звонка
#     responses:
#       200:
#         description: Успешный вызов
#       500:
#         description: Ошибка при вызове
#     """
#     try:
#         # Логика для совершения звонка
#         logger.info(f"User made a call to (Пользователь позвонил.){phone}.")
#         return jsonify({"message": f"Calling (Вызов.){phone}..."}), 200
#     except Exception as e:
#         logger.error(f"Error making a call to (Ошибка вызова при звонке.){phone}: {str(e)}")
#         return jsonify({"error": "Failed to make a call. (Не удалось позвонить.)"}), 500
#
# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         # Логика для входа пользователя
#         username = request.json.get('username')
#         password = request.json.get('password')
#         logger.info(f"User {username} logged in.")
#         return jsonify({"message": "Logged in successfully. (Вписался успешно.)"}), 200
#     except Exception as e:
#         logger.error(f"Login error: {str(e)}")
#         return jsonify({"error": "Login failed. (Ошибка входа.)"}), 500
#
# @app.route('/logout', methods=['POST'])
# def logout():
#     try:
#         # Логика для выхода пользователя
#         logger.info("User logged out.")
#         return jsonify({"message": "Logged out successfully. (Зарегистрировано успешно.)"}), 200
#     except Exception as e:
#         logger.error(f"Logout error: {str(e)}")
#         return jsonify({"error": "Logout failed. (Выход не удался)"}), 500
#
# if __name__ == '__main__':
#     # app.run(debug=True)           ### - ???
#     app.run(host='0.0.0.0', port=5000, debug=True) ### - Для доступа телефона в целях настройки




