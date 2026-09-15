from datetime import datetime
from pathlib import Path


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "export_log.txt"


def get_agency_label(agency_code, service=None):
    """
    Return a readable agency/service label for the export log.
    """

    if agency_code == "010":
        return "GPF"

    elif agency_code == "011":
        return "GDF"

    elif agency_code == "037":

        if service == "FIRE":
            return "MOHA Fire"

        elif service == "PRISON":
            return "MOHA Prison"

        return "MOHA"

    return agency_code


def log_export(
    payroll,
    agency_code,
    service,
    record_count,
    output_file,
    status="SUCCESS"
):
    """
    Record basic payroll export activity.

    Employee-level payroll contribution information
    is not written to the log.
    """

    LOG_DIR.mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    agency_label = get_agency_label(
        agency_code,
        service
    )

    file_name = Path(output_file).name

    log_entry = (
        f"{timestamp} | "
        f"{payroll} | "
        f"{agency_code} | "
        f"{agency_label} | "
        f"{record_count} records | "
        f"{file_name} | "
        f"{status}\n"
    )

    with LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as log_file:
        log_file.write(log_entry)