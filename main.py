import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter_tooltip import ToolTip

import PyPDF2
from PIL import Image, ImageTk

from io import TextIOWrapper
import os
import re


class PDFselector(object):
    def __init__(self, master, information_pdf_name: str, column: int):
        self.raw_pdf = None
        self.pdf = None
        self.pdf_merge_num_pages = None
        self.pdf_original_range = None
        # self.merge_approval = None

        self.master = master
        # self.merge_approval = False
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
            # self.merge_approval = True
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
            # self.merge_approval = True
            # self.lock_unlock_merge_btn()

    def enable_text_box(self):
        if self.pdf_num_pages_checkbox_state.get() == 1:
            self.pdf_num_pages_text.config(state="normal")
            self.pdf_button_set_page_num.config(state="normal")
            self.deselect_checkbox(self.pdf_num_all_checkbox_state)
            # self.merge_approval = False
            # self.lock_unlock_merge_btn()
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
            self.first_pdf_merge_num_pages = pages_range
            # self.merge_approval = True
            # self.lock_unlock_merge_btn()

            filename = pdfname.cget("text")
            pdfname.config(text=f"{filename.split( )[0]} {pages_range}")
        else:
            messagebox.showwarning(title="Warning", message="Wrong pages range format.")

    def clear(self):
        self.raw_pdf = None
        self.pdf = None
        self.pdf_merge_num_pages = None
        # self.merge_approval = None
        self.pdf_num_pages_checkbox.config(state="disabled")
        self.pdf_num_all_checkbox.config(state="disabled")
        self.pdf_num_pages_text.delete(0, tk.END)
        self.pdf_num_pages_text.config(state="disabled")
        self.pdf_button_set_page_num.config(state="disabled")
        self.deselect_checkbox(self.pdf_num_all_checkbox_state)
        self.deselect_checkbox(self.pdf_num_pages_checkbox_state)
        self.pdfname.config(text="")


