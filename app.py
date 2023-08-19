from flask import Flask, render_template, request
from celery import Celery
from email_utils import send_email # Импортируем функцию send_email из внешнего модуля email_utils, она используется
# для отправки электронных сообщений

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0' #Задаем настройки для Celery, указывая URL-адреса брокера и бэкенда
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])#Создаем экземпляр Celery-приложения.
# Передаем ему имя текущего Flask-приложения
# app.name и настройки, определенные выше.
celery.conf.update(app.config)


@app.route('/') # Определяем маршрут "/" для отображения шаблона order_form.html
def index():
    return render_template('order_form.html')


@app.route('/order', methods=['POST'])# Определяем маршрут "/order" для обработки POST-запросов
def order():
    order_data = { # Извлекаем данные из формы POST-запроса
        'name': request.form['name'],
        'email': request.form['email'],
        'details': request.form['details']
    }
    send_order_confirmation_email.delay(order_data)# Запуск асинхронной задачи send_order_confirmation_email
    send_email("Подтверждение заказа", "annannfffa@gmail.com", order_data['email'], # Отправка подтверждения заказа на почту
               f"Уважаемый(ая) {order_data['name']}, ваш заказ подтвержден.")
    return 'Заказ принят!'


@celery.task
def send_order_confirmation_email(order_data):#Определяем асинхронную задачу send_order_confirmation_email,
#которая отправляет письмо с подтверждением заказа.
    subject = 'Подтверждение заказа'
    from_email = 'annannfffa@gmail.com'
    to_email = order_data['email']
    message = f"Уважаемый(ая) {order_data['name']}, ваш заказ подтвержден."

    send_email(subject, from_email, to_email, message)


if __name__ == "__main__":# Запуск Flask-приложения
    app.run(debug=True)
