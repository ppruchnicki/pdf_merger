import tkinter as tk
import PyPDF2
from tkinter.filedialog import askopenfile
import os


root = tk.Tk()

canvas = tk.Canvas(root, width=900, height=600)
canvas.grid(columnspan=3, rowspan=3)

# first instruction
first_instruction = tk.Label(root, text="Select first PDF file to merge")
first_instruction.grid(column=0, row=0)

# first filename
first_filename = tk.Label(root, text="")
first_filename.grid(column=0, row=1)


def open_first_file():
    first_browse_text.set("Loading...")
    file1 = askopenfile(
        parent=root, mode="rb", title="Choose a file", filetypes=[("Pdf file", "*.pdf")]
    )
    if file1:
        read_pdf = PyPDF2.PdfFileReader(file1)
        first_filename_txt = os.path.basename(file1.name)
        first_num_pages = read_pdf.getNumPages()
        first_filename.config(text=first_filename_txt)
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
first_browse_btn.grid(column=0, row=2)

# second instruction
second_instruction = tk.Label(root, text="Select second PDF file to merge")
second_instruction.grid(column=1, row=0)

# second filename
second_filename = tk.Label(root, text="")
second_filename.grid(column=1, row=1)


def open_second_file():
    second_browse_text.set("Loading...")
    file2 = askopenfile(
        parent=root, mode="rb", title="Choose a file", filetypes=[("Pdf file", "*.pdf")]
    )
    if file2:
        read_pdf = PyPDF2.PdfFileReader(file2)
        second_filename_txt = os.path.basename(file2.name)
        second_num_pages = read_pdf.getNumPages()
        second_filename.config(text=second_filename_txt)
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
second_browse_btn.grid(column=1, row=2)


def merge_files():
    pass


# merge button
merge_text = tk.StringVar()
merge_btn = tk.Button(
    root,
    textvariable=merge_text,
    bg="black",
    fg="white",
    height=2,
    width=15,
    command=lambda: merge_files(),
)
merge_text.set("Merge")
merge_btn.grid(column=2, row=2)

root.mainloop()
