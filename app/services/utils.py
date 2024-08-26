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