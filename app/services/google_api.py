from datetime import datetime

from typing import List
from aiogoogle import Aiogoogle

from app.models import CharityProject
from app.core.config import settings
from app.constants import DATE_TIME_FORMAT
from app.services.utils import create_spreadsheet_body, create_table_values, get_sheet_dimensions, will_data_fit


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    spreadsheet_body = create_spreadsheet_body(date_time=now_date_time)
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
):
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: List[CharityProject],
        wrapper_services: Aiogoogle,
        sheet_name: str
):
    now_date_time = datetime.now().strftime(DATE_TIME_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = create_table_values(projects, now_date_time)
    rows, columns = await get_sheet_dimensions(
        service, spreadsheetid, sheet_name
    )
    if not will_data_fit(table_values, (rows, columns)):
        raise ValueError("Data exceeds the current dimensions of the sheet")
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:C30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )