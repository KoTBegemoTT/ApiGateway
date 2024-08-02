# APIGateway


Этот сервис является точкой входа для обращения к другим.

## Services

### Auth service
Сервис для аунтификации.

| Method | Path                       | Description                            |
|--------|----------------------------|----------------------------------------|
| POST   | /auth-service/register/    | Регистрация пользователя               |
| POST   | /auth-service/auth/        | Получение или обновление токена        |
| GET    | /auth-service/check_token/ | Проверка токена на валидность          |


### Transaction service
Сервис для создания транзакции и получения информации о них.

| Method | Path                          | Description                        |
|--------|-------------------------------|------------------------------------|
| POST   | /transaction-service/create/  | Создание транзакции                |
| POST   | /transaction-service/report/  | Получение отчёта о транзакциях     |


### Face verification sevice
Сервис верификации пользователя.

| Method | Path                                    | Description                                    |
|--------|-----------------------------------------|------------------------------------------------|
| GET    | /face-verification-service/get_vector/  | Получение векторного представления изображения |
