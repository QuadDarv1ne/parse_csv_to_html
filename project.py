import os
import csv


class PriceMachine:
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

    def search_product(self, search_query, min_price=None, max_price=None, min_weight=None, max_weight=None):
        results = [
            product for product in self.data
            if search_query.lower() in product.get('название', '').lower()
               and (min_price is None or float(product.get('цена', 0)) >= min_price)
               and (max_price is None or float(product.get('цена', 0)) <= max_price)
               and (min_weight is None or float(product.get('вес', 1)) >= min_weight)
               and (max_weight is None or float(product.get('вес', 1)) <= max_weight)
        ]
        sorted_results = sorted(results, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
        return sorted_results

    def export_to_html(self, output_file_path=r'C:\Users\maksi\Downloads\praktika_price_list\output.html',
                       rows_per_page=100):
        if self.data:
            sorted_data = sorted(self.data, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
            num_pages = -(-len(sorted_data) // rows_per_page)  # ceil division
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(f'''
                <!DOCTYPE html>
                <html lang='ru'>
                <head>
                    <meta charset='UTF-8'>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Позиции продуктов</title>
                    <!-- Подключение Bootstrap CSS -->
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
                    <style>
                        .page-link.active {{
                            background-color: #007bff;
                            color: white;
                        }}
                        .modal-body img {{
                            max-width: 100%;
                            height: auto;
                        }}
                        @media (max-width: 768px) {{
                            .table-responsive {{
                                overflow-x: auto;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="container mt-4">
                        <h1 class="mb-4">Список продуктов</h1>
                        <form class="form-inline mb-4">
                            <input class="form-control mr-sm-2" type="search" placeholder="Поиск по наименованию" aria-label="Search" id="search-name">
                            <input class="form-control mr-sm-2" type="number" placeholder="Цена от" aria-label="Min Price" id="search-min-price">
                            <input class="form-control mr-sm-2" type="number" placeholder="Цена до" aria-label="Max Price" id="search-max-price">
                            <input class="form-control mr-sm-2" type="number" placeholder="Вес от" aria-label="Min Weight" id="search-min-weight">
                            <input class="form-control mr-sm-2" type="number" placeholder="Вес до" aria-label="Max Weight" id="search-max-weight">
                            <button class="btn btn-primary my-2 my-sm-0" type="button" id="search-button">Искать</button>
                        </form>
                        <div class="table-responsive">
                            <table class="table table-striped table-bordered">
                                <thead>
                                    <tr>
                                        <th>№</th>
                                        <th>Наименование</th>
                                        <th>Цена</th>
                                        <th>Вес</th>
                                        <th>Файл</th>
                                        <th>Цена за кг.</th>
                                    </tr>
                                </thead>
                                <tbody id="product-table-body">
                ''')
                for idx, row in enumerate(sorted_data, start=1):
                    item_name = row.get('название', '')
                    price_per_kg = float(row.get('цена', 0)) / float(row.get('вес', 1))
                    file.write(
                        f"<tr data-name='{item_name}' data-price='{row.get('цена', 0)}' data-weight='{row.get('вес', 1)}'><td>{idx}</td><td>{item_name}</td><td>{row.get('цена', '')}</td><td>{row.get('вес', '')}</td><td>{row.get('файл', '')}</td><td>{price_per_kg:.1f}</td></tr>"
                    )
                file.write(f'''
                                </tbody>
                            </table>
                            <nav aria-label="Page navigation example">
                                <ul class="pagination" id="pagination">
                ''')
                for page in range(1, num_pages + 1):
                    file.write(
                        f'<li class="page-item"><a class="page-link" href="#" data-page="{page}">{page}</a></li>')
                file.write('''
                                </ul>
                            </nav>
                        </div>
                        <div class="modal fade" id="productModal" tabindex="-1" aria-labelledby="productModalLabel" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="productModalLabel">Подробности о продукте</h5>
                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        <!-- Информация о продукте -->
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
                        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
                        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
                        <script>
                            document.addEventListener('DOMContentLoaded', function() {{
                                const rowsPerPage = {rows_per_page};
                                const rows = document.querySelectorAll('#product-table-body tr');
                                const numPages = Math.ceil(rows.length / rowsPerPage);
                                const paginationContainer = document.getElementById('pagination');

                                function showPage(page) {{
                                    rows.forEach((row, index) => {{
                                        row.style.display = (index >= (page - 1) * rowsPerPage && index < page * rowsPerPage) ? '' : 'none';
                                    }});
                                }}

                                function createPagination() {{
                                    paginationContainer.innerHTML = '';
                                    for (let i = 1; i <= numPages; i++) {{
                                        const button = document.createElement('a');
                                        button.className = 'page-link';
                                        button.href = '#';
                                        button.innerText = i;
                                        button.dataset.page = i;
                                        button.addEventListener('click', (event) => {{
                                            event.preventDefault();
                                            showPage(i);
                                            document.querySelectorAll('.page-link').forEach(btn => btn.classList.remove('active'));
                                            button.classList.add('active');
                                        }});
                                        paginationContainer.appendChild(button);
                                    }}
                                    showPage(1);
                                    document.querySelectorAll('.page-link')[0].classList.add('active');
                                }}

                                function filterResults() {{
                                    const searchName = document.getElementById('search-name').value.toLowerCase();
                                    const minPrice = parseFloat(document.getElementById('search-min-price').value) || 0;
                                    const maxPrice = parseFloat(document.getElementById('search-max-price').value) || Infinity;
                                    const minWeight = parseFloat(document.getElementById('search-min-weight').value) || 0;
                                    const maxWeight = parseFloat(document.getElementById('search-max-weight').value) || Infinity;

                                    rows.forEach(row => {{
                                        const name = row.dataset.name.toLowerCase();
                                        const price = parseFloat(row.dataset.price);
                                        const weight = parseFloat(row.dataset.weight);

                                        const visible = name.includes(searchName) &&
                                                        price >= minPrice && price <= maxPrice &&
                                                        weight >= minWeight && weight <= maxWeight;

                                        row.style.display = visible ? '' : 'none';
                                    }});
                                    createPagination();
                                }}

                                document.getElementById('search-button').addEventListener('click', filterResults);
                                createPagination();
                            }});
                        </script>
                </body>
                </html>
                ''')
            print(f"HTML файл успешно создан: {output_file_path}")
        else:
            print("Нет данных для экспорта в HTML файл.")


price_machine = PriceMachine()
price_machine.load_prices(r'C:\Users\maksi\Downloads\praktika_price_list')

try:
    while True:
        search_query = input("Введите фрагмент наименования товара для поиска (или 'exit' для выхода): ")

        # лучше указать здесь
        if search_query.lower() == 'exit':
            price_machine.export_to_html()
            print("Работа завершена.")
            break

        min_price = input("Введите минимальную цену (или оставьте пустым): ")
        max_price = input("Введите максимальную цену (или оставьте пустым): ")
        min_weight = input("Введите минимальный вес (или оставьте пустым): ")
        max_weight = input("Введите максимальный вес (или оставьте пустым): ")

        min_price = float(min_price) if min_price else None
        max_price = float(max_price) if max_price else None
        min_weight = float(min_weight) if min_weight else None
        max_weight = float(max_weight) if max_weight else None

        results = price_machine.search_product(search_query, min_price, max_price, min_weight, max_weight)

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
