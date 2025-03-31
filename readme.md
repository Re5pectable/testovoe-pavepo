# Pavepo Audio API — инструкция по запуску

## 1. Локальное хранилище аудиофайлов

При запуске через Docker можно указать маунт папки, где будут храниться загруженные аудиофайлы:

```yaml
services:
  pavepo-api:
    container_name: pavepo-api
    build: ./src
    volumes:
      - ./media:/usr/app/media
```

Внутри контейнера файлы будут сохраняться в `/usr/app/media`.

---

## 2. Указание допустимых расширений аудио

В `.env` файле укажите разрешённые форматы:

```env
ALLOWED_EXTENTIONS=mp3,wav,flac,aac,m4a,ogg,opus,alac,aif,aiff,wma,amr,ape,mp2
```

Список разделяется запятыми, без пробелов.

---

## 3. Прогон миграций (если база уже запущена)

```bash
docker exec pavepo-api bash -c "cd src/db && alembic upgrade head"
```

---

## 4. Запуск приложения

```bash
docker compose up
```

Приложение будет доступно на `http://127.0.0.1:8000`.