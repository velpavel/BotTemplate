Template for Telegram bots.
Need pyTelegramBotAPI

Шаблон для Телеграм ботов.
Нужен pyTelegramBotAPI
Для начала запустить init_new.py
Потом в созданном config.ini прописать
Token
Admin_id (если известен).

При запуске в продуктиве изменить
Debug = 0

Текущие состояния пользователя при необходимости сохраняются в user_operation.
current_operation - Операция (регистраиця, работа с задачами и т.п.)
operation_status - шаг/этап операции.
additional_info - вся необходимая доп инфа. при необходимости сохранить группу параметров использовать json