# Уведомления от sendpulse

Напоминалка, когда кончается пакет в Sendpulse на SMTP. <br>
Уведомления приходят в Telegram

Для работы необходимо: 
- настроить venv окружение `python3 -m venv venv`
- установить все пакеты из requirements.txt <br>
-- Linux<br>
`source venv/bin/activate` && `pip install -r requirements.txt`<br>
-- Windows<br>
`cd venv/Scripts/ && activate.bat` && `pip install -r requirements.txt`
- прописать данные в database.db:
  - client_id - ID клиента sendpulse
  - client_secret - Secret клиента sendpulse
  - TG_TOKEN - Токен телеграм бота
  - CHAT_ID - Чат куда будут приходить уведомления
  - EXCEPTION_CHAT_ID - Чат куда будут приходить технические сообщения<br>
- настроить crontab<br><br>
 `(*/30 * * * * cd /var/www/smtp_sendpulse_bot;source venv/bin/activate;python3.8 main.py)`- пример
<br>
<br>
Уведомления приходят когда подходит срок к окончанию тарифа (за 3, 2, 1 дней)<br>
Уведомления приходят когда кончается количество писем (3000, 2000, 1000, 500, 300, 200>)<br>
Уведомления приходят когда кончается траффик (500, 400, 300, 200, 100, 50>)<br>
