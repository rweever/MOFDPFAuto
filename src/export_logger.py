from datetime import datetime
from pathlib import Path


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "export_log.txt"


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

    No payroll contribution values or employee information
    are written to the log.
    """

    LOG_DIR.mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    service_value = service if service else "N/A"

    file_name = Path(output_file).name

    log_entry = (
        f"{timestamp} | "
        f"{payroll} | "
        f"{agency_code} | "
        f"{service_value} | "
        f"{record_count} records | "
        f"{file_name} | "
        f"{status}\n"
    )

    with LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as log_file:
        log_file.write(log_entry)