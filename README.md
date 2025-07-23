# 📂 File Organizer

A simple yet powerful Python script that automatically organizes files in a folder based on their types (Documents, Images, Videos, Audio, Archives, Code, and Others).

This project helps you keep your folders neat by moving files into categorized subfolders automatically.  

---

## ✨ Features
- Categorizes files into:
  - **Documents** (PDF, Word, Excel, PowerPoint, etc.)
  - **Images** (JPG, PNG, SVG, etc.)
  - **Videos** (MP4, MKV, AVI, etc.)
  - **Audio** (MP3, WAV, FLAC, etc.)
  - **Archives** (ZIP, RAR, TAR, etc.)
  - **Code** (Python, HTML, Java, etc.)
  - **Others** (Anything else)
- **Logging:** Keeps a detailed log of all actions in `file_organizer.log`.
- **Error handling:** Notifies you if any file couldn’t be moved.
- **Customizable:** Easily add new file types or categories.
- **Backup friendly:** It does **not** overwrite files with the same name.

---

## 📁 Project Structure
File Organizer/
│
├── file_organizer.py # Main script
├── file_organizer.log # Log file (auto-created)
├── README.md # Project documentation
└── organized_files/ # Sample folder for testing

---

## 🛠 Requirements
- Python 3.6+
- Standard libraries: `os`, `shutil`, `logging`, `pathlib`, `collections`

---

## 🚀 How to Use

1. **Clone or Download** the repository:
   ```bash
   git clone https://github.com/LIXUN22/file-organizer-automation
   cd file-organizer


