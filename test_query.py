from src.payroll_query import fetch_contribution_data


payroll = "03726/0400"
service = "FIRE"


try:
    columns, rows = fetch_contribution_data(
        payroll,
        service
    )

    print("Payroll contribution query successful.")
    print()
    print("Columns returned:")
    print(columns)
    print()
    print(f"Number of records returned: {len(rows)}")

except Exception as error:
    print("Payroll contribution query failed.")
    print(error)