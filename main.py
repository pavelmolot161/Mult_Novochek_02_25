
from flask import Flask, render_template, request, jsonify
from config import Config
from models import db, RentalItem
from flasgger import Swagger
import logging

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
swagger = Swagger(app)

with app.app_context():
    db.create_all()  # Создаёт таблицы в базе данных

# Настройка логирования
logging.basicConfig(level=logging.INFO)  # Уровень логирования
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    logger.info("User accessed the home page. (Пользователь получил доступ к домашней странице)")

    # Получаем все элементы из базы данных
    items = RentalItem.query.all()  # Получаем все записи из таблицы RentalItem

    # Извлекаем все элементы из базы данных
    item1 = RentalItem.query.get(1)  # Манипулятор
    item2 = RentalItem.query.get(2)  # Мини экскаватор
    item3 = RentalItem.query.get(3)  # Эвакуатор
    item4 = RentalItem.query.get(4)  # Мини самосвал
    item5 = RentalItem.query.get(5)  # Каток

    # Передаем элементы в шаблон
    return render_template('index.html', item1=item1, item2=item2, item3=item3, item4=item4, item5=item5)  # Передаем список элементов в шаблон

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

###________________________________________________________________________________________________________

@app.route('/update_price', methods=['POST'])
def update_price():
    """
    Обновить цену
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Название объекта
            new_price:
              type: integer
              description: Новая цена
    responses:
      200:
        description: Успешное обновление цены
      400:
        description: Ошибка в запросе
      404:
        description: Объект не найден
      500:
        description: Ошибка при обновлении цены
    """
    try:
        data = request.json  # Получаем данные из запроса
        title = data.get('title')  # Получаем название объекта
        new_price = data.get('new_price')  # Получаем новую цену

        # Проверка на наличие данных
        if title is None or new_price is None:
            return jsonify({"error": "Title and new_price are required. (Название и новая цена требуются)"}), 400

        # Проверка типа new_price
        if not isinstance(new_price, int):
            return jsonify({"error": "new_price must be an integer. (Новая цена должна быть целым числом)"}), 400

        # Находим объект в базе данных
        item = RentalItem.query.filter_by(title=title).first()
        if item is None:
            return jsonify({"error": "Item not found. (Пункт не найден)"}), 404

        # Обновляем цену
        item.price = new_price
        db.session.commit()  # Сохраняем изменения в базе данных

        logger.info(f"Price for {title} updated to {new_price}.")
        return jsonify({"message": f"Price for {title} updated to {new_price}."}), 200
    except Exception as e:
        logger.error(f"Error updating price (Ошибка обновления цены): {str(e)}")
        return jsonify({"error": f"Failed to update price: {str(e)} (Не удалось обновить цену: {str(e)})"}), 500

@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        data = request.json
        title = data.get('title')
        price = data.get('price')

        if title is None or price is None:
            return jsonify({"error": "Title and price are required. (Название и цена требуются 2)"}), 400

        new_item = RentalItem(title=title, price=price)
        db.session.add(new_item)
        db.session.commit()

        return jsonify({"message": "Item added successfully. (Пункт добавлен успешно 2)"}), 201
    except Exception as e:
        logger.error(f"Error adding item (Ошибка добавления элемента 2): {str(e)}")
        return jsonify({"error": "Failed to add item. (Не удалось добавить элемент 2)"}), 500

@app.route('/update_text', methods=['POST'])
def update_text():
    """
    Обновить текст
    ---
    parameters:
      - name: section
        in: body
        type: string
        required: true
        description: Секция для обновления (например, 'footer', 'right_side')
      - name: new_text
        in: body
        type: string
        required: true
        description: Новый текст
    responses:
      200:
        description: Успешное обновление текста
      500:
        description: Ошибка при обновлении текста
    """
    try:
        data = request.json
        section = data.get('section')
        new_text = data.get('new_text')
        # Логика для обновления текста в соответствующей секции
        logger.info(f"Text in {section} updated to: {new_text}.")
        return jsonify({"message": f"Text in {section} updated to: {new_text}."}), 200
    except Exception as e:
        logger.error(f"Error updating text: {str(e)}")
        return jsonify({"error": "Failed to update text."}), 500

###____     ДОБАВЛЕНИЕ ДАННЫХ В БАЗУ ДАННЫХ это необходимость     _________________________________________
"""После каждого запуска приложения создается новый комплект записей сейчас их там уже два комплекта"""

# Создаем контекст приложения
# with app.app_context():
#
#     # Создаем новую запись
#     new_item1 = RentalItem(title='Манипулятор', price=3000)
#     new_item2 = RentalItem(title='Мини экскаватор', price=2500)
#     new_item3 = RentalItem(title='Эвакуатор', price=3500)
#     new_item4 = RentalItem(title='Мини самосвал', price=3000)
#     new_item5 = RentalItem(title='Каток', price=2250)
#
#     # Добавляем запись в сессию и сохраняем изменения
#     db.session.add(new_item1)
#     db.session.add(new_item2)
#     db.session.add(new_item3)
#     db.session.add(new_item4)
#     db.session.add(new_item5)
#
#     db.session.commit()

###________________________________________________________________________________________________________

@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Удалить элемент по ID
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID элемента для удаления
    responses:
      200:
        description: Успешное удаление элемента
      404:
        description: Элемент не найден
    """
    try:
        # Находим элемент по ID
        item = RentalItem.query.get(item_id)
        if item is None:
            return jsonify({"error": "Item not found. (Пункт не найден)"}), 404

        # Удаляем элемент
        db.session.delete(item)
        db.session.commit()  # Сохраняем изменения в базе данных

        return jsonify({"message": f"Item {item_id} deleted successfully. (Объект удален успешно)"}), 200
    except Exception as e:
        logger.error(f"Error deleting item (Ошибка удаления элемента): {str(e)}")
        return jsonify({"error": "Failed to delete item. (Не удалось удалить элемент)"}), 500

#____________________________________________________________________________________________________________________

@app.route('/delete_items', methods=['POST'])
def delete_items():
    """
    Удалить несколько элементов по списку ID
    ---
    parameters:
      - name: item_ids
        in: body
        type: array
        items:
          type: integer
        required: true
        description: Список ID элементов для удаления
    responses:
      200:
        description: Успешное удаление элементов
      404:
        description: Один или несколько элементов не найдены
    """
    try:
        data = request.json
        item_ids = data.get('item_ids', [])

        for item_id in item_ids:
            item = RentalItem.query.get(item_id)
            if item:
                db.session.delete(item)

        db.session.commit()  # Сохраняем изменения в базе данных

        return jsonify({"message": "Items deleted successfully. (Предметы успешно удалены 2) "}), 200
    except Exception as e:
        logger.error(f"Error deleting items (Ошибка удаления элементов 2): {str(e)}")
        return jsonify({"error": "Failed to delete items. (Не удалось удалить элементы 2)"}), 500

#____________________________________________________________________________________________________________________



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




