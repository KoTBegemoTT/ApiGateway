# Changelog

Все заметные изменения в этом проекте будут задокументированы в этом файле.

Этот формат основывается на [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), и этот проект придерживается [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [6.0.0] - 2024-9-6

### Добавлено

- Трейсинг с jaeger
- Запус Prometheus в docker compose
- Запуск Jaeger в docker compose

### Изменено

- Сессия для отправки запросов к каждому сервису теперь создаётся один раз и периспользуется

## [5.1.0] - 2024-8-29

### Добавлено

- Конфигурация для Helm

## [5.0.0] - 2024-8-27

### Добавлено

- Манифесты для запуска сервиса в kubernetes

## [4.0.0] - 2024-8-20

### Добавлено

- Запуск postgres в docker compose.

### Изменено

- Теперь переменные настроек можно переопределять, с помощью env переменных.

## [3.1.0] - 2024-8-12

### Добавлено

- health check для kafka в docker-compose.yml
- url /verify/, который принимает изображение и user id, и перенаправляет это на аналогичный url в auth service

## [3.0.0] - 2024-8-7

### Добавлено

- url /healthz/ready для проверки статуса сервиса

### Изменено

- В запросах, перенаправляемых на transactions service теперь перед перенаправлением происходит проверка токена аналогично запросу на /auth_service/check_token.

## [2.0.0] - 2024-8-2

### Добавлено

- Docker compose
- url /auth_service/check_token, для проверки токена на валидность
- Добавлены сабмодули в папке submodules в корне

### Изменено

- В случае возникновения ошибки в стороннем сервисе запросы Gateway теперь обрабатывают и возвращают ту же ошибку

## [1.1.0] - 2024-8-1

### Добавлено

- Docker контейнер

## [1.0.0] - 2024-07-28

### Добавлено

- Api с использованием FastApi
- Тесты с pytest
- gitlab-ci
