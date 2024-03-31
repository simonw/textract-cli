from textract_cli.tables import get_text, get_rows_columns_map, generate_table_csv


def test_get_text():
    result = {"Relationships": [{"Type": "CHILD", "Ids": ["block1", "block2"]}]}

    blocks_map = {
        "block1": {"BlockType": "WORD", "Text": "Hello"},
        "block2": {"BlockType": "SELECTION_ELEMENT", "SelectionStatus": "SELECTED"},
    }

    expected_text = "Hello X "

    assert get_text(result, blocks_map) == expected_text


TABLE = {
    "Relationships": [{"Type": "CHILD", "Ids": ["cell1", "cell2", "cell3", "cell4"]}]
}

BLOCKS_MAP = {
    "cell1": {
        "BlockType": "CELL",
        "RowIndex": 0,
        "ColumnIndex": 0,
        "Id": "cell1",
        "Relationships": [{"Type": "CHILD", "Ids": ["cell1-word"]}],
    },
    "cell1-word": {"BlockType": "WORD", "Text": "A", "Id": "cell1-word"},
    "cell2": {
        "BlockType": "CELL",
        "RowIndex": 0,
        "ColumnIndex": 1,
        "Id": "cell2",
        "Relationships": [{"Type": "CHILD", "Ids": ["cell2-word"]}],
    },
    "cell2-word": {"BlockType": "WORD", "Text": "1,000.0", "Id": "cell2-word"},
    "cell3": {
        "BlockType": "CELL",
        "RowIndex": 1,
        "ColumnIndex": 0,
        "Id": "cell3",
        "Relationships": [{"Type": "CHILD", "Ids": ["cell3-word"]}],
    },
    "cell3-word": {"BlockType": "WORD", "Text": "C", "Id": "cell3-word"},
    "cell4": {
        "BlockType": "CELL",
        "RowIndex": 1,
        "ColumnIndex": 1,
        "Id": "cell4",
        "Relationships": [{"Type": "CHILD", "Ids": ["cell4-word"]}],
    },
    "cell4-word": {"BlockType": "WORD", "Text": "2.000,00", "Id": "cell4-word"},
}


def test_get_rows_columns_map():
    expected_rows = {0: {0: "A ", 1: "1,000.0 "}, 1: {0: "C ", 1: "2.000,00 "}}

    returned_rows = get_rows_columns_map(TABLE, BLOCKS_MAP)

    assert returned_rows == expected_rows


def test_generate_table_csv():
    table_index = 0

    returned_csv = generate_table_csv(TABLE, BLOCKS_MAP, table_index)

    expected_csv = """Table: Table_0

A ;1,000.0 ;
C ;2.000,00 ;


"""
    assert len(expected_csv) == len(returned_csv)
    for exp_line, re_line in zip(expected_csv, returned_csv):
        assert exp_line == re_line
    assert returned_csv == expected_csv
