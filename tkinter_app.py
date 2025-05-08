import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from delete_files import get_extensions, prompt_extensions_to_delete, delete_files, get_count_extensions
import os
import sys

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


HEADER_FONT = ("Segoe UI", 16, "bold")
NORMAL_FONT = ("Segoe UI", 12)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter App")
        self.geometry("500x600")
        self.resizable(False, False)
        self.extensions_checkboxes = dict()
        self.folder_path = ""

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Cleanup tool", font=HEADER_FONT)
        self.label.pack(pady=20)

        self.btn_select_folder = ctk.CTkButton(self, text="Select Folder", command=self.select_folder)
        self.btn_select_folder.pack()

        self.label_folder = ctk.CTkLabel(self, text="No folde selected", font=NORMAL_FONT)
        self.label_folder.pack(pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=400, height=300)
        self.scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.btn_delete = ctk.CTkButton(self, text="Delete Selected Files", command=self.delete_selected_files)
        self.btn_delete.pack(pady=10)

    def select_folder(self):
        self.folder_path = ctk.filedialog.askdirectory(title="Select Folder")
        if not self.folder_path:
            messagebox.showerror("Error", "No folder selected.", icon="error", detail="Please select a folder.", font=NORMAL_FONT)
            return
        self.label_folder.configure(text=f"Selected folder: {self.folder_path}")
        self.populate_extensions()

    def populate_extensions(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.extensions_checkboxes.clear()

        extensions = get_extensions(self.label_folder.cget("text").split(": ")[1])
        count_extensions = get_count_extensions(self.label_folder.cget("text").split(": ")[1])
        for ext in extensions:
            var = ctk.BooleanVar()
            count = count_extensions[ext]
            full_var_text = f"{ext} ({count})"
            
            checkbox = ctk.CTkCheckBox(self.scroll_frame, text=full_var_text, variable=var)
            checkbox.pack(anchor="w")
            self.extensions_checkboxes[ext] = var
        
    def delete_selected_files(self):
        if not self.folder_path:
            messagebox.showerror("Error", "No files have been selected asshole")
        selected_files = {ext for ext, var in self.extensions_checkboxes.items() if var.get()}
        if not selected_files:
            messagebox.showerror("Error", "No extensions selected.", icon="error", detail="Please select at least one extension.")
            
        print(selected_files)

        confirm = messagebox.askyesno("Info", "Are you sure you want to delete these files?")
        if not confirm:
            messagebox.showinfo("Info", "Operation cancelled.", icon="info", detail="No files deleted.")
            return
        delete_files(self.folder_path, selected_files)
        self.populate_extensions()
        messagebox.showinfo("Info", "Operation ended sucessfully, your files have been deleted, don't check your recycily bin it's gone for good",)
        
            



newApp = App()
newApp.mainloop()