from io import TextIOWrapper
import tkinter as tk
import PyPDF2
from tkinter.filedialog import askopenfile, asksaveasfile
import os


root = tk.Tk()
root.title("PDF Merger")


canvas = tk.Canvas(root, width=900, height=300)
canvas.grid(columnspan=3, rowspan=7)

# first instruction
first_instruction = tk.Label(root, text="Select first PDF file to merge")
first_instruction.grid(column=0, row=0)

# first filename
first_filename = tk.Label(root, text="")
first_filename.grid(column=0, row=1)


def open_first_file():
    global file1
    global first_num_pages
    first_browse_text.set("Loading...")
    file1 = askopenfile(
        parent=root, mode="rb", title="Choose a file", filetypes=[("Pdf file", "*.pdf")]
    )
    if file1:
        read_pdf = PyPDF2.PdfFileReader(file1)
        first_filename_txt = os.path.basename(file1.name)
        first_num_pages = read_pdf.getNumPages()
        first_filename.config(text=first_filename_txt)
        file1 = read_pdf
    first_browse_text.set("Browse")


# first browse button
first_browse_text = tk.StringVar()
first_browse_btn = tk.Button(
    root,
    textvariable=first_browse_text,
    bg="black",
    fg="white",
    height=2,
    width=15,
    command=lambda: open_first_file(),
)
first_browse_text.set("Browse")
first_browse_btn.grid(column=0, row=5)

# second instruction
second_instruction = tk.Label(root, text="Select second PDF file to merge")
second_instruction.grid(column=1, row=0)

# second filename
second_filename = tk.Label(root, text="")
second_filename.grid(column=1, row=1)

# second_page num selector
second_file_num_all_state = tk.IntVar()
second_file_num_pages_state = tk.IntVar()


def change_pages_checkbox_state():
    second_file_num_pages_state.set(0)


second_file_num_all = tk.Checkbutton(
    root,
    text="All",
    variable=second_file_num_all_state,
    onvalue=1,
    offvalue=0,
    state="disabled",
    command=change_pages_checkbox_state(),
)
second_file_num_text = tk.Text(root, height=1, width=10, state="disabled")
second_file_num_text.grid(column=1, row=4)
second_file_button_set_page_num = tk.Button(
    root,
    text="Set",
    state="disabled",
)
second_file_button_set_page_num.grid(column=1, row=5)


def enable_text_box():
    second_file_num_text["state"] = "normal"
    second_file_button_set_page_num["state"] = "normal"
    second_file_num_all_state.set(0)


second_file_num_all.grid(column=1, row=2)

second_file_num_pages = tk.Checkbutton(
    root,
    text="Pages",
    variable=second_file_num_pages_state,
    onvalue=1,
    offvalue=0,
    state="disabled",
    command=enable_text_box(),
)
second_file_num_pages.grid(column=1, row=3)


def open_second_file():
    global file2
    global second_num_pages
    second_browse_text.set("Loading...")
    file2 = askopenfile(
        parent=root, mode="rb", title="Choose a file", filetypes=[("Pdf file", "*.pdf")]
    )
    if file2:
        read_pdf = PyPDF2.PdfFileReader(file2)
        second_filename_txt = os.path.basename(file2.name)
        second_num_pages = read_pdf.getNumPages()
        second_filename.config(text=second_filename_txt)
        file2 = read_pdf
        second_file_num_pages["state"] = "normal"
        second_file_num_all["state"] = "normal"
        second_file_num_all_state.set(1)
    if file1 and file2:
        merge_btn["state"] = "normal"
    second_browse_text.set("Browse")


# second browse button
second_browse_text = tk.StringVar()
second_browse_btn = tk.Button(
    root,
    textvariable=second_browse_text,
    bg="black",
    fg="white",
    height=2,
    width=15,
    command=lambda: open_second_file(),
)
second_browse_text.set("Browse")
second_browse_btn.grid(column=1, row=6)


def merge_files():
    merged_file = PyPDF2.PdfFileWriter()
    for page_num in range(first_num_pages):
        page_obj = file1.getPage(page_num)
        merged_file.addPage(page_obj)
    for page_num in range(second_num_pages):
        page_obj = file2.getPage(page_num)
        merged_file.addPage(page_obj)
    f = asksaveasfile(
        mode="w", defaultextension=".pdf", filetypes=[("Pdf file", "*.pdf")]
    )
    f.close()
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    pdf_output_file = open(f.name, "wb")
    merged_file.write(pdf_output_file)
    pdf_output_file.close()


# merge button
merge_text = tk.StringVar()
merge_btn = tk.Button(
    root,
    textvariable=merge_text,
    bg="black",
    fg="white",
    height=2,
    width=15,
    state="disabled",
    command=lambda: merge_files(),
)
merge_text.set("Merge")
merge_btn.grid(column=2, row=3)

root.mainloop()
