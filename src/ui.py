import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from src.payroll_service import parse_payroll
from src.payroll_query import fetch_contribution_data
from src.excel_export import generate_excel
from src.export_logger import log_export


# --------------------------------------------------
# Colours
# --------------------------------------------------

BG_COLOR = "#F0F2F5"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#1877F2"
PRIMARY_HOVER = "#166FE5"
TEXT_COLOR = "#1C1E21"
MUTED_TEXT = "#65676B"
BORDER_COLOR = "#DADDE1"
SUCCESS_COLOR = "#42B72A"
ERROR_COLOR = "#E41E3F"
STATUS_BG = "#F7F8FA"


# --------------------------------------------------
# Rounded Rectangle Helper
# --------------------------------------------------

def create_rounded_rectangle(
    canvas,
    x1,
    y1,
    x2,
    y2,
    radius=20,
    **kwargs
):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]

    return canvas.create_polygon(
        points,
        smooth=True,
        **kwargs
    )


# --------------------------------------------------
# Rounded Button
# --------------------------------------------------

class RoundedButton(tk.Canvas):

    def __init__(
        self,
        parent,
        text,
        command,
        width=540,
        height=50,
        radius=12
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=CARD_COLOR,
            highlightthickness=0,
            cursor="hand2"
        )

        self.command = command

        self.button_shape = create_rounded_rectangle(
            self,
            1,
            1,
            width - 1,
            height - 1,
            radius=radius,
            fill=PRIMARY_COLOR,
            outline=PRIMARY_COLOR
        )

        self.button_text = self.create_text(
            width / 2,
            height / 2,
            text=text,
            fill="#FFFFFF",
            font=("Segoe UI", 11, "bold")
        )

        self.tag_bind(
            self.button_shape,
            "<Button-1>",
            self._click
        )

        self.tag_bind(
            self.button_text,
            "<Button-1>",
            self._click
        )

        self.bind(
            "<Enter>",
            self._hover_on
        )

        self.bind(
            "<Leave>",
            self._hover_off
        )

    def _click(self, event=None):
        if self.command:
            self.command()

    def _hover_on(self, event=None):
        self.itemconfig(
            self.button_shape,
            fill=PRIMARY_HOVER,
            outline=PRIMARY_HOVER
        )

    def _hover_off(self, event=None):
        self.itemconfig(
            self.button_shape,
            fill=PRIMARY_COLOR,
            outline=PRIMARY_COLOR
        )


# --------------------------------------------------
# Service Behaviour
# --------------------------------------------------

def update_service_options(event=None):
    payroll = payroll_entry.get().strip()

    if payroll.startswith("037"):

        fire_radio.config(
            state="normal",
            fg=TEXT_COLOR
        )

        prison_radio.config(
            state="normal",
            fg=TEXT_COLOR
        )

    else:

        service_var.set("")

        fire_radio.config(
            state="disabled",
            fg=MUTED_TEXT
        )

        prison_radio.config(
            state="disabled",
            fg=MUTED_TEXT
        )


# --------------------------------------------------
# Status Behaviour
# --------------------------------------------------

def set_status(message, status_type="default"):

    if status_type == "success":
        text_color = SUCCESS_COLOR

    elif status_type == "error":
        text_color = ERROR_COLOR

    elif status_type == "processing":
        text_color = PRIMARY_COLOR

    else:
        text_color = TEXT_COLOR

    status_label.config(
        text=message,
        fg=text_color
    )


# --------------------------------------------------
# Generate Export
# --------------------------------------------------

