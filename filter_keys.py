import requests

# Твоя ссылка
RAW_URL = "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_lite.txt"
OUTPUT_FILE = "filtered_vless_keys.txt"

# Список признаков для удаления (флаг РФ в кодировке, сам флаг, и русские сервисы)
FORBIDDEN_MARKERS = [
    "%F0%9F%87%B7%F0%9F%87%BA", # Это 🇷🇺 в URL-кодировке
    "🇷🇺",                       # Обычный эмодзи
    "Yandex",                   # Яндекс
    "VK",                       # ВК
    ".ru"                       # Домены .ru (например ads.x5.ru)
]

def main():
    try:
        print(f"Загрузка ключей из: {RAW_URL}")
        response = requests.get(RAW_URL, timeout=30)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        total_before = len(lines)
        
        filtered_lines = []
        removed_count = 0

        # Проверяем все строки в файле
        for line in lines:
            line_strip = line.strip()
            if not line_strip:
                continue

            # Проверяем на наличие любого запрещенного маркера
            found_forbidden = False
            for marker in FORBIDDEN_MARKERS:
                if marker.lower() in line_strip.lower(): # Регистр не важен
                    found_forbidden = True
                    break
            
            if found_forbidden:
                removed_count += 1
            else:
                filtered_lines.append(line_strip)

        # Сохраняем результат
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(filtered_lines))

        print(f"Успешно обработано!")
        print(f"Всего было: {total_before}")
        print(f"Удалено русских ключей: {removed_count}")
        print(f"Осталось нормальных: {len(filtered_lines)}")

    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)

if __name__ == "__main__":
    main()
