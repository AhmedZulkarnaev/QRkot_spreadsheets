import copy
from datetime import datetime
from typing import Any, Dict, List

from app.models.charity_project import CharityProject
from app.constants import (
    DATE_TIME_FORMAT, SPREADSHEET_TEMPLATE, TABLE_VALUES_TEMPLATE
)


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


async def get_sheet_dimensions(service, spreadsheetid, sheet_name):
    response = await service.spreadsheets.get(spreadsheetId=spreadsheetid)
    sheets = response['sheets']

    for sheet in sheets:
        if sheet['properties']['title'] == sheet_name:
            rows = sheet['properties']['gridProperties']['rowCount']
            columns = sheet['properties']['gridProperties']['columnCount']
            return rows, columns
    raise ValueError(f"Sheet named {sheet_name} not found")


def will_data_fit(data, sheet_dimensions):
    num_rows, num_cols = sheet_dimensions
    data_rows = len(data)
    data_cols = len(data[0]) if data else 0

    return data_rows <= num_rows and data_cols <= num_cols