def generate_export():

    payroll = payroll_entry.get().strip()
    service = service_var.get()

    if service == "":
        service = None

    try:

        payroll_info = parse_payroll(
            payroll,
            service
        )

        set_status(
            "Retrieving payroll contribution data...",
            "processing"
        )

        root.update_idletasks()

        columns, rows = fetch_contribution_data(
            payroll,
            service
        )

        if len(rows) == 0:

            set_status(
                "No payroll contribution records were found.",
                "error"
            )

            return

        output_file = generate_excel(
            columns,
            rows,
            payroll,
            service
        )

        log_export(
    payroll=payroll_info["payroll"],
    agency_code=payroll_info["agency_code"],
    service=payroll_info["service"],
    record_count=len(rows),
    output_file=output_file,
    status="SUCCESS"
)

        set_status(
            (
                "Contribution file generated successfully.\n"
                f"{payroll_info['agency_name']} "
                f"({payroll_info['agency_code']})  •  "
                f"{len(rows)} records"
            ),
            "success"
        )

        messagebox.showinfo(
            "Export Complete",
            (
                "Payroll contribution export completed successfully.\n\n"
                f"Records exported: {len(rows)}\n"
                f"File: {output_file}"
            )
        )

    except ValueError as error:

        set_status(
            str(error),
            "error"
        )

    except Exception as error:

        set_status(
            "Unable to generate payroll contribution file.",
            "error"
        )

        messagebox.showerror(
            "Export Error",
            (
                "The payroll contribution export "
                "could not be completed.\n\n"
                f"Details: {error}"
            )
        )


# --------------------------------------------------
# Main Window
# --------------------------------------------------

root = tk.Tk()

root.title(
    "Payroll Contribution Export"
)

root.geometry(
    "680x680"
)

root.resizable(
    False,
    False
)

root.configure(
    bg=BG_COLOR
)


# --------------------------------------------------
# Main Container
# --------------------------------------------------

main_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=45,
    pady=14
)


# --------------------------------------------------
# Header
# --------------------------------------------------

header_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

header_frame.pack(
    fill="x",
    pady=(0, 4)
)


# --------------------------------------------------
# Logo
# --------------------------------------------------

logo_path = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "logo.png"
)

try:

    logo_image = tk.PhotoImage(
        file=logo_path
    )

    logo_image = logo_image.subsample(
        3,
        4
    )

    logo_label = tk.Label(
        header_frame,
        image=logo_image,
        bg=BG_COLOR
    )

    logo_label.pack(
        pady=(0, 2)
    )

except tk.TclError:
    logo_image = None


# --------------------------------------------------
# Header Description
# --------------------------------------------------

description_label = tk.Label(
    header_frame,
    text="Generate DPF payroll contribution files",
    font=("Segoe UI", 10),
    fg=MUTED_TEXT,
    bg=BG_COLOR
)

description_label.pack(
    pady=(0, 4)
)


# --------------------------------------------------
# Rounded Main Card
# --------------------------------------------------

card_canvas = tk.Canvas(
    main_frame,
    width=590,
    height=315,
    bg=BG_COLOR,
    highlightthickness=0
)

card_canvas.pack(
    pady=(0, 6)
)

create_rounded_rectangle(
    card_canvas,
    2,
    2,
    588,
    313,
    radius=18,
    fill=CARD_COLOR,
    outline=BORDER_COLOR
)

card_content = tk.Frame(
    card_canvas,
    bg=CARD_COLOR
)

card_canvas.create_window(
    28,
    20,
    anchor="nw",
    window=card_content,
    width=534,
    height=270
)


# --------------------------------------------------
# Payroll
# --------------------------------------------------

