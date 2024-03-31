"""Utilities to collect tables from an image via textract

Reference: https://docs.aws.amazon.com/textract/latest/dg/examples-export-table-csv.html
"""


def get_text(cell, blocks_map):
    text = ""
    if "Relationships" in cell:
        for relationship in cell["Relationships"]:
            if relationship["Type"] == "CHILD":
                for child_id in relationship["Ids"]:
                    word = blocks_map[child_id]
                    if word["BlockType"] == "WORD":
                        if (
                            "," in word["Text"]
                            and word["Text"].replace(",", "").isnumeric()
                        ):
                            text += '"' + word["Text"] + '"' + " "
                        else:
                            text += word["Text"] + " "
                    if word["BlockType"] == "SELECTION_ELEMENT":
                        if word["SelectionStatus"] == "SELECTED":
                            text += "X "
    return text


def get_rows_columns_map(table, blocks_map):
    rows = {}

    for relationship in table["Relationships"]:
        if relationship["Type"] == "CHILD":
            for child_id in relationship["Ids"]:
                cell = blocks_map[child_id]
                if cell["BlockType"] == "CELL":
                    row_index = cell["RowIndex"]
                    col_index = cell["ColumnIndex"]
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}

                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


SEPARATOR = ";"


def generate_table_csv(table, blocks_map, table_index, separator=None):
    separator = SEPARATOR if separator is None else separator

    rows = get_rows_columns_map(table, blocks_map)

    table_id = "Table_" + str(table_index)

    # get cells.
    csv = "Table: {0}\n\n".format(table_id)

    for _, cols in rows.items():
        for _, text in cols.items():
            csv += "{}".format(text) + separator
        csv += "\n"

    csv += "\n\n"
    return csv


def get_table_csv_results(client, image_bytes):
    # get the results
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )

    # Get the text blocks
    blocks = response["Blocks"]

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block["Id"]] = block
        if block["BlockType"] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "No Table found."

    csv = ""
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv(table, blocks_map, index + 1)

    return csv
