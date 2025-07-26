import os
import shutil
from pathlib import Path
from collections import defaultdict
import logging

import customtkinter as ctk
from tkinter import filedialog, messagebox

# File type mapping
FILE_TYPES = {
    "Documents": {".pdf", ".docx", ".txt", ".doc", ".xls", ".xlsx"},
    "Images": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
    "Videos": {".mp4", ".avi", ".mov"},
    "Audio": {".mp3", ".wav", ".flac"},
    "Archives": {".zip", ".rar", ".7z", ".tar"},
    "Code": {".py", ".js", ".html", ".css", ".cpp", ".c", ".java"},
}

EXT_TO_CATEGORY = {ext: cat for cat, exts in FILE_TYPES.items() for ext in exts}

# Logging setup
logging.basicConfig(
    filename='file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s — %(levelname)s — %(message)s',
    filemode='a'
)

class FileOrganizerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("700x650")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.folder_path = None
        self.moved_files = defaultdict(list)
        self.category_checks = {}
        self.category_dropdown_visible = False

        self.build_ui()

    def build_ui(self):
        self.header = ctk.CTkLabel(self, text="Smart File Organizer", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(pady=20)

        self.folder_btn = ctk.CTkButton(self, text="Select Folder", command=self.select_folder)
        self.folder_btn.pack()

        self.folder_label = ctk.CTkLabel(self, text="No folder selected", wraplength=500)
        self.folder_label.pack(pady=5)

        self.include_sub = ctk.CTkCheckBox(self, text="Include Subfolders")
        self.include_sub.pack(pady=5)

        self.dark_mode = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_theme)
        self.dark_mode.pack(pady=5)

        self.category_container = ctk.CTkFrame(self, fg_color="transparent")
        self.category_container.pack()

        self.category_btn = ctk.CTkButton(self.category_container, text="Select Categories ⮟", command=self.toggle_category_dropdown)
        self.category_btn.pack()

        self.category_frame = ctk.CTkFrame(self.category_container, fg_color="transparent")
        for category in FILE_TYPES.keys():
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(self.category_frame, text=category, variable=var)
            chk.pack(anchor="w", padx=10)
            self.category_checks[category] = var

        self.preview_btn = ctk.CTkButton(self, text="Preview Organization", command=self.preview_files)
        self.preview_btn.pack(pady=5)

        self.organize_btn = ctk.CTkButton(self, text="Organize Files", command=self.organize_files, fg_color="green")
        self.organize_btn.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, width=600, height=250)
        self.output_box.pack(pady=10)

        self.reset_btn = ctk.CTkButton(self, text="Undo Last Move", command=self.undo_move)
        self.reset_btn.pack(pady=5)

    def toggle_theme(self):
        mode = "dark" if self.dark_mode.get() else "light"
        ctk.set_appearance_mode(mode)

    def toggle_category_dropdown(self):
        if self.category_dropdown_visible:
            self.category_frame.pack_forget()
            self.category_btn.configure(text="Select Categories ⌄")
        else:
            self.category_frame.pack(pady=5)
            self.category_btn.configure(text="Select Categories ⌃")
        self.category_dropdown_visible = not self.category_dropdown_visible

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = Path(folder)
            self.folder_label.configure(text=f"Selected: {self.folder_path}")
            logging.info(f"Folder selected: {self.folder_path}")

    def get_all_files(self, path):
        return path.rglob("*") if self.include_sub.get() else path.iterdir()

    def preview_files(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        self.output_box.delete("0.0", "end")
        file_count = defaultdict(int)
        files = self.get_all_files(self.folder_path)

        for file in files:
            if file.is_file():
                ext = file.suffix.lower()
                category = EXT_TO_CATEGORY.get(ext, "Others")
                if category in self.category_checks and not self.category_checks[category].get():
                    continue
                file_count[category] += 1

        self.output_box.insert("end", "Preview:\n")
        for category, count in file_count.items():
            self.output_box.insert("end", f"  {category}: {count} file(s)\n")
            logging.info(f"Preview - {category}: {count} file(s)")

    def organize_files(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        self.moved_files.clear()
        self.output_box.delete("0.0", "end")
        files = self.get_all_files(self.folder_path)

        for file in files:
            if file.is_file() and not file.name.startswith("."):
                ext = file.suffix.lower()
                category = EXT_TO_CATEGORY.get(ext, "Others")
                if category in self.category_checks and not self.category_checks[category].get():
                    continue
                target_dir = self.folder_path / category
                target_dir.mkdir(exist_ok=True)

                try:
                    original_path = file
                    new_path = target_dir / file.name
                    shutil.move(str(file), str(new_path))
                    self.moved_files[category].append((new_path, original_path))
                    self.output_box.insert("end", f"Moved {file.name} → {category}/\n")
                    logging.info(f"Moved file: {file} → {new_path}")
                except Exception as e:
                    self.output_box.insert("end", f"Failed to move {file.name}: {e}\n")
                    logging.error(f"Failed to move {file}: {e}")

        self.output_box.insert("end", "\nOrganizing complete.\n")
        logging.info("Organizing complete.")

    def undo_move(self):
        if not self.moved_files:
            self.output_box.insert("end", "No recent move to undo.\n")
            logging.info("Undo attempted with no move history.")
            return

        for category, files in self.moved_files.items():
            for new_path, original_path in files:
                try:
                    original_parent = original_path.parent
                    original_parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(new_path), str(original_path))
                    self.output_box.insert("end", f"Restored {new_path.name}\n")
                    logging.info(f"Restored file: {new_path} → {original_path}")
                except Exception as e:
                    self.output_box.insert("end", f"Failed to restore {new_path.name}: {e}\n")
                    logging.error(f"Failed to restore {new_path}: {e}")

        self.moved_files.clear()
        self.output_box.insert("end", "\nUndo complete.\n")
        logging.info("Undo complete.")


if __name__ == "__main__":
    app = FileOrganizerGUI()
    app.mainloop()
