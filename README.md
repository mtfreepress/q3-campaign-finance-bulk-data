# q3-campaign-finance-bulk-data

Convert the Excel workbooks in `input-q3-bulk-data/` to CSV:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python finance-xlsx-to-csv.py
```

CSVs are written to `output-q3-bulk-data/<workbook name>/<worksheet name>.csv`.
Every worksheet is exported, including hidden and empty sheets. Running the
script again overwrites matching CSVs. Input workbooks are left unchanged.

To use other directories:

```sh
.venv/bin/python finance-xlsx-to-csv.py --input-dir path/to/excel --output-dir path/to/csv
```

The first row is treated as the header. The export drops columns that contain
only empty or whitespace-only cells below that header, including columns with
Excel-generated names such as `Column970`. Columns containing zero or false are
kept, and remaining columns retain their original order and headers. Blank rows
are preserved.
CSVs use UTF-8 and standard CSV quoting. Excel formatting is not
included; formulas use their saved Excel results (blank if no saved result is
available). Dates and times are exported as Python's ISO-style text values.
