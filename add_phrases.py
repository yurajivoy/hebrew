import json
import re

INDEX_FILE = "index.html"
POOL_FILE = "phrases_pool.json"

# 1. Загружаем доступный пул фраз
try:
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool = json.load(f)
except Exception as e:
    print(f"Ошибка чтения файла пула: {e}")
    exit(0)

if not pool:
    print("Пул фраз пуст! Добавление не требуется.")
    exit(0)

# Берем первые 5 фраз из пула
phrases_to_add = pool[:5]
remaining_pool = pool[5:]

# 2. Читаем index.html и определяем последний ID
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

existing_ids = [int(i) for i in re.findall(r"id:\s*(\d+)", html_content)]
max_id = max(existing_ids) if existing_ids else 0

# 3. Формируем строки фраз для JS
formatted_js_items = []
for idx, item in enumerate(phrases_to_add, start=1):
    new_id = max_id + idx
    js_line = (
        f'      {{ id: {new_id}, '
        f'hebrew: "{item["hebrew"]}", '
        f'transcription: "{item["transcription"]}", '
        f'russian: "{item["russian"]}", '
        f'category: "{item["category"]}" }},'
    )
    formatted_js_items.append(js_line)

new_phrases_js = "\n" + "\n".join(formatted_js_items)

# 4. Вшиваем в массив basePhrasesDB внутри index.html
pattern = r"(const basePhrasesDB = \[[\s\S]*?)(];)"
updated_html = re.sub(pattern, r"\1" + new_phrases_js + r"\n    \2", html_content, count=1)

# 5. Сохраняем обновленный index.html и усеченный phrases_pool.json
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(updated_html)

with open(POOL_FILE, "w", encoding="utf-8") as f:
    json.dump(remaining_pool, f, ensure_ascii=False, indent=2)

print(f"Успешно перенесено {len(phrases_to_add)} фраз из пула в index.html!")
