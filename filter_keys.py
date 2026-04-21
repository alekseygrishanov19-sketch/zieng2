import requests
import os

# Твоя ссылка
RAW_URL = "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_lite.txt"
OUTPUT_FILE = "filtered_vless_keys.txt"
FORBIDDEN_FLAG = "🇷🇺"
MAX_CHECK = 100 # Проверяем только первые 100 строк

def main():
    try:
        print(f"Загрузка ключей из: {RAW_URL}")
        response = requests.get(RAW_URL, timeout=30)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        total_lines = len(lines)
        print(f"Всего получено строк: {total_lines}")

        filtered_lines = []
        removed_count = 0

        for i, line in enumerate(lines):
            # Если это одна из первых 100 строк и в ней есть русский флаг - удаляем
            if i < MAX_CHECK and FORBIDDEN_FLAG in line:
                removed_count += 1
                continue
            
            # Все остальное (после 100-й строки или без флага) — сохраняем
            if line.strip(): # Пропускаем пустые строки
                filtered_lines.append(line)

        # Сохраняем результат в файл
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(filtered_lines))

        print(f"Готово! Удалено ключей с флагом: {removed_count}")
        print(f"Сохранено всего ключей в {OUTPUT_FILE}: {len(filtered_lines)}")

    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)

if __name__ == "__main__":
    main()

