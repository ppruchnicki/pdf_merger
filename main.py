from io import TextIOWrapper
import tkinter as tk
import PyPDF2
from tkinter.filedialog import askopenfile, asksaveasfile
import os


class PDFMerger:
    def __init__(self, master) -> None:
        global file1
        global first_num_pages
        global file2
        global second_num_pages
        global success_popup

        self.master = master
        master.title("PDF Merger")
        self.canvas = tk.Canvas(self.master, width=900, height=300)
        self.canvas.grid(columnspan=3, rowspan=7)

        # first instruction
        self.first_instruction = tk.Label(
            self.master, text="Select first PDF file to merge"
        )

        # first filename
        self.first_filename = tk.Label(self.master, text="")

        # first browse button
        self.first_browse_text = tk.StringVar()
        self.first_browse_btn = tk.Button(
            self.master,
            textvariable=self.first_browse_text,
            bg="black",
            fg="white",
            height=2,
            width=15,
            command=lambda: self.open_first_file(),
        )
        self.first_browse_text.set("Browse")

        # second instruction
        self.second_instruction = tk.Label(
            self.master, text="Select second PDF file to merge"
        )

        # second filename
        self.second_filename = tk.Label(self.master, text="")

        # second_page num selector
        self.second_file_num_all_checkbox_state = tk.IntVar()
        self.second_file_num_pages_checkbox_state = tk.IntVar()
        self.second_file_num_pages_text = tk.Text(
            self.master,
            height=1,
            width=10,
            state="disabled",
        )
        self.second_file_button_set_page_num = tk.Button(
            self.master,
            text="Set",
            state="disabled",
        )

        self.second_file_num_all_checkbox = tk.Checkbutton(
            self.master,
            text="All",
            variable=self.second_file_num_all_checkbox_state,
            onvalue=1,
            offvalue=0,
            state="disabled",
            command=lambda: self.change_pages_checkbox_state(),
        )
        self.second_file_num_pages_checkbox = tk.Checkbutton(
            self.master,
            text="Pages",
            variable=self.second_file_num_pages_checkbox_state,
            onvalue=1,
            offvalue=0,
            state="disabled",
            command=lambda: self.enable_text_box(),
        )

        # second browse button
        self.second_browse_text = tk.StringVar()
        self.second_browse_btn = tk.Button(
            self.master,
            textvariable=self.second_browse_text,
            bg="black",
            fg="white",
            height=2,
            width=15,
            command=lambda: self.open_second_file(),
        )
        self.second_browse_text.set("Browse")

        # merge button
        self.merge_text = tk.StringVar()
        self.merge_btn = tk.Button(
            self.master,
            textvariable=self.merge_text,
            bg="black",
            fg="white",
            height=2,
            width=15,
            state="disabled",
            command=lambda: self.merge_files(),
        )
        self.merge_text.set("Merge")

        # LAYOUT
        self.first_instruction.grid(column=0, row=0)
        self.first_filename.grid(column=0, row=1)
        self.first_browse_btn.grid(column=0, row=5)

        self.second_instruction.grid(column=1, row=0)
        self.second_filename.grid(column=1, row=1)
        self.second_file_num_all_checkbox.grid(column=1, row=2)
        self.second_file_num_pages_checkbox.grid(column=1, row=3)
        self.second_file_num_pages_text.grid(column=1, row=4)
        self.second_file_button_set_page_num.grid(column=1, row=5)
        self.second_browse_btn.grid(column=1, row=6)

        self.merge_btn.grid(column=2, row=3)

    def open_first_file(self):
        self.first_browse_text.set("Loading...")
        self.file1 = askopenfile(
            parent=root,
            mode="rb",
            title="Choose a file",
            filetypes=[("Pdf file", "*.pdf")],
        )
        if self.file1:
            read_pdf = PyPDF2.PdfFileReader(self.file1)
            first_filename_txt = os.path.basename(self.file1.name)
            self.first_num_pages = read_pdf.getNumPages()
            self.first_filename.config(text=first_filename_txt)
            self.file1 = read_pdf
        self.first_browse_text.set("Browse")

    def deselect_checkbox(self, checkbox):
        checkbox.deselect()

    def change_pages_checkbox_state(self):
        if self.second_file_num_pages_checkbox_state.get() == 1:
            self.deselect_checkbox(self.second_file_num_pages_checkbox)
            self.second_file_num_pages_text.config(state="disabled")
            self.second_file_button_set_page_num.config(state="disabled")

    def enable_text_box(self):
        if self.second_file_num_pages_checkbox_state.get() == 1:
            self.second_file_num_pages_text.config(state="normal")
            self.second_file_button_set_page_num.config(state="normal")
            self.deselect_checkbox(self.second_file_num_all_checkbox)
        else:
            self.second_file_num_pages_text.config(state="disabled")
            self.second_file_button_set_page_num.config(state="disabled")

    def open_second_file(self):
        self.second_browse_text.set("Loading...")
        self.file2 = askopenfile(
            parent=root,
            mode="rb",
            title="Choose a file",
            filetypes=[("Pdf file", "*.pdf")],
        )
        if self.file2:
            read_pdf = PyPDF2.PdfFileReader(self.file2)
            second_filename_txt = os.path.basename(self.file2.name)
            self.second_num_pages = read_pdf.getNumPages()
            self.second_filename.config(text=second_filename_txt)
            self.file2 = read_pdf
            self.second_file_num_pages_checkbox.config(state="normal")
            self.second_file_num_all_checkbox.config(state="normal")
            self.second_file_num_all_checkbox.select()
        if self.file1 and self.file2:
            self.merge_btn.config(state="normal")
        self.second_browse_text.set("Browse")

    def delete_popup(self):
        self.success_popup.destroy()

    def success(self):
        self.success_popup = tk.Toplevel(self.master)
        self.success_popup.geometry("250x80")
        self.success_popup.title("Information   ")
        tk.Label(self.success_popup, text="PDFs merged!", fg="green", pady=10).pack()
        tk.Button(self.success_popup, text="OK", command=self.delete_popup).pack()

    def merge_files(self):
        merged_file = PyPDF2.PdfFileWriter()
        for page_num in range(self.first_num_pages):
            page_obj = self.file1.getPage(page_num)
            merged_file.addPage(page_obj)
        for page_num in range(self.second_num_pages):
            page_obj = self.file2.getPage(page_num)
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
        self.success()


root = tk.Tk()
mygui = PDFMerger(root)
root.mainloop()