payroll_label = tk.Label(
    card_content,
    text="Payroll Run Control",
    font=("Segoe UI", 11, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR
)

payroll_label.pack(
    anchor="w"
)


# --------------------------------------------------
# Rounded Payroll Input
# --------------------------------------------------

entry_canvas = tk.Canvas(
    card_content,
    height=46,
    bg=CARD_COLOR,
    highlightthickness=0
)

entry_canvas.pack(
    fill="x",
    pady=(8, 4)
)

create_rounded_rectangle(
    entry_canvas,
    1,
    1,
    532,
    44,
    radius=10,
    fill="#FFFFFF",
    outline=BORDER_COLOR
)

payroll_entry = tk.Entry(
    entry_canvas,
    font=("Segoe UI", 12),
    fg=TEXT_COLOR,
    bg="#FFFFFF",
    relief="flat",
    bd=0
)

entry_canvas.create_window(
    14,
    22,
    anchor="w",
    window=payroll_entry,
    width=500
)

payroll_entry.bind(
    "<KeyRelease>",
    update_service_options
)


payroll_example_label = tk.Label(
    card_content,
    text="Example: 03726/0400",
    font=("Segoe UI", 9),
    fg=MUTED_TEXT,
    bg=CARD_COLOR
)

payroll_example_label.pack(
    anchor="w",
    pady=(0, 16)
)


# --------------------------------------------------
# Service
# --------------------------------------------------

service_label = tk.Label(
    card_content,
    text="Service",
    font=("Segoe UI", 11, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR
)

service_label.pack(
    anchor="w"
)

service_helper = tk.Label(
    card_content,
    text="Required only for Agency 037",
    font=("Segoe UI", 9),
    fg=MUTED_TEXT,
    bg=CARD_COLOR
)

service_helper.pack(
    anchor="w",
    pady=(2, 7)
)


service_var = tk.StringVar(
    value=""
)

service_frame = tk.Frame(
    card_content,
    bg=CARD_COLOR
)

service_frame.pack(
    anchor="w",
    pady=(0, 12)
)


fire_radio = tk.Radiobutton(
    service_frame,
    text="Fire",
    variable=service_var,
    value="FIRE",
    state="disabled",
    font=("Segoe UI", 10),
    fg=MUTED_TEXT,
    bg=CARD_COLOR,
    activebackground=CARD_COLOR,
    selectcolor=CARD_COLOR,
    disabledforeground="#A0A0A0"
)

fire_radio.pack(
    side="left",
    padx=(0, 35)
)


prison_radio = tk.Radiobutton(
    service_frame,
    text="Prison",
    variable=service_var,
    value="PRISON",
    state="disabled",
    font=("Segoe UI", 10),
    fg=MUTED_TEXT,
    bg=CARD_COLOR,
    activebackground=CARD_COLOR,
    selectcolor=CARD_COLOR,
    disabledforeground="#A0A0A0"
)

prison_radio.pack(
    side="left"
)


# --------------------------------------------------
# Rounded Generate Button
# --------------------------------------------------

generate_button = RoundedButton(
    card_content,
    text="Generate Export",
    command=generate_export,
    width=534,
    height=50,
    radius=12
)

generate_button.pack()


# --------------------------------------------------
# Status Heading
# --------------------------------------------------

status_title = tk.Label(
    main_frame,
    text="Status",
    font=("Segoe UI", 11, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
)

status_title.pack(
    anchor="w",
    pady=(0, 4)
)


# --------------------------------------------------
# Rounded Status Card
# --------------------------------------------------

status_canvas = tk.Canvas(
    main_frame,
    width=590,
    height=78,
    bg=BG_COLOR,
    highlightthickness=0
)

status_canvas.pack(
    pady=(0, 4)
)

create_rounded_rectangle(
    status_canvas,
    2,
    2,
    588,
    76,
    radius=14,
    fill=STATUS_BG,
    outline=BORDER_COLOR
)


status_content = tk.Frame(
    status_canvas,
    bg=STATUS_BG
)

status_canvas.create_window(
    20,
    10,
    anchor="nw",
    window=status_content,
    width=545,
    height=52
)


status_label = tk.Label(
    status_content,
    text="Ready to generate.",
    font=("Segoe UI", 10),
    fg=TEXT_COLOR,
    bg=STATUS_BG,
    anchor="w",
    justify="left",
    wraplength=500
)

status_label.pack(
    fill="both",
    expand=True,
    padx=(5, 0),
    pady=(0, 0)
)


# --------------------------------------------------
# Start Application
# --------------------------------------------------

root.mainloop()