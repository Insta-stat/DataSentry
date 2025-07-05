import requests

# 🔗 Полная mp4-ссылка (не обрезай!)
url = "https://instagram.fdac7-1.fna.fbcdn.net/o1/v/t16/f2/m86/AQMdYfxT_MOk4K_dfvj3NY2dGKkfxJtQkPjo5nHGpvVTJBcXD8hHIXnOTxs8k5dT2ZnjAc92vPdxAF2BuI_PZVEkeDTvm71lUN1viFk.mp4?stp=dst-mp4&efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0&_nc_cat=100&vs=747788810911725_3140017688&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC85NjREOTYwQjNEMkIxMzM3OTk4RjcxMUU4Qjg3N0Q5NV92aWRlb19kYXNoaW5pdC5tcDQVAALIARIAFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HSEV4bkIyWl9JR05sTm9JQUxYZjRUQjh6MWhNYnFfRUFBQUYVAgLIARIAKAAYABsAFQAAJuLCp%2F6Jgdo%2FFQIoAkMzLBdAWHEGJN0vGxgSZGFzaF9iYXNlbGluZV8xX3YxEQB1%2Fgdl5p0BAA%3D%3D&_nc_rid=82600156b5&ccb=9-4&oh=00_AfOsKlRsnRrex7qP83Rx8buX2QsAG6use_2KR2EDZkIDhg&oe=68541547&_nc_sid=10d13b"

# 📁 Имя файла для сохранения
filename = "video.mp4"

# 🧠 Заголовки, имитирующие браузер
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
}

print("[INFO] Скачивание началось...")
print(f"[DEBUG] URL: {url}")
print(f"[DEBUG] Имя файла: {filename}")

try:
    response = requests.get(url, headers=headers, stream=True, timeout=30)
    response.raise_for_status()  # Проверка на ошибки HTTP

    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"[SUCCESS] Файл успешно скачан: {filename}")

except requests.exceptions.RequestException as e:
    print(f"[ERROR] Не удалось скачать видео: {e}")
