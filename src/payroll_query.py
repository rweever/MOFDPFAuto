from src.database import get_connection
from src.payroll_service import parse_payroll
from src.agency_config import AGENCY_CONFIG


def build_payroll_query(payroll_info):
    """
    Build the payroll contribution query using validated payroll information.

    Dynamic table names are derived only from the validated payroll value.
    User/configuration values are passed separately as SQL parameters.
    """

    payroll = payroll_info["payroll"]
    agency_code = payroll_info["agency_code"]
    agency_name = payroll_info["agency_name"]
    year = payroll_info["year"]
    service = payroll_info["service"]

    config = AGENCY_CONFIG[agency_code]

    main_pay_element = config["main_pay_element"]

    deduction_elements = config.get("deduction_pay_elements", [])

    # Support up to three optional pay-element removals.
    deductions = deduction_elements[:3]

    while len(deductions) < 3:
        deductions.append(None)

    deduct_pe1, deduct_pe2, deduct_pe3 = deductions

    # Safe table names derived from the already validated payroll.
    payroll_table_suffix = payroll.replace("/", "_")

    payelm_table = f"gogpaytb_{payroll_table_suffix}_PayElm"
    indv_table = f"gogpaytb_{year}_{agency_code}INDV"

    # Optional Agency 037 service filtering.
    service_filter = ""
    service_parameters = []

    if agency_code == "037":
        service_sections = config["services"][service]

        placeholders = ", ".join(
            ["?"] * len(service_sections)
        )

        service_filter = (
            f"\nAND HR.section IN ({placeholders})"
        )

        service_parameters.extend(service_sections)

    query = f"""
    SELECT
        ROW_NUMBER() OVER(ORDER BY PE_Max.emp_id) AS [Seq],

        ? AS [Ministry],

        HR.section AS [Section_Unit],

        PE_Max.emp_id AS [Employee Number],

        HR.surname AS [Last Name],

        HR.firstname AS [First Name],

        HR.middlename AS [Middle Name],

        PE.Ref AS [DPF Number],

        HR.gross
            - ISNULL(PE_DEDUCT1.Cur, 0)
            - ISNULL(PE_DEDUCT2.Cur, 0)
            - ISNULL(PE_DEDUCT3.Cur, 0)
        AS [Gross Salary],

        CAST(
            SUBSTRING(PE_Max.payroll, 7, 2)
            AS INT
        ) AS [Contribution Month],

        CASE SUBSTRING(PE_Max.payroll, 7, 2)
            WHEN '01' THEN 'January'
            WHEN '02' THEN 'February'
            WHEN '03' THEN 'March'
            WHEN '04' THEN 'April'
            WHEN '05' THEN 'May'
            WHEN '06' THEN 'June'
            WHEN '07' THEN 'July'
            WHEN '08' THEN 'August'
            WHEN '09' THEN 'September'
            WHEN '10' THEN 'October'
            WHEN '11' THEN 'November'
            WHEN '12' THEN 'December'
        END
        + '-20'
        + SUBSTRING(PE_Max.payroll, 4, 2)
        AS [Date Period],

        PE.ToDate AS [Contribution YTD],

        DATENAME(MONTH, PE.start_date)
        + '-'
        + CAST(YEAR(PE.start_date) AS VARCHAR(4))
        AS [Start_Cease],

        '' AS [Remarks]

    FROM
    (
        SELECT
            PAYELM.payroll,
            PAYELM.PayElmId,
            PAYELM.emp_id,
            MAX(PAYELM.eff_date) AS MAXeff_date

        FROM {payelm_table} PAYELM

        WHERE PAYELM.Cur <> 0
        AND PAYELM.PayElmId = ?

        GROUP BY
            PAYELM.payroll,
            PAYELM.PayElmId,
            PAYELM.emp_id

    ) PE_Max


    LEFT JOIN {indv_table} HR

        ON PE_Max.emp_id = HR.emp_id
        AND PE_Max.payroll = HR.payroll


    JOIN {payelm_table} PE

        ON PE_Max.emp_id = PE.emp_id
        AND PE_Max.payroll = PE.payroll
        AND PE_Max.MAXeff_date = PE.eff_date
        AND PE_Max.PayElmId = PE.PayElmId


    LEFT JOIN
    (
        SELECT
            payroll,
            PayElmId,
            emp_id,
            MAX(eff_date) AS MAXeff_date

        FROM {payelm_table}

        WHERE Cur <> 0
        AND PayElmId = ?

        GROUP BY
            payroll,
            PayElmId,
            emp_id

    ) PE_Max_DEDUCT1

        ON PE_Max.emp_id = PE_Max_DEDUCT1.emp_id
        AND PE_Max.payroll = PE_Max_DEDUCT1.payroll


    LEFT JOIN {payelm_table} PE_DEDUCT1

        ON PE_Max_DEDUCT1.emp_id = PE_DEDUCT1.emp_id
        AND PE_Max_DEDUCT1.payroll = PE_DEDUCT1.payroll
        AND PE_Max_DEDUCT1.MAXeff_date = PE_DEDUCT1.eff_date
        AND PE_Max_DEDUCT1.PayElmId = PE_DEDUCT1.PayElmId


    LEFT JOIN
    (
        SELECT
            payroll,
            PayElmId,
            emp_id,
            MAX(eff_date) AS MAXeff_date

        FROM {payelm_table}

        WHERE Cur <> 0
        AND PayElmId = ?

        GROUP BY
            payroll,
            PayElmId,
            emp_id

    ) PE_Max_DEDUCT2

        ON PE_Max.emp_id = PE_Max_DEDUCT2.emp_id
        AND PE_Max.payroll = PE_Max_DEDUCT2.payroll


    LEFT JOIN {payelm_table} PE_DEDUCT2

        ON PE_Max_DEDUCT2.emp_id = PE_DEDUCT2.emp_id
        AND PE_Max_DEDUCT2.payroll = PE_DEDUCT2.payroll
        AND PE_Max_DEDUCT2.MAXeff_date = PE_DEDUCT2.eff_date
        AND PE_Max_DEDUCT2.PayElmId = PE_DEDUCT2.PayElmId


    LEFT JOIN
    (
        SELECT
            payroll,
            PayElmId,
            emp_id,
            MAX(eff_date) AS MAXeff_date

        FROM {payelm_table}

        WHERE Cur <> 0
        AND PayElmId = ?

        GROUP BY
            payroll,
            PayElmId,
            emp_id

    ) PE_Max_DEDUCT3

        ON PE_Max.emp_id = PE_Max_DEDUCT3.emp_id
        AND PE_Max.payroll = PE_Max_DEDUCT3.payroll


    LEFT JOIN {payelm_table} PE_DEDUCT3

        ON PE_Max_DEDUCT3.emp_id = PE_DEDUCT3.emp_id
        AND PE_Max_DEDUCT3.payroll = PE_DEDUCT3.payroll
        AND PE_Max_DEDUCT3.MAXeff_date = PE_DEDUCT3.eff_date
        AND PE_Max_DEDUCT3.PayElmId = PE_DEDUCT3.PayElmId


    JOIN DBShrpn..location_descp LD

        ON HR.section = LD.loc_code


    WHERE HR.emp_status = 'A'

    AND HR.pv_no > 0

    AND HR.payroll = ?

    {service_filter}

    ORDER BY PE.emp_id ASC
    """

    parameters = [
        agency_name,
        main_pay_element,
        deduct_pe1,
        deduct_pe2,
        deduct_pe3,
        payroll,
    ]

    parameters.extend(service_parameters)

    return query, parameters


def fetch_contribution_data(payroll, service=None):
    """
    Validate the payroll, execute the contribution query,
    and return the column names and retrieved rows.
    """

    payroll_info = parse_payroll(
        payroll,
        service
    )

    query, parameters = build_payroll_query(
        payroll_info
    )

    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            query,
            parameters
        )

        columns = [
            column[0]
            for column in cursor.description
        ]

        rows = cursor.fetchall()

        return columns, rows

    finally:
        if connection is not None:
            connection.close()