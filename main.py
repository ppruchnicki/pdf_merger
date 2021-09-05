import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile, asksaveasfile

import PyPDF2
from PIL import Image, ImageTk

from io import TextIOWrapper
import os
import re


class ToolTip(object):  # TODO send to other file
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", "8", "normal"),
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def createToolTip(widget, text):
        toolTip = ToolTip(widget)

        def enter(event):
            toolTip.showtip(text)

        def leave(event):
            toolTip.hidetip()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)


class PDFMerger:
    def __init__(self, master) -> None:
        global raw_pdf_1
        global pdf_1
        global first_num_pages
        global raw_pdf_2
        global pdf_2
        global second_num_pages
        global canvas

        self.master = master
        master.title("PDF Merger")
        self.canvas = tk.Canvas(self.master, width=900, height=300)
        self.canvas.grid(columnspan=3, rowspan=7)

        # vars

        self.first_pdf_num_all_checkbox_state = tk.IntVar()
        self.first_pdf_num_pages_checkbox_state = tk.IntVar()
        self.first_browse_text = tk.StringVar()
        self.second_pdf_num_all_checkbox_state = tk.IntVar()
        self.second_pdf_num_pages_checkbox_state = tk.IntVar()
        self.second_browse_text = tk.StringVar()
        self.merge_text = tk.StringVar()

        # first instruction
        self.first_instruction = tk.Label(
            self.master, text="Select first PDF file to merge"
        )

        # first pdfname
        self.first_pdfname = tk.Label(self.master, text="")

        # second pdf pages textbox
        self.first_pdf_num_pages_text = tk.Text(
            self.master,
            height=1,
            width=10,
            state="disabled",
        )

        # second pdf pages set button
        self.first_pdf_button_set_page_num = tk.Button(
            self.master,
            text="Set",
            state="disabled",
            command=lambda: self.set_pdf_page_range(
                self.first_pdfname,
                self.first_pdf_num_pages_text,
                True,
            ),
        )

        # second pdf all pages checkbox
        self.first_pdf_num_all_checkbox = tk.Checkbutton(
            self.master,
            text="All",
            variable=self.first_pdf_num_all_checkbox_state,
            onvalue=1,
            offvalue=0,
            state="disabled",
            command=lambda: self.change_first_pages_checkbox_state(),
        )

        # second pdf particular pages checkbox
        self.first_pdf_num_pages_checkbox = tk.Checkbutton(
            self.master,
            text="Pages",
            variable=self.first_pdf_num_pages_checkbox_state,
            onvalue=1,
            offvalue=0,
            state="disabled",
            command=lambda: self.enable_first_text_box(),
        )

        # first browse button
        self.first_browse_btn = tk.Button(
            self.master,
            textvariable=self.first_browse_text,
            bg="black",
            fg="white",
            height=2,
            width=15,
            command=lambda: self.open_first_pdf(),
        )
        self.first_browse_text.set("Browse")

        # pages textbox tooltip
        ToolTip.createToolTip(
            self.first_pdf_num_pages_text,
            "Range a-b, seperate pages/ranges divided by ';'",
        )

        # second instruction
        self.second_instruction = tk.Label(
            self.master, text="Select second PDF file to merge"
        )

        # second pdfname
        self.second_pdfname = tk.Label(self.master, text="")

        # second pdf pages textbox
        self.second_pdf_num_pages_text = tk.Text(
            self.master,
            height=1,
            width=10,
            state="disabled",
        )

        # second pdf pages set button
        self.second_pdf_button_set_page_num = tk.Button(
            self.master,
            text="Set",
            state="disabled",
            command=lambda: self.set_pdf_page_range(
                self.second_pdfname,
                self.second_pdf_num_pages_text,
                False,
            ),
        )

        # second pdf all pages checkbox
        self.second_pdf_num_all_checkbox = tk.Checkbutton(
            self.master,
            text="All",
            variable=self.second_pdf_num_all_checkbox_state,
            onvalue=1,
            offvalue=0,
            state="disabled",
            command=lambda: self.change_second_pages_checkbox_state(),
        )

        # second pdf particular pages checkbox
        self.second_pdf_num_pages_checkbox = tk.Checkbutton(
            self.master,
            text="Pages",
            variable=self.second_pdf_num_pages_checkbox_state,
            onvalue=1,
            offvalue=0,
            state="disabled",
            command=lambda: self.enable_second_text_box(),
        )

        # second pages textbox tooltip
        ToolTip.createToolTip(
            self.second_pdf_num_pages_text,
            "Range a-b, seperate pages/ranges divided by ';'",
        )

        # second browse button
        self.second_browse_btn = tk.Button(
            self.master,
            textvariable=self.second_browse_text,
            bg="black",
            fg="white",
            height=2,
            width=15,
            command=lambda: self.open_second_pdf(),
        )
        self.second_browse_text.set("Browse")

        # merge button
        self.merge_btn = tk.Button(
            self.master,
            textvariable=self.merge_text,
            bg="black",
            fg="white",
            height=12,
            width=15,
            state="disabled",
            command=lambda: self.merge_pdfs(),
        )
        self.merge_text.set("Merge")

        # LAYOUT
        self.first_instruction.grid(column=0, row=0)
        self.first_pdfname.grid(column=0, row=1)
        self.first_pdf_num_all_checkbox.grid(column=0, row=2)
        self.first_pdf_num_pages_checkbox.grid(column=0, row=3)
        self.first_pdf_num_pages_text.grid(column=0, row=4)
        self.first_pdf_button_set_page_num.grid(column=0, row=5)
        self.first_browse_btn.grid(column=0, row=6)

        self.second_instruction.grid(column=1, row=0)
        self.second_pdfname.grid(column=1, row=1)
        self.second_pdf_num_all_checkbox.grid(column=1, row=2)
        self.second_pdf_num_pages_checkbox.grid(column=1, row=3)
        self.second_pdf_num_pages_text.grid(column=1, row=4)
        self.second_pdf_button_set_page_num.grid(column=1, row=5)
        self.second_browse_btn.grid(column=1, row=6)

        self.merge_btn.grid(column=2, row=0, rowspan=7)

    def open_first_pdf(self):
        self.first_browse_text.set("Loading...")
        self.raw_pdf_1 = askopenfile(
            parent=root,
            mode="rb",
            title="Choose a pdf",
            filetypes=[("Pdf file", "*.pdf")],
        )
        if self.raw_pdf_1:
            read_pdf = PyPDF2.PdfFileReader(self.raw_pdf_1)
            first_pdfname_txt = os.path.basename(self.raw_pdf_1.name)
            self.first_num_pages = read_pdf.getNumPages()
            self.first_pdfname.config(text=first_pdfname_txt)
            self.pdf_1 = read_pdf
            self.first_pdf_num_pages_checkbox.config(state="normal")
            self.first_pdf_num_all_checkbox.config(state="normal")
            self.first_pdf_num_all_checkbox.select()
        self.first_browse_text.set("Browse")

    def deselect_checkbox(self, checkbox):
        checkbox.deselect()

    def change_first_pages_checkbox_state(self):
        if self.first_pdf_num_pages_checkbox_state.get() == 1:
            self.deselect_checkbox(self.first_pdf_num_pages_checkbox)
            self.first_pdf_num_pages_text.config(state="disabled")
            self.first_pdf_button_set_page_num.config(state="disabled")
            filename = self.first_pdfname.cget("text")
            self.first_pdfname.config(text=f"{filename.split( )[0]}")
            read_pdf = PyPDF2.PdfFileReader(self.raw_pdf_1)
            self.first_num_pages = read_pdf.getNumPages()

    def change_second_pages_checkbox_state(self):
        if self.second_pdf_num_pages_checkbox_state.get() == 1:
            self.deselect_checkbox(self.second_pdf_num_pages_checkbox)
            self.second_pdf_num_pages_text.config(state="disabled")
            self.second_pdf_button_set_page_num.config(state="disabled")
            filename = self.second_pdfname.cget("text")
            self.second_pdfname.config(text=f"{filename.split( )[0]}")
            read_pdf = PyPDF2.PdfFileReader(self.raw_pdf_2)
            self.second_num_pages = read_pdf.getNumPages()

    def enable_first_text_box(self):
        if self.first_pdf_num_pages_checkbox_state.get() == 1:
            self.first_pdf_num_pages_text.config(state="normal")
            self.first_pdf_button_set_page_num.config(state="normal")
            self.deselect_checkbox(self.first_pdf_num_all_checkbox)
        else:
            self.first_pdf_num_pages_text.config(state="disabled")
            self.first_pdf_button_set_page_num.config(state="disabled")

    def enable_second_text_box(self):
        if self.second_pdf_num_pages_checkbox_state.get() == 1:
            self.second_pdf_num_pages_text.config(state="normal")
            self.second_pdf_button_set_page_num.config(state="normal")
            self.deselect_checkbox(self.second_pdf_num_all_checkbox)
        else:
            self.second_pdf_num_pages_text.config(state="disabled")
            self.second_pdf_button_set_page_num.config(state="disabled")

    def open_second_pdf(self):
        self.second_browse_text.set("Loading...")
        self.raw_pdf_2 = askopenfile(
            parent=root,
            mode="rb",
            title="Choose a pdf",
            filetypes=[("Pdf file", "*.pdf")],
        )
        if self.raw_pdf_2:
            read_pdf = PyPDF2.PdfFileReader(self.raw_pdf_2)
            second_pdfname_txt = os.path.basename(self.raw_pdf_2.name)
            self.second_num_pages = read_pdf.getNumPages()
            self.second_pdfname.config(text=second_pdfname_txt)
            self.pdf_2 = read_pdf
            self.second_pdf_num_pages_checkbox.config(state="normal")
            self.second_pdf_num_all_checkbox.config(state="normal")
            self.second_pdf_num_all_checkbox.select()
        if self.pdf_1 and self.pdf_2:
            self.merge_btn.config(state="normal")
        self.second_browse_text.set("Browse")

    def set_pdf_page_range(self, pdfname, pages_ranges, first: bool):
        pages_range = pages_ranges.get("1.0", "end-1c")
        pattern_letters = re.compile("[a-z]+")
        pattern_numbers = re.compile("[0-9]+")
        pattern_signs = re.compile("[;-]")
        if (
            pattern_letters.search(pages_range) is None
            and pattern_numbers.search(pages_range) is not None
            and pattern_signs.search(pages_range) is not None
        ):
            filename = pdfname.cget("text")
            pdfname.config(text=f"{filename.split( )[0]} {pages_range}")
            if first:
                # TODO add checker if page is out of pdf page range throw warning
                self.first_num_pages = pages_range
            else:
                # TODO add checker if page is out of pdf page range
                self.second_num_pages = pages_range
        else:
            messagebox.showwarning(title="Warning", message="Wrong pages range format.")

    def clear(self):
        self.raw_pdf_1 = None
        self.pdf_1 = None
        self.first_num_pages = None
        self.raw_pdf_2 = None
        self.pdf_2 = None
        self.second_num_pages = None
        self.first_pdf_num_pages_checkbox.config(state="disabled")
        self.first_pdf_num_all_checkbox.config(state="disabled")
        self.first_pdf_num_pages_text.delete(1.0, tk.END)
        self.first_pdf_num_pages_text.config(state="disabled")
        self.first_pdf_button_set_page_num.config(state="disabled")
        self.first_pdf_num_all_checkbox.deselect()
        self.first_pdfname.config(text="")
        self.second_pdf_num_pages_checkbox.config(state="disabled")
        self.second_pdf_num_all_checkbox.config(state="disabled")
        self.second_pdf_num_pages_text.delete(1.0, tk.END)
        self.second_pdf_num_pages_text.config(state="disabled")
        self.second_pdf_num_all_checkbox.deselect()
        self.second_pdf_button_set_page_num.config(state="disabled")
        self.second_pdfname.config(text="")
        self.merge_btn.config(state="disabled")

    def merge_pdfs(self):
        merged_pdf = PyPDF2.PdfFileWriter()
        if self.first_pdf_num_pages_checkbox_state.get() == 0:
            for page_num in range(self.first_num_pages):
                page_obj = self.pdf_1.getPage(page_num)
                merged_pdf.addPage(page_obj)
        else:
            if len(self.first_pdfname.cget("text").split()) > 1:
                pages_list = self.first_num_pages.split(";")
                for pages in pages_list:
                    if "-" in pages:
                        pages_range_list = pages.split("-")
                        for page in range(
                            int(pages_range_list[0].strip()) - 1,
                            int(pages_range_list[1].strip()),
                        ):
                            page_obj = self.pdf_1.getPage(page)
                            merged_pdf.addPage(page_obj)
                    else:
                        if pages:
                            page_obj = self.pdf_1.getPage(int(pages.strip()) - 1)
                            merged_pdf.addPage(page_obj)
            else:
                return messagebox.showwarning(
                    title="Warning", message="Pages range is not set."
                )
        if self.second_pdf_num_pages_checkbox_state.get() == 0:
            for page_num in range(self.second_num_pages):
                page_obj = self.pdf_2.getPage(page_num)
                merged_pdf.addPage(page_obj)
        else:
            if len(self.second_pdfname.cget("text").split()) > 1:
                pages_list = self.second_num_pages.split(";")
                for pages in pages_list:
                    if "-" in pages:
                        pages_range_list = pages.split("-")
                        for page in range(
                            int(pages_range_list[0].strip()) - 1,
                            int(pages_range_list[1].strip()),
                        ):
                            page_obj = self.pdf_2.getPage(page)
                            merged_pdf.addPage(page_obj)
                    else:
                        if pages:
                            page_obj = self.pdf_2.getPage(int(pages.strip()) - 1)
                            merged_pdf.addPage(page_obj)
            else:
                return messagebox.showwarning(
                    title="Warning", message="Pages range is not set."
                )
        f = asksaveasfile(  # TODO change default location to root
            mode="w", defaultextension=".pdf", filetypes=[("Pdf file", "*.pdf")]
        )
        f.close()
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        pdf_output_pdf = open(f.name, "wb")
        merged_pdf.write(pdf_output_pdf)
        pdf_output_pdf.close()
        messagebox.showinfo(title="Information", message="PDFs merged!")
        self.clear()


root = tk.Tk()
ico = Image.open("pdf.png")
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
mygui = PDFMerger(root)
root.minsize(900, 300)
root.maxsize(900, 300)
root.mainloop()
