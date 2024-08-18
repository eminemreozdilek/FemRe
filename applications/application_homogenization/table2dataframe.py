import pandas as pd
from PySide6.QtWidgets import QTableWidget


def get_dataframe(table: QTableWidget):
    """Converts data from the table widget to a pandas DataFrame."""
    columns = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
    data = []
    for row in range(table.rowCount()):
        row_data = []
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item:
                row_data.append(item.text())  # Extract text from table item
            else:
                row_data.append(None)  # Handle empty cells
        data.append(row_data)
    return pd.DataFrame(data, columns=columns)
