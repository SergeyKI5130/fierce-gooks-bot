import json
from datetime import datetime
from pathlib import Path


def save_response(user, answer, response_file="responses.json", names_file="group_names.json"):
    # Загружаем текущие ответы
    if Path(response_file).exists():
        with open(response_file, "r", encoding="utf-8") as f:
            all_responses = json.load(f)
    else:
        all_responses = {}

    # Получаем текущую дату
    today = str(datetime.now().date())

    # Загружаем имена из файла
    group_names = {}
    if Path(names_file).exists():
        with open(names_file, "r", encoding="utf-8") as f:
            group_names = json.load(f)

    # Получение username и group name
    username = user.username or "unknown"
    group_name = group_names.get(username, "Бэм лентяй, games_name не прописал :Р ")

    # Ответ для сохранения
    response = {
        "full_name": user.full_name,
        "group_name": group_name,
        "link": f"https://t.me/{username}" if user.username else None,
        "answer": answer,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Добавляем в responses
    all_responses.setdefault(today, []).append(response)

    # Сохраняем обратно
    with open(response_file, "w", encoding="utf-8") as f:
        json.dump(all_responses, f, ensure_ascii=False, indent=2)
