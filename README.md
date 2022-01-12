# Уведомления от sendpulse

Напоминалка, когда кончается пакет в sendpulse на рассылку. <br>
Уведомления приходят в Telegram

Для работы необходимо: 
- установить все пакеты из requirements.txt
- прописать данные в database.db:
  - client_id - ID клиента sendpulse
  - client_secret - Secret клиента sendpulse
  - TG_TOKEN - Токен телеграм бота
  - CHAT_ID - Чат куда будут приходить уведомления
  - EXCEPTION_CHAT_ID - Чат куда будут приходить технические сообщения