# Уведомления от sendpulse

Напоминалка, когда кончается пакет в Sendpulse на SMTP. <br>
Уведомления приходят в Telegram

Для работы необходимо: 
- настроить venv окружение
- установить все пакеты из requirements.txt
- прописать данные в database.db:
  - client_id - ID клиента sendpulse
  - client_secret - Secret клиента sendpulse
  - TG_TOKEN - Токен телеграм бота
  - CHAT_ID - Чат куда будут приходить уведомления
  - EXCEPTION_CHAT_ID - Чат куда будут приходить технические сообщения
- настроить crontab<br>
(*/30 * * * * cd /var/www/smtp_sendpulse_bot;source venv/bin/activate;python3.8 main.py) - пример



Уведомления приходят когда подходит срок к окончанию тарифа (за 3, 2, 1 дней)<br>
Уведомления приходят когда кончается количество писем (1000, 500, 300, 100 >)<br>
