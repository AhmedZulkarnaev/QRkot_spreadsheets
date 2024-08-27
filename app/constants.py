DATE_TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
COLUMNS = 5
ROWS = 100

SPREADSHEET_TEMPLATE = {
    'properties': {
        'title': 'Отчёт',
        'locale': 'ru_RU'
    },
    'sheets': [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': 100,
                'columnCount': 26
            }
        }
    }]
}


TABLE_VALUES_TEMPLATE = [
    ['Отчёт от', None],
    ['Топ проектов по скорости закрытия.'],
    ['Название проекта', 'Время сбора', 'Описание']
]
