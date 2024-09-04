import os
import csv

class PriceMachine():

    def __init__(self):
        self.data = []

    def load_prices(self, folder_path):
        key_mapping = {
            'название': ['название', 'продукт', 'товар', 'наименование'],
            'цена': ['цена', 'розница'],
            'вес': ['фасовка', 'масса', 'вес']
        }

        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file, delimiter=',')
                    for row in csv_reader:
                        data = {'файл': file}
                        for key, possible_keys in key_mapping.items():
                            for possible_key in possible_keys:
                                if possible_key in row:
                                    data[key] = row[possible_key]
                                    break
                        self.data.append(data)

    def export_to_console(self):
        for idx, product in enumerate(self.data, 1):
            print(
                f"{idx}. Название: {product.get('название')}, Цена: {product.get('цена')}, Вес: {product.get('вес')}, Файл: {product.get('файл')}")

    def search_product(self, search_query):
        results = [product for product in self.data if search_query.lower() in product.get('название', '').lower()]
        sorted_results = sorted(results, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
        return sorted_results

    def export_to_html(self, output_file_path=r'C:\Users\maksi\Downloads\praktika_price_list\output.html'):
        if self.data:
            sorted_data = sorted(self.data, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write('''
                <!DOCTYPE html>
                <html lang='ru'>
                <head>
                    <meta charset='UTF-8'>
                    <title>Позиции продуктов</title>
                </head>
                <body>
                    <table>
                        <tr>
                            <th>№</th>
                            <th>Наименование</th>
                            <th>Цена</th>
                            <th>Вес</th>
                            <th>Файл</th>
                            <th>Цена за кг.</th>
                        </tr>
                ''')
                for idx, row in enumerate(sorted_data, start=1):
                    item_name = row.get('название', '')
                    price_per_kg = float(row.get('цена', 0)) / float(row.get('вес', 1))
                    file.write(
                        f"<tr><td>{idx}</td><td>{item_name}</td><td>{row.get('цена', '')}</td><td>{row.get('вес', '')}</td><td>{row.get('файл', '')}</td><td>{price_per_kg:.1f}</td></tr>"
                    )
                file.write('''
                    </table>
                </body>
                </html>
                ''')
            print(f"HTML файл успешно создан: {output_file_path}")
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

price_machine = PriceMachine()
price_machine.load_prices(r'C:\Users\maksi\Downloads\praktika_price_list')

try:
    while True:
        search_query = input("Введите фрагмент наименования товара для поиска (или 'exit' для выхода): ")

        if search_query.lower() == 'exit':
            price_machine.export_to_html()
            print("Работа завершена.")
            break

        results = price_machine.search_product(search_query)

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
