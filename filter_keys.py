import os
import requests
from datetime import datetime

# Настройки через переменные окружения (можно задать в workflow)
RAW_URL = os.getenv("RAW_URL", "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_lite.txt")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "filtered_vless_keys.txt")
FORBIDDEN_FLAG = os.getenv("FORBIDDEN_FLAG", "🇷🇺")
MAX_CHECK = int(os.getenv("MAX_CHECK", "100"))  # проверяем только первые N строк

def main():
    try:
        print(f"[{datetime.utcnow().isoformat()}] Downloading: {RAW_URL}")
        resp = requests.get(RAW_URL, timeout=30)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        total = len(lines)
        to_check = min(MAX_CHECK, total)
        print(f"Total lines: {total}. Will check first {to_check} lines for forbidden flag.")

        removed = 0
        filtered = []
        for idx, line in enumerate(lines):
            if idx < to_check and FORBIDDEN_FLAG in line:
                removed += 1
                continue
            # optionally skip empty lines
            if line.strip() == "":
                continue
            filtered.append(line)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(filtered))

        print(f"Done. Removed {removed} lines with flag. Saved {len(filtered)} lines to {OUTPUT_FILE}.")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
