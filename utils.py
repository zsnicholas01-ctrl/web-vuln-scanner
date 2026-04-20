# utils.py
def save_report(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)