
import os
import csv
import json

class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path='prices'):
        key_data = {
            'название': ['название', 'продукт', 'товар', 'наименование'],
            'цена': ['цена', 'розница'],
            'вес': ['фасовка', 'масса', 'вес']
        }
        # Проверяем наличие папки
        if not os.path.exists(file_path):
            print(f"Путь '{file_path}' не найден.")
            return

        for file in os.listdir(file_path):
            if file.endswith('.csv'):
                try:
                    with open(os.path.join(file_path, file), 'r', encoding='utf-8') as csv_file:
                        csv_reader = csv.DictReader(csv_file, delimiter=',')
                        print(f"Чтение файла: {file}")  # Информирование о процессе чтения файла
                        for row in csv_reader:
                            data = {'файл': file}
                            for key, possible_keys in key_data.items():
                                for possible_key in possible_keys:
                                    if possible_key in row:
                                        data[key] = row[possible_key]
                                        break
                            self.data.append(data)
                    print(f"Файл {file} успешно прочитан.")  # Успешное завершение чтения файла
                except Exception as e:
                    print(f"Ошибка при чтении файла {file}: {e}")
            else:
                print(f"Файл {file} пропущен, так как не является CSV.")
    def export_to_console(self):
        for idx, product in enumerate(self.data, 1):
            print(
                f"{idx}. Название: {product.get('название')}, Цена: {product.get('цена')}, Вес: {product.get('вес')}, Файл: {product.get('файл')}")


    def _search_product_price_weight(self, headers):
        results = [product for product in self.data if headers.lower() in product.get('название', '').lower()]
        sorted_results = sorted(results, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
        return sorted_results

    def export_to_html(self, fname=r'C:\Users\user\Python Project 10\pythonProject8\pythonProject\Price_list_analyzer\output.html'):
        if self.data:
            sorted_data = sorted(self.data, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
            with open(fname, 'w', encoding='utf-8') as file:
                file.write('''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset='UTF-8'>
                    <title>Позиции продуктов</title>
                </head>
                <body>
                    <table>
                        <tr>
                            <th>Номер</th>
                            <th>Название</th>
                            <th>Цена</th>
                            <th>Фасовка</th>
                            <th>Файл</th>
                            <th>Цена за кг.</th>
                        </tr>
                ''')
                for idx, row in enumerate(sorted_data, start=1):
                    item_name = row.get('название', '')
                    try:
                        price_per_kg = float(row.get('цена', 0)) / float(row.get('вес', 1))
                    except ValueError:
                        price_per_kg = 0
                    file.write(
                        f"<tr><td>{idx}</td><td>{item_name}</td><td>{row.get('цена', '')}</td><td>{row.get('вес', '')}</td><td>{row.get('файл', '')}</td><td>{price_per_kg:.1f}</td></tr>"
                    )
                file.write('''
                    </table>
                </body>
                </html>
                ''')
            print(f"HTML файл успешно создан: {fname}")
        else:
            print("Нет данных для экспорта в HTML файл.")

    def find_text(self, text):
        results = [row for row in self.data if 'название' in row and text.lower() in row['название'].lower()]
        sorted_results = sorted(results, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))

        if sorted_results:
            print("Результаты поиска:")
            for idx, result in enumerate(sorted_results, 1):
                print(
                    f"{idx}. Название: {result.get('название')}, Цена: {result.get('цена')}, Вес: {result.get('вес')}, Файл: {result.get('файл')}, Цена за кг: {float(result.get('цена', 0)) / float(result.get('вес', 1))}")
        else:
            print("Нет результатов по вашему запросу.")

        return sorted_results


pm = PriceMachine()
pm.load_prices(r'C:\Users\user\Python Project 10\pythonProject8\pythonProject\Price_list_analyzer\prices')


try:
    while True:
        search_query = input("Введите фрагмент наименования товара для поиска (или 'exit' для выхода): ")

        if search_query.lower() == 'exit':
            pm.export_to_html()
            print("Работа завершена.")
            break

        results = pm._search_product_price_weight(search_query)#find_text(search_query)

        if results:
            sorted_results = sorted(results, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
            for idx, result in enumerate(sorted_results, 1):
                print(
                    f"{idx}. Название: {result.get('название')}, Цена: {result.get('цена')}, Вес: {result.get('вес')}, Файл: {result.get('файл')}, Цена за кг: {float(result.get('цена', 0)) / float(result.get('вес', 1))}")
        else:
            print("Нет результатов по вашему запросу.")
            print(f"Вы искали: {search_query}")

except Exception as e:
    print(f"Произошла ошибка: {e}")
