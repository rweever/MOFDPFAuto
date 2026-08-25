from src.payroll_query import fetch_contribution_data
from src.excel_export import generate_excel


payroll = "03726/0400"
service = "FIRE"

try:
    columns, rows = fetch_contribution_data(
        payroll,
        service
    )

    output_file = generate_excel(
        columns,
        rows,
        payroll,
        service
    )

    print("Excel generation successful.")
    print(f"Records exported: {len(rows)}")
    print(f"File created: {output_file}")

except Exception as error:
    print("Excel generation failed.")
    print(error)