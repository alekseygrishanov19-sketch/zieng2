import requests

# Твоя ссылка
RAW_URL = "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_lite.txt"
OUTPUT_FILE = "filtered_vless_keys.txt"

# ТОЛЬКО РУССКИЙ ФЛАГ (в обычном виде и в кодировке ссылки)
RU_FLAG_EMOJI = "🇷🇺"
RU_FLAG_ENCODED = "%F0%9F%87%B7%F0%9F%87%BA"

def main():
    try:
        print(f"Загрузка: {RAW_URL}")
        response = requests.get(RAW_URL, timeout=30)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        total_before = len(lines)
        
        filtered_lines = []
        removed_count = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Проверяем ТОЛЬКО наличие флага
            if RU_FLAG_EMOJI in line or RU_FLAG_ENCODED in line:
                removed_count += 1
                continue
            
            # Если флага нет — сохраняем ключ
            filtered_lines.append(line)

        # Сохраняем результат
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(filtered_lines))

        print(f"Готово!")
        print(f"Было всего: {total_before}")
        print(f"Удалено (только по флагу 🇷🇺): {removed_count}")
        print(f"Осталось: {len(filtered_lines)}")

    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)

if __name__ == "__main__":
    main()