class PDFMerger:
    def __init__(self, master) -> None:
        # global raw_pdf_1
        # global pdf_1
        # global first_pdf_merge_num_pages
        # global first_pdf_original_range
        # global raw_pdf_2
        # global pdf_2
        # global second_pdf_merge_num_pages
        # global second_pdf_original_range
        # global frame
        # global merge_approval

        self.master = master
        # self.merge_approval = [False, False]
        master.title("PDF Merger")
        self.frame = ttk.Frame(self.master, width=660, height=300)
        self.frame.grid(columnspan=4, rowspan=7)

        # vars
        # self.first_pdf_num_all_checkbox_state = tk.IntVar()
        # self.first_pdf_num_pages_checkbox_state = tk.IntVar()
        # self.first_browse_text = tk.StringVar()
        # self.second_pdf_num_all_checkbox_state = tk.IntVar()
        # self.second_pdf_num_pages_checkbox_state = tk.IntVar()
        # self.second_browse_text = tk.StringVar()
        self.merge_text = tk.StringVar()

        # first instruction
        # self.first_instruction = ttk.Label(
        #     self.master,
        #     text="Select first PDF",
        #     font=12,
        # )

        # # first pdfname
        # self.first_pdfname = ttk.Label(self.master, text="")

        # # first pdf pages textbox
        # self.first_pdf_num_pages_text = ttk.Entry(
        #     self.master,
        #     width=10,
        #     state="disabled",
        # )

        # # first pdf pages set button
        # self.first_pdf_button_set_page_num = ttk.Button(
        #     self.master,
        #     text="Set",
        #     state="disabled",
        #     command=lambda: self.set_pdf_page_range(
        #         self.first_pdfname,
        #         self.first_pdf_num_pages_text,
        #         True,
        #     ),
        # )

        # # first pdf all pages checkbox
        # self.first_pdf_num_all_checkbox = ttk.Checkbutton(
        #     self.master,
        #     text="All",
        #     variable=self.first_pdf_num_all_checkbox_state,
        #     onvalue=1,
        #     offvalue=0,
        #     state="disabled",
        #     command=lambda: self.change_first_pages_checkbox_state(),
        # )

        # # first pdf particular pages checkbox
        # self.first_pdf_num_pages_checkbox = ttk.Checkbutton(
        #     self.master,
        #     text="Pages",
        #     variable=self.first_pdf_num_pages_checkbox_state,
        #     onvalue=1,
        #     offvalue=0,
        #     state="disabled",
        #     command=lambda: self.enable_first_text_box(),
        # )

        # # first browse button
        # self.first_browse_btn = ttk.Button(
        #     self.master,
        #     textvariable=self.first_browse_text,
        #     width=15,
        #     command=lambda: self.open_first_pdf(),
        #     style="Accent.TButton",
        # )
        # self.first_browse_text.set("Browse")

        # # pages textbox tooltip
        # ToolTip.createToolTip(
        #     self.first_pdf_num_pages_text,
        #     "Separate each page or range with a semicolon (such as '4; 7; 15-34; 56')",
        # )

        # # second instruction
        # self.second_instruction = ttk.Label(
        #     self.master,
        #     text="Select second PDF",
        #     font=12,
        # )

        # # second pdfname
        # self.second_pdfname = ttk.Label(self.master, text="")

        # # second pdf pages textbox
        # self.second_pdf_num_pages_text = ttk.Entry(
        #     self.master,
        #     width=10,
        #     state="disabled",
        # )

        # # second pdf pages set button
        # self.second_pdf_button_set_page_num = ttk.Button(
        #     self.master,
        #     text="Set",
        #     state="disabled",
        #     command=lambda: self.set_pdf_page_range(
        #         self.second_pdfname,
        #         self.second_pdf_num_pages_text,
        #         False,
        #     ),
        # )

        # # second pdf all pages checkbox
        # self.second_pdf_num_all_checkbox = ttk.Checkbutton(
        #     self.master,
        #     text="All",
        #     variable=self.second_pdf_num_all_checkbox_state,
        #     onvalue=1,
        #     offvalue=0,
        #     state="disabled",
        #     command=lambda: self.change_second_pages_checkbox_state(),
        # )

        # # second pdf particular pages checkbox
        # self.second_pdf_num_pages_checkbox = ttk.Checkbutton(
        #     self.master,
        #     text="Pages",
        #     variable=self.second_pdf_num_pages_checkbox_state,
        #     onvalue=1,
        #     offvalue=0,
        #     state="disabled",
        #     command=lambda: self.enable_second_text_box(),
        # )

        # # second pages textbox tooltip
        # ToolTip.createToolTip(
        #     self.second_pdf_num_pages_text,
        #     "Separate each page or range with a semicolon (such as '4; 7; 15-34; 56')",
        # )

        # # second browse button
        # self.second_browse_btn = ttk.Button(
        #     self.master,
        #     textvariable=self.second_browse_text,
        #     width=15,
        #     command=lambda: self.open_second_pdf(),
        #     style="Accent.TButton",
        # )
        # self.second_browse_text.set("Browse")

        # merge button
        self.merge_btn = ttk.Button(
            self.master,
            textvariable=self.merge_text,
            width=15,
            state="active",
            command=lambda: self.merge_pdfs(),
            style="Accent.TButton",
        )
        self.merge_text.set("Merge")

        # LAYOUT
        # self.first_instruction.grid(column=0, row=0)
        # self.first_pdfname.grid(column=0, row=1)
        # self.first_pdf_num_all_checkbox.grid(column=0, row=2)
        # self.first_pdf_num_pages_checkbox.grid(column=0, row=3)
        # self.first_pdf_num_pages_text.grid(column=0, row=4)
        # self.first_pdf_button_set_page_num.grid(column=0, row=5)
        # self.first_browse_btn.grid(column=0, row=6)

        # self.second_instruction.grid(column=1, row=0)
        # self.second_pdfname.grid(column=1, row=1)
        # self.second_pdf_num_all_checkbox.grid(column=1, row=2)
        # self.second_pdf_num_pages_checkbox.grid(column=1, row=3)
        # self.second_pdf_num_pages_text.grid(column=1, row=4)
        # self.second_pdf_button_set_page_num.grid(column=1, row=5)
        # self.second_browse_btn.grid(column=1, row=6)

        self.merge_btn.grid(column=2, row=3)

        first_selector = PDFselector(self.master, "first", 0)
        self.first_selector = first_selector
        second_selector = PDFselector(self.master, "second", 1)
        self.second_selector = second_selector

    # def open_first_pdf(self):
    #     self.first_browse_text.set("Loading...")
    #     self.raw_pdf_1 = askopenfilename(
    #         parent=self.master,
    #         title="Choose a pdf",
    #         filetypes=[("Pdf file", "*.pdf")],
    #     )
    #     if self.raw_pdf_1:
    #         read_pdf = PyPDF2.PdfFileReader(self.raw_pdf_1)
    #         first_pdfname_txt = os.path.basename(self.raw_pdf_1)
    #         self.first_pdf_original_range = read_pdf.getNumPages()
    #         self.first_pdf_merge_num_pages = self.first_pdf_original_range
    #         self.first_pdfname.config(text=first_pdfname_txt)
    #         self.pdf_1 = read_pdf
    #         self.first_pdf_num_pages_checkbox.config(state="normal")
    #         self.first_pdf_num_all_checkbox.config(state="normal")
    #         self.select_checkbox(self.first_pdf_num_all_checkbox_state)
    #         self.merge_approval[0] = True
    #     self.first_browse_text.set("Browse")

    # def deselect_checkbox(self, checkbox_state: bool):
    #     checkbox_state.set(0)

    # def select_checkbox(self, checkbox_state: bool):
    #     checkbox_state.set(1)

    # def lock_unlock_merge_btn(self):
    #     if self.merge_approval[0] and self.merge_approval[1]:
    #         self.merge_btn.config(state="active")
    #     else:
    #         self.merge_btn.config(state="disabled")

    # def change_first_pages_checkbox_state(self):
    #     if self.first_pdf_num_pages_checkbox_state.get() == 1:
    #         self.deselect_checkbox(self.first_pdf_num_pages_checkbox_state)
    #         self.first_pdf_num_pages_text.config(state="disabled")
    #         self.first_pdf_button_set_page_num.config(state="disabled")
    #         filename = self.first_pdfname.cget("text")
    #         self.first_pdfname.config(text=f"{filename.split( )[0]}")
    #         read_pdf = PyPDF2.PdfFileReader(self.raw_pdf_1)
    #         self.first_pdf_merge_num_pages = read_pdf.getNumPages()
    #         self.merge_approval[0] = True
    #         self.lock_unlock_merge_btn()

    # def change_second_pages_checkbox_state(self):
    #     if self.second_pdf_num_pages_checkbox_state.get() == 1:
    #         self.deselect_checkbox(self.second_pdf_num_pages_checkbox_state)
    #         self.second_pdf_num_pages_text.config(state="disabled")
    #         self.second_pdf_button_set_page_num.config(state="disabled")
    #         filename = self.second_pdfname.cget("text")
    #         self.second_pdfname.config(text=f"{filename.split( )[0]}")
    #         read_pdf = PyPDF2.PdfFileReader(self.raw_pdf_2)
    #         self.second_pdf_merge_num_pages = read_pdf.getNumPages()
    #         self.merge_approval[1] = True
    #         self.lock_unlock_merge_btn()

    # def enable_first_text_box(self):
    #     if self.first_pdf_num_pages_checkbox_state.get() == 1:
    #         self.first_pdf_num_pages_text.config(state="normal")
    #         self.first_pdf_button_set_page_num.config(state="normal")
    #         self.deselect_checkbox(self.first_pdf_num_all_checkbox_state)
    #         self.merge_approval[0] = False
    #         self.lock_unlock_merge_btn()
    #     else:
    #         self.first_pdf_num_pages_text.config(state="disabled")
    #         self.first_pdf_button_set_page_num.config(state="disabled")

    # def enable_second_text_box(self):
    #     if self.second_pdf_num_pages_checkbox_state.get() == 1:
    #         self.second_pdf_num_pages_text.config(state="normal")
    #         self.second_pdf_button_set_page_num.config(state="normal")
    #         self.deselect_checkbox(self.second_pdf_num_all_checkbox_state)
    #         self.merge_approval[1] = False
    #         self.lock_unlock_merge_btn()
    #     else:
    #         self.second_pdf_num_pages_text.config(state="disabled")
    #         self.second_pdf_button_set_page_num.config(state="disabled")
    #     if len(self.second_pdfname.cget("text").split()) < 2:
    #         self.merge_btn.config(state="disabled")

    # def open_second_pdf(self):
    #     self.second_browse_text.set("Loading...")
    #     self.raw_pdf_2 = askopenfilename(
    #         parent=self.master,
    #         title="Choose a pdf",
    #         filetypes=[("Pdf file", "*.pdf")],
    #     )
    #     if self.raw_pdf_2:
    #         read_pdf = PyPDF2.PdfFileReader(self.raw_pdf_2)
    #         second_pdfname_txt = os.path.basename(self.raw_pdf_2)
    #         self.second_pdf_original_range = read_pdf.getNumPages()
    #         self.second_pdf_merge_num_pages = self.second_pdf_original_range
    #         self.second_pdfname.config(text=second_pdfname_txt)
    #         self.pdf_2 = read_pdf
    #         self.second_pdf_num_pages_checkbox.config(state="normal")
    #         self.second_pdf_num_all_checkbox.config(state="normal")
    #         self.select_checkbox(self.second_pdf_num_all_checkbox_state)
    #         self.merge_approval[1] = True
    #         self.lock_unlock_merge_btn()
    #     if (
    #         self.pdf_1
    #         and self.pdf_2
    #         and self.merge_approval[0]
    #         and self.merge_approval[1]
    #     ):
    #         self.lock_unlock_merge_btn()
    #     self.second_browse_text.set("Browse")

    # def set_pdf_page_range(self, pdfname: str, pages_ranges: str, first: bool):
    #     pages_range = pages_ranges.get()
    #     pattern_letters = re.compile("[a-z]+")
    #     pattern_numbers = re.compile("[0-9]+")
    #     pattern_signs = re.compile("[;-]")
    #     if (
    #         pattern_letters.search(pages_range) is None
    #         and pattern_numbers.search(pages_range) is not None
    #         and pattern_signs.search(pages_range) is not None
    #     ):
    #         if first:
    #             pages_list = re.split("-|;", pages_range)
    #             for page in pages_list:
    #                 if int(page.strip()) > self.first_pdf_original_range:
    #                     return messagebox.showwarning(
    #                         title="Warning", message="Pages range exceeds PDF size."
    #                     )
    #             self.first_pdf_merge_num_pages = pages_range
    #             self.merge_approval[0] = True
    #             self.lock_unlock_merge_btn()
    #         else:
    #             pages_list = re.split("-|;", pages_range)
    #             for page in pages_list:
    #                 if int(page.strip()) > self.second_pdf_original_range:
    #                     return messagebox.showwarning(
    #                         title="Warning", message="Pages range exceeds PDF size."
    #                     )
    #             self.second_pdf_merge_num_pages = pages_range
    #             self.merge_approval[1] = True
    #             self.lock_unlock_merge_btn()

    #         filename = pdfname.cget("text")
    #         pdfname.config(text=f"{filename.split( )[0]} {pages_range}")
    #     else:
    #         messagebox.showwarning(title="Warning", message="Wrong pages range format.")

    # def clear(self):
    #     self.raw_pdf_1 = None
    #     self.pdf_1 = None
    #     self.first_pdf_merge_num_pages = None
    #     self.raw_pdf_2 = None
    #     self.pdf_2 = None
    #     self.second_pdf_merge_num_pages = None
    #     self.merge_approval = None
    #     self.first_pdf_num_pages_checkbox.config(state="disabled")
    #     self.first_pdf_num_all_checkbox.config(state="disabled")
    #     self.first_pdf_num_pages_text.delete(0, tk.END)
    #     self.first_pdf_num_pages_text.config(state="disabled")
    #     self.first_pdf_button_set_page_num.config(state="disabled")
    #     self.deselect_checkbox(self.first_pdf_num_all_checkbox_state)
    #     self.deselect_checkbox(self.first_pdf_num_pages_checkbox_state)
    #     self.first_pdfname.config(text="")
    #     self.second_pdf_num_pages_checkbox.config(state="disabled")
    #     self.second_pdf_num_all_checkbox.config(state="disabled")
    #     self.second_pdf_num_pages_text.delete(0, tk.END)
    #     self.second_pdf_num_pages_text.config(state="disabled")
    #     self.second_pdf_button_set_page_num.config(state="disabled")
    #     self.deselect_checkbox(self.second_pdf_num_all_checkbox_state)
    #     self.deselect_checkbox(self.second_pdf_num_pages_checkbox_state)
    #     self.second_pdfname.config(text="")
    #     # self.merge_btn.config(state="disabled")

    def merge_pdfs(self):
        merged_pdf = PyPDF2.PdfFileWriter()
        if self.first_selector.pdf is None or self.second_selector.pdf is None:
            return messagebox.showwarning(title="Warning", message="Select both PDFs.")
        if self.first_selector.pdf_num_pages_checkbox_state.get() == 0:
            for page_num in range(self.first_selector.pdf_merge_num_pages):
                page_obj = self.first_selector.pdf.getPage(page_num)
                merged_pdf.addPage(page_obj)
        else:
            if len(self.first_selector.pdfname.cget("text").split()) > 1:
                pages_list = self.first_selector.pdf_merge_num_pages.split(";")
                for pages in pages_list:
                    if "-" in pages:
                        pages_range_list = pages.split("-")
                        for page in range(
                            int(pages_range_list[0].strip()) - 1,
                            int(pages_range_list[1].strip()),
                        ):
                            page_obj = self.first_selector.pdf.getPage(page)
                            merged_pdf.addPage(page_obj)
                    else:
                        if pages:
                            page_obj = self.first_selector.pdf.getPage(
                                int(pages.strip()) - 1
                            )
                            merged_pdf.addPage(page_obj)
            else:
                return messagebox.showwarning(
                    title="Warning", message="Pages range is not set."
                )
        if self.second_selector.pdf_num_pages_checkbox_state.get() == 0:
            for page_num in range(self.second_selector.pdf_merge_num_pages):
                page_obj = self.second_selector.pdf.getPage(page_num)
                merged_pdf.addPage(page_obj)
        else:
            if len(self.second_selector.pdfname.cget("text").split()) > 1:
                pages_list = self.second_selector.pdf_merge_num_pages.split(";")
                for pages in pages_list:
                    if "-" in pages:
                        pages_range_list = pages.split("-")
                        for page in range(
                            int(pages_range_list[0].strip()) - 1,
                            int(pages_range_list[1].strip()),
                        ):
                            page_obj = self.second_selector.pdf.getPage(page)
                            merged_pdf.addPage(page_obj)
                    else:
                        if pages:
                            page_obj = self.second_selector.pdf.getPage(
                                int(pages.strip()) - 1
                            )
                            merged_pdf.addPage(page_obj)
            else:
                return messagebox.showwarning(
                    title="Warning", message="Pages range is not set."
                )
        f = asksaveasfile(
            mode="w", defaultextension=".pdf", filetypes=[("Pdf file", "*.pdf")]
        )
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        else:
            f.close()
        pdf_output_pdf = open(f.name, "wb")
        merged_pdf.write(pdf_output_pdf)
        pdf_output_pdf.close()
        messagebox.showinfo(title="Information", message="PDFs merged!")
        self.merge_btn.config(state="disabled")
        self.first_selector.clear()
        self.second_selector.clear()


root = tk.Tk()
root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "light")
ico = Image.open("pdf_blue.png")
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
mygui = PDFMerger(root)
root.minsize(660, 300)
root.maxsize(660, 300)
root.mainloop()
