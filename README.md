# MOF DPF Payroll Export Utility

Application for automating DPF payroll contribution extraction and Microsoft Excel generation.

## Configuration Guidance

The application connects to the Ministry of Finance SQL Server environment using configuration values stored locally in a `.env` file. Database credentials are not stored directly in the Python source code and are excluded from the GitHub repository.

### 1. Prerequisites

The application requires:

* Python 3
* Visual Studio Code or another Python development environment
* Access to the authorised Ministry of Finance ICT environment
* Network access to the Payroll Data Warehouse
* Microsoft SQL Server ODBC driver
* Git for version control

### 2. Install Python Dependencies

From the project directory, run:

```powershell
python -m pip install -r requirements.txt
```

The application uses:

* `pyodbc` for Microsoft SQL Server connectivity
* `python-dotenv` for local configuration management
* `openpyxl` for Microsoft Excel generation

Tkinter is used for the desktop user interface and is normally included with standard Python installations.

### 3. Create the Local Environment File

A local `.env` file is required for database connectivity.

Create the file in the project root:

```text
MOFDPFAuto/

├── .env
├── .env.example
├── app.py
├── requirements.txt
├── assets/
├── logs/
├── output/
└── src/
```

Use `.env.example` as the configuration template.

The `.env` file should contain:

```text
DB_DRIVER=SQL Server
DB_SERVER=<database-server>
DB_DATABASE=<payroll-database>
DB_USER=<database-user>
DB_PASSWORD=<database-password>
```

Replace the placeholder values with the authorised database configuration for the environment in which the application is being executed.

### 4. Credential Protection

The `.env` file contains sensitive configuration information and must remain on the authorised local workstation.

It is excluded from Git version control through `.gitignore`.

Before committing changes, this can be verified using:

```powershell
git check-ignore .env
```

The expected result is:

```text
.env
```

The `.env.example` file may be stored in GitHub because it contains configuration placeholders only and no production credentials.

Generated payroll Excel files and operational export logs are also excluded from the repository.

### 5. Database Access

The application requires access to the Ministry of Finance Payroll Data Warehouse. Database access is intended to be read-only and is used only to retrieve payroll contribution information required for the export process.

The database referenced in the `.env` configuration must correspond with the payroll year being processed. For example, a 2026 payroll must be queried against the appropriate 2026 payroll database.

### 6. Run the Application

From the project root, run:

```powershell
python .\app.py
```

The Payroll Contribution Export interface will open.

The user then:

1. Enters the complete payroll parameter, for example `03726/0400`.
2. Selects Fire or Prison where Agency 037 is detected.
3. Selects **Generate Export**.
4. Reviews the system status and generated Microsoft Excel file.

Agency 010 and Agency 011 do not require a service selection.

### 7. Output

Successful processing generates a Microsoft Excel `.xlsx` file in the local `output` directory.

Example:

```text
output/

└── DPF_03726_0400_FIRE.xlsx
```

The `output` directory is excluded from GitHub because generated payroll contribution files may contain sensitive organisational information.

Successful exports are also recorded in a local activity log. The log captures:

* date and time of the export;
* payroll RunControl;
* agency code;
* agency or service label;
* number of records exported;
* generated file name; and
* export status.

Example:

```text
2026-09-15 10:56:06 | 01126/0700 | 011 | GDF | 2714 records | DPF_01126_0700.xlsx | SUCCESS
```

For Agency 037, the service is also identified in the log.

Example:

```text
2026-09-15 10:42:18 | 03726/0400 | 037 | MOHA Fire | 922 records | DPF_03726_0400_FIRE.xlsx | SUCCESS
```

The `logs` directory is excluded from GitHub so that operational activity records remain within the authorised Ministry of Finance environment.

### 8. Supported Agencies

The application supports:

* `010` — Guyana Police Force
* `011` — Guyana Defence Force
* `037` — Ministry of Home Affairs

Agency 037 requires the additional selection of either Fire or Prison to separate the relevant payroll contribution records.

The export activity log uses the following labels:

* `010` — GPF
* `011` — GDF
* `037` with Fire — MOHA Fire
* `037` with Prison — MOHA Prison

### 9. Current Application Limitation

The application requires access to the authorised Ministry of Finance ICT environment and Payroll Data Warehouse for live data retrieval. Therefore, database-dependent functionality cannot be reproduced outside that environment without appropriate authorised access and configuration.

The payroll database configured in the `.env` file must also correspond with the payroll year being processed.

A screen-recorded demonstration is maintained as contingency evidence of the working end-to-end application.
