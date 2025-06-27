import logging

from openpyxl import load_workbook
from manifester.xlsx_row import XLSXRow


def read_excel(xlsx_file: str) -> list[XLSXRow]:
    """
    Read Excel file into source records

    :param xlsx_file: full path to Excel file
    :return: list[XLSXRow] a list of source records
    """
    workbook = load_workbook(filename='MS1986-167_Goldstein-Avery-papers_Template-for-digitization-metadata.xlsx')
    digitization_sheet = workbook["Digitization"]
    manifest_sheet = workbook["Manifest"]

    # The two worksheets in the file should have the same number of rows.
    if manifest_sheet.max_row != digitization_sheet.max_row:
        raise Exception('Mismatch between digitization and manifest records')

    records = []
    for i in range(2, digitization_sheet.max_row):
        record = XLSXRow(manifest_sheet[i], digitization_sheet[i][0].value)
        records.append(record)
        logging.info(f'Extracted {record.identifier} ::: {record.title}')

    return records