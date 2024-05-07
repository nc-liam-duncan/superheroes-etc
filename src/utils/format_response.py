def format_response(rows, column_headings):
    return [
        {col: item for col, item in zip(column_headings, row)} for row in rows
    ]
