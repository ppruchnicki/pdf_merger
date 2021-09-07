import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile
from widgets.tkinter_tooltip import ToolTip

import PyPDF2

import os
import re
import typing


class PDFselector(object):
    def __init__(self, master, information_pdf_name: str, column: int):
        self.raw_pdf = None
        self.pdf = None
        self.pdf_merge_num_pages = None
        self.pdf_original_range = None

        self.master = master
        self.name = information_pdf_name
        self.column = column

        # vars
        self.pdf_num_all_checkbox_state = tk.IntVar()
        self.pdf_num_pages_checkbox_state = tk.IntVar()
        self.browse_text = tk.StringVar()

        # instruction
        self.instruction = ttk.Label(
            self.master,
            text=f"Select {self.name} PDF",
            font=12,
        )

        # pdfname
        self.pdfname = ttk.Label(self.master, text="")

        # pdf pages textbox
        self.pdf_num_pages_text = ttk.Entry(
            self.master,
            width=10,
            state="disabled",
        )

        # pdf pages set button
        self.pdf_button_set_page_num = ttk.Button(
            self.master,
            text="Set",
            state="disabled",
            command=lambda: self.set_pdf_page_range(
                self.pdfname,
                self.pdf_num_pages_text,
                True,
            ),
        )

        # pdf all pages checkbox
        self.pdf_num_all_checkbox = ttk.Checkbutton(
            self.master,
            text="All",
            variable=self.pdf_num_all_checkbox_state,
            onvalue=1,
            offvalue=0,
            state="disabled",
            command=lambda: self.change_pages_checkbox_state(),
        )

        # pdf particular pages checkbox
        self.pdf_num_pages_checkbox = ttk.Checkbutton(
            self.master,
            text="Pages",
            variable=self.pdf_num_pages_checkbox_state,
            onvalue=1,
            offvalue=0,
            state="disabled",
            command=lambda: self.enable_text_box(),
        )

        # browse button
        self.browse_btn = ttk.Button(
            self.master,
            textvariable=self.browse_text,
            width=15,
            command=lambda: self.open_pdf(),
            style="Accent.TButton",
        )
        self.browse_text.set("Browse")

        # pages textbox tooltip
        ToolTip.createToolTip(
            self.pdf_num_pages_text,
            "Separate each page or range with a semicolon (such as '4; 7; 15-34; 56')",
        )

        self.instruction.grid(column=self.column, row=0)
        self.pdfname.grid(column=self.column, row=1)
        self.pdf_num_all_checkbox.grid(column=self.column, row=2)
        self.pdf_num_pages_checkbox.grid(column=self.column, row=3)
        self.pdf_num_pages_text.grid(column=self.column, row=4)
        self.pdf_button_set_page_num.grid(column=self.column, row=5)
        self.browse_btn.grid(column=self.column, row=6)

    def open_pdf(self):
        self.browse_text.set("Loading...")
        self.raw_pdf = askopenfilename(
            parent=self.master,
            title="Choose a pdf",
            filetypes=[("Pdf file", "*.pdf")],
        )
        if self.raw_pdf:
            read_pdf = PyPDF2.PdfFileReader(self.raw_pdf)
            pdfname_txt = os.path.basename(self.raw_pdf)
            self.pdf_original_range = read_pdf.getNumPages()
            self.pdf_merge_num_pages = self.pdf_original_range
            self.pdfname.config(text=pdfname_txt)
            self.pdf = read_pdf
            self.pdf_num_pages_checkbox.config(state="normal")
            self.pdf_num_all_checkbox.config(state="normal")
            self.select_checkbox(self.pdf_num_all_checkbox_state)
        self.browse_text.set("Browse")

    def deselect_checkbox(self, checkbox_state: bool):
        checkbox_state.set(0)

    def select_checkbox(self, checkbox_state: bool):
        checkbox_state.set(1)

    def change_pages_checkbox_state(self):
        if self.pdf_num_pages_checkbox_state.get() == 1:
            self.deselect_checkbox(self.pdf_num_pages_checkbox_state)
            self.pdf_num_pages_text.config(state="disabled")
            self.pdf_button_set_page_num.config(state="disabled")
            filename = self.pdfname.cget("text")
            self.pdfname.config(text=f"{filename.split( )[0]}")
            read_pdf = PyPDF2.PdfFileReader(self.raw_pdf)
            self.first_pdf_merge_num_pages = read_pdf.getNumPages()

    def enable_text_box(self):
        if self.pdf_num_pages_checkbox_state.get() == 1:
            self.pdf_num_pages_text.config(state="normal")
            self.pdf_button_set_page_num.config(state="normal")
            self.deselect_checkbox(self.pdf_num_all_checkbox_state)
        else:
            self.pdf_num_pages_text.config(state="disabled")
            self.pdf_button_set_page_num.config(state="disabled")

    def set_pdf_page_range(self, pdfname: str, pages_ranges: str, first: bool):
        pages_range = pages_ranges.get()
        pattern_letters = re.compile("[a-z]+")
        pattern_numbers = re.compile("[0-9]+")
        pattern_signs = re.compile("[;-]")
        if (
            pattern_letters.search(pages_range) is None
            and pattern_numbers.search(pages_range) is not None
            and pattern_signs.search(pages_range) is not None
        ):
            pages_list = re.split("-|;", pages_range)
            for page in pages_list:
                if int(page.strip()) > self.pdf_original_range:
                    return messagebox.showwarning(
                        title="Warning", message="Pages range exceeds PDF size."
                    )
            self.pdf_merge_num_pages = pages_range

            filename = pdfname.cget("text")
            pdfname.config(text=f"{filename.split( )[0]} {pages_range}")
        else:
            messagebox.showwarning(title="Warning", message="Wrong pages range format.")

    def clear(self):
        self.raw_pdf = None
        self.pdf = None
        self.pdf_merge_num_pages = None
        self.pdf_num_pages_checkbox.config(state="disabled")
        self.pdf_num_all_checkbox.config(state="disabled")
        self.pdf_num_pages_text.delete(0, tk.END)
        self.pdf_num_pages_text.config(state="disabled")
        self.pdf_button_set_page_num.config(state="disabled")
        self.deselect_checkbox(self.pdf_num_all_checkbox_state)
        self.deselect_checkbox(self.pdf_num_pages_checkbox_state)
        self.pdfname.config(text="")
