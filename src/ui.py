import tkinter as tk

from src.payroll_service import parse_payroll


def update_service_options(event=None):
    """
    Enable Fire/Prison only when the payroll belongs to Agency 037.
    For all other payrolls, clear and disable the service options.
    """

    payroll = payroll_entry.get().strip()

    if payroll.startswith("037"):
        fire_radio.config(state="normal")
        prison_radio.config(state="normal")
    else:
        service_var.set("")
        fire_radio.config(state="disabled")
        prison_radio.config(state="disabled")


def generate_export():
    """
    Validate the payroll and service selection.

    Database retrieval and Excel generation will be added later.
    """

    payroll = payroll_entry.get().strip()
    service = service_var.get()

    if service == "":
        service = None

    try:
        result = parse_payroll(payroll, service)

        status_label.config(
            text=(
                f"Validated successfully.\n"
                f"Agency: {result['agency_name']} "
                f"({result['agency_code']}) | "
                f"Year: {result['year']} | "
                f"Service: {result['service'] or 'N/A'}"
            )
        )

    except ValueError as error:
        status_label.config(
            text=str(error)
        )


# --------------------------------------------------
# Main Application Window
# --------------------------------------------------

root = tk.Tk()

root.title("Payroll Contribution Export")
root.geometry("600x430")
root.resizable(False, False)


# --------------------------------------------------
# Application Title
# --------------------------------------------------

title_label = tk.Label(
    root,
    text="PAYROLL CONTRIBUTION EXPORT",
    font=("Arial", 16, "bold")
)
title_label.pack(
    pady=(25, 2)
)

subtitle_label = tk.Label(
    root,
    text="Ministry of Finance",
    font=("Arial", 11)
)
subtitle_label.pack(
    pady=(0, 25)
)


# --------------------------------------------------
# Payroll Input
# --------------------------------------------------

payroll_label = tk.Label(
    root,
    text="Payroll",
    font=("Arial", 10, "bold")
)
payroll_label.pack(
    anchor="w",
    padx=60
)

payroll_entry = tk.Entry(
    root,
    width=48,
    font=("Arial", 11)
)
payroll_entry.pack(
    padx=60,
    pady=(5, 20)
)

# Check payroll whenever the user types
payroll_entry.bind(
    "<KeyRelease>",
    update_service_options
)


# --------------------------------------------------
# Service Options
# --------------------------------------------------

service_label = tk.Label(
    root,
    text="Service (required for Agency 037 only)",
    font=("Arial", 10, "bold")
)
service_label.pack(
    anchor="w",
    padx=60
)

service_var = tk.StringVar(
    value=""
)

service_frame = tk.Frame(
    root
)
service_frame.pack(
    pady=10
)

fire_radio = tk.Radiobutton(
    service_frame,
    text="Fire",
    variable=service_var,
    value="FIRE",
    state="disabled"
)
fire_radio.pack(
    side="left",
    padx=20
)

prison_radio = tk.Radiobutton(
    service_frame,
    text="Prison",
    variable=service_var,
    value="PRISON",
    state="disabled"
)
prison_radio.pack(
    side="left",
    padx=20
)


# --------------------------------------------------
# Generate Button
# --------------------------------------------------

generate_button = tk.Button(
    root,
    text="Generate Export",
    command=generate_export,
    width=20
)
generate_button.pack(
    pady=25
)


# --------------------------------------------------
# Status Area
# --------------------------------------------------

status_title = tk.Label(
    root,
    text="Status",
    font=("Arial", 10, "bold")
)
status_title.pack(
    anchor="w",
    padx=60
)

status_label = tk.Label(
    root,
    text="Ready to generate.",
    relief="sunken",
    anchor="w",
    justify="left",
    width=62,
    height=3
)
status_label.pack(
    padx=60,
    pady=(5, 20)
)


# --------------------------------------------------
# Start Application
# --------------------------------------------------

root.mainloop()