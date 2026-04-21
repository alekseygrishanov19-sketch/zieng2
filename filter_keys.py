    # filter_keys.py
    import requests
    from datetime import datetime

    # --- НАСТРОЙКИ ---
    # Ссылка на RAW файл с гитхаба (!!! ЗАМЕНИ НА СВОЮ !!!)
    RAW_URL = "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_lite.txt" 
    # Имя файла, куда сохранять результат (будет в репозитории)
    OUTPUT_FILE = "filtered_vless_keys.txt"
    # Флаг, который ищем (русский флаг)
    FORBIDDEN_FLAG = "🇷🇺"

    def update_keys():
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Начало обновления ключей...")
            
            # Получаем данные по ссылке
            response = requests.get(RAW_URL)
            response.raise_for_status() # Проверка на ошибки при скачивании
            
            # Декодируем и разбиваем на строки
            content = response.text
            lines = content.strip().split('\n')
            
            initial_count = len(lines)
            
            # Фильтруем: оставляем только те строки, где нет русского флага
            # Дополнительная проверка, что строка не пустая, если вдруг там такие есть
            filtered_lines = [line for line in lines if line and FORBIDDEN_FLAG not in line]
            
            removed_count = initial_count - len(filtered_lines)
            
            print(f"Всего ключей: {initial_count}, удалено с флагом '{FORBIDDEN_FLAG}': {removed_count}, осталось: {len(filtered_lines)}")
            
            return filtered_lines

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении данных: {e}")
            return None
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            return None

    if __name__ == "__main__":
        filtered_keys = update_keys()
        
        if filtered_keys is not None:
            # Сохраняем в файл
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(filtered_keys))
            print(f"Результат сохранен в файл {OUTPUT_FILE}")
        else:
            print("Не удалось обновить ключи. Файл результата не создан.")
