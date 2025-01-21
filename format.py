import re

def process_html_file(file_path):
    # Читаем содержимое файла
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("Ошибка: Файл не найден. Проверьте путь.")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Удаляем все &nbsp;
    content = content.replace("&nbsp;", " ")

    # Удаляем все теги <br> (их замены не будет, просто удаляем)
    content = re.sub(r"<br\s*/?>", "", content)

    # Регулярное выражение для поиска формул
    formula_regex = re.compile(r"([a-zA-Z0-9_{}^=+\-*/().\\]+)")

    # Функция для добавления \( ... \) вокруг формулы
    def wrap_formula(match):
        return f"\\({match.group(0)}\\)"

    # Поиск и замена формул внутри HTML содержимого
    def replace_in_tags(match):
        inner_html = match.group(1)
        replaced_html = re.sub(formula_regex, wrap_formula, inner_html)
        return match.group(0).replace(inner_html, replaced_html)

    # Поиск формул внутри тегов и оборачивание их в \( ... \)
    processed_content = re.sub(r">(.*?)<", replace_in_tags, content, flags=re.DOTALL)

    # Сохраняем результат в новый файл
    output_file = file_path.replace('.html', '_processed.html')
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(processed_content)
        print(f"Обработанный файл сохранён: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    # Запрашиваем путь до HTML-файла
    file_path = input("Введите путь до HTML-файла: ")
    process_html_file(file_path)
