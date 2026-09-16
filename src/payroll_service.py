AGENCY_NAMES = {
    "010": "Guyana Police Force",
    "011": "Guyana Defence Force",
    "037": "Ministry of Home Affairs"
}


def parse_payroll(payroll, service=None):
    """
    Parse and validate a payroll identifier.

    Example:
        03726/0400

    Agency Code: 037
    Year:        2026
    Period:      0400
    """

    payroll = payroll.strip().upper()

    # Validate basic payroll format
    if len(payroll) != 10 or payroll[5] != "/":
        raise ValueError(
            "Payroll must be entered in the format 03726/0400."
        )

    agency_code = payroll[:3]
    year_code = payroll[3:5]
    period_code = payroll[6:]

    # Validate individual components
    if not agency_code.isdigit():
        raise ValueError("Agency code must be numeric.")

    if not year_code.isdigit():
        raise ValueError("Payroll year must be numeric.")

    if not period_code.isdigit():
        raise ValueError("Payroll period must be numeric.")

    # Convert 26 to 2026
    year = f"20{year_code}"

    # Agencies supported by this application 
    supported_agencies = ("010", "011", "037")

    if agency_code not in supported_agencies:
        raise ValueError(
            f"Agency {agency_code} is not supported by this application."
        )

    # Get agency name
    agency_name = AGENCY_NAMES[agency_code]

    # Normalise service value
    if service:
        service = service.strip().upper()

    # Agency 037 must be separated into FIRE or PRISON
    if agency_code == "037":
        if service not in ("FIRE", "PRISON"):
            raise ValueError(
                "Agency 037 requires either FIRE or PRISON service."
            )

    # Service is not required for Agencies 010 and 011
    if agency_code in ("010", "011"):
        service = None

    return {
        "payroll": payroll,
        "agency_code": agency_code,
        "agency_name": agency_name,
        "year": year,
        "period": period_code,
        "service": service,
    }