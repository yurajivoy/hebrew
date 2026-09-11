import json
import re

INDEX_FILE = "index.html"
POOL_FILE = "phrases_pool.json"

try:
    with open(POOL_FILE, "r", encoding="utf-8") as f:
        pool = json.load(f)
except Exception as e:
    print(f"Ошибка чтения файла пула: {e}")
    exit(0)

if not pool:
    print("Пул фраз пуст! Добавление не требуется.")
    exit(0)

phrases_to_add = pool[:5]
remaining_pool = pool[5:]

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

# Находим максимальный существующий ID
existing_ids = [int(i) for i in re.findall(r"id:\s*(\d+)", html_content)]
max_id = max(existing_ids) if existing_ids else 0

formatted_js_items = []
for idx, item in enumerate(phrases_to_add, start=1):
    new_id = max_id + idx
    # Экранируем кавычки
    hebrew = item.get("hebrew", "").replace('"', '\\"')
    trans = item.get("transcription", "").replace('"', '\\"')
    rus = item.get("russian", "").replace('"', '\\"')
    cat = item.get("category", "").replace('"', '\\"')
    theory = item.get("theory", "Разбор временно отсутствует.").replace('"', '\\"')

    js_line = (
        f'      {{ id: {new_id}, '
        f'hebrew: "{hebrew}", '
        f'transcription: "{trans}", '
        f'russian: "{rus}", '
        f'category: "{cat}", '
        f'theory: "{theory}" }},'
    )
    formatted_js_items.append(js_line)

new_phrases_js = "\n" + "\n".join(formatted_js_items)

# Добавляем новые элементы в массив basePhrasesDB
pattern = r"(const basePhrasesDB = \[[\s\S]*?)(];)"
updated_html = re.sub(pattern, r"\1" + new_phrases_js + r"\n    \2", html_content, count=1)

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(updated_html)

with open(POOL_FILE, "w", encoding="utf-8") as f:
    json.dump(remaining_pool, f, ensure_ascii=False, indent=2)

print(f"Успешно перенесено {len(phrases_to_add)} фраз с теорией в index.html!")
