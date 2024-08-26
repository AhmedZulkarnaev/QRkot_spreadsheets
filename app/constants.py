import copy
from datetime import datetime
from typing import Any, Dict, List

from app.models.charity_project import CharityProject

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


def create_spreadsheet_body(
        rows: int = 100, columns: int = 26, date_time: str = None
) -> Dict[str, Any]:
    if date_time is None:
        date_time = datetime.now().strftime(DATE_TIME_FORMAT)

    spreadsheet_body = copy.deepcopy(SPREADSHEET_TEMPLATE)

    spreadsheet_body['properties']['title'] = f'Отчёт от {date_time}'

    spreadsheet_body['sheets'][0]['properties']['gridProperties'][
        'rowCount'
    ] = rows
    spreadsheet_body['sheets'][0]['properties']['gridProperties'][
        'columnCount'
    ] = columns

    return spreadsheet_body


def create_table_values(projects: List[CharityProject], now_date_time: str):
    table_values = copy.deepcopy(TABLE_VALUES_TEMPLATE)
    table_values[0][1] = now_date_time

    for project in projects:
        new_row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description),
        ]
        table_values.append(new_row)

    return table_values


TABLE_VALUES_TEMPLATE = [
    ['Отчёт от', None],
    ['Топ проектов по скорости закрытия.'],
    ['Название проекта', 'Время сбора', 'Описание']
]
