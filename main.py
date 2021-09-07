import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile
from widgets.tkinter_tooltip import ToolTip
from widgets.tkinter_PDFselector import PDFselector

import PyPDF2
from PIL import Image, ImageTk
import typing
import subprocess
import os
import platform

# TODO add readme
# TODO add license
# TODO add compiled file for win/linux


class PDFMerger:
    def __init__(self, master) -> None:

        self.master = master
        master.title("PDF Merger")
        self.frame = ttk.Frame(self.master, width=660, height=300)
        self.frame.grid(columnspan=4, rowspan=7)

        self.merge_text = tk.StringVar()

        canvas = tk.Canvas(self.master, width=200, height=100)
        canvas.grid(column=2, row=0, rowspan=5)

        img = Image.open("file.png")
        img = img.resize((150, 150))

        img = ImageTk.PhotoImage(img)
        logo_label = tk.Label(image=img)
        logo_label.image = img
        logo_label.grid(column=2, row=1, rowspan=4)

        # merge button
        self.merge_btn = ttk.Button(
            self.master,
            textvariable=self.merge_text,
            width=15,
            command=lambda: self.merge_pdfs(),
            style="Accent.TButton",
        )
        self.merge_text.set("Merge")

        # LAYOUT
        first_selector = PDFselector(self.master, "first", 0)
        self.first_selector = first_selector
        second_selector = PDFselector(self.master, "second", 1)
        self.second_selector = second_selector

        self.merge_btn.grid(column=2, row=5)

    def get_pdf_pages_to_merge(self, pdf_object: PDFselector, merged_pdf):
        if pdf_object.pdf_num_pages_checkbox_state.get() == 0:
            for page_num in range(pdf_object.pdf_merge_num_pages):
                page_obj = pdf_object.pdf.getPage(page_num)
                merged_pdf.addPage(page_obj)
            return True
        else:
            if len(pdf_object.pdfname.cget("text").split()) > 1:
                pages_list = pdf_object.pdf_merge_num_pages.split(";")
                for pages in pages_list:
                    if "-" in pages:
                        pages_range_list = pages.split("-")
                        for page in range(
                            int(pages_range_list[0].strip()) - 1,
                            int(pages_range_list[1].strip()),
                        ):
                            page_obj = pdf_object.pdf.getPage(page)
                            merged_pdf.addPage(page_obj)
                    else:
                        if pages:
                            page_obj = pdf_object.pdf.getPage(int(pages.strip()) - 1)
                            merged_pdf.addPage(page_obj)
                return True
            else:
                messagebox.showwarning(
                    title="Warning", message="Pages range is not set."
                )
                return False

    def merge_pdfs(self):
        merged_pdf = PyPDF2.PdfFileWriter()
        if self.first_selector.pdf is None or self.second_selector.pdf is None:
            return messagebox.showwarning(title="Warning", message="Select both PDFs.")
        if not self.get_pdf_pages_to_merge(
            self.first_selector, merged_pdf
        ) or not self.get_pdf_pages_to_merge(self.second_selector, merged_pdf):
            return
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
        self.first_selector.clear()
        self.second_selector.clear()
        if platform.system() == "Linux":
            subprocess.call(["xdg-open", pdf_output_pdf.name])
        else:
            os.startfile(pdf_output_pdf.name)


root = tk.Tk()
root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "light")
ico = Image.open("pdf_color.png")
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
mygui = PDFMerger(root)
root.minsize(660, 300)
root.maxsize(660, 300)
root.mainloop()
