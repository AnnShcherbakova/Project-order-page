import smtplib#Импортируем необходимые модули для отправки электронной почты через SMTP сервер
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, from_email, to_email, message):# Определением функцию для отправки электронных писем
    # Параметры для подключения к SMTP серверу Gmail
    smtp_host = 'smtp.gmail.com'# Адрес SMTP сервера Gmail
    smtp_port = 587# Порт для шифрованного соединения
    smtp_username = ''  # Адрес электронной почты
    smtp_password = ''

    msg = MIMEMultipart()# Создаем объект MIMEMultipart для формирования письма #Затем устанавливаем параметры письма: адрес
    # отправителя, адрес получателя, тема и добавляется текстовая часть сообщения.
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))#Добавляем текст сообщения в письмо

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server: # Создаем объекта SMTP
            server.starttls()
            server.login(smtp_username, smtp_password) # Аутентификация на SMTP сервере с использованием адреса и пароля
            server.sendmail(from_email, to_email, msg.as_string())# Отправка письма, указывая отправителя, получателя и текст письма
            print("Письмо успешно отправлено!")
    except Exception as e:
        print("Ошибка отправки письма:", e)
