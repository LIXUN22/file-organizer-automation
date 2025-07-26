import os
import shutil
import logging
from pathlib import Path
from collections import defaultdict

# Logging setup
logging.basicConfig(
    filename='file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# File type categories
FILE_TYPES = {
    'Documents': {
        '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages',
        '.xls', '.xlsx', '.csv', '.ppt', '.pptx', '.odp'
    },
    'Images': {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg',
        '.webp', '.ico', '.raw', '.heic', '.avif'
    },
    'Videos': {
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm',
        '.mkv', '.m4v', '.3gp', '.mpg', '.mpeg'
    },
    'Audio': {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma',
        '.m4a', '.opus', '.aiff'
    },
    'Archives': {
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz',
        '.tar.gz', '.tar.bz2'
    },
    'Code': {
        '.py', '.js', '.html', '.css', '.java', '.cpp', '.c',
        '.php', '.rb', '.go', '.rs', '.ts', '.jsx', '.vue'
    },
}

# Quick lookup: extension → category
EXT_TO_CATEGORY = {ext: cat for cat, exts in FILE_TYPES.items() for ext in exts}

def show_supported_file_types():
    print("\nSupported file types:")
    for category, extensions in FILE_TYPES.items():
        print(f"- {category}: {', '.join(sorted(extensions))}")
    print()

def organize_files(folder_path='.'):
    folder = Path(folder_path).resolve()
    moved_files = defaultdict(list)

    if not folder.exists() or not folder.is_dir():
        print("The path you entered is not a valid folder.")
        logging.error(f"Invalid directory: {folder}")
        return

    print(f"\nOrganizing files in: {folder}")
    logging.info(f"Started organizing files in: {folder}")

    try:
        for file in folder.iterdir():
            if file.is_file() and not file.name.startswith('.'):
                ext = file.suffix.lower()
                category = EXT_TO_CATEGORY.get(ext, 'Others')
                target_dir = folder / category

                try:
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_dir / file.name))
                    moved_files[category].append(file.name)
                    logging.info(f"Moved {file.name} to {category}/")
                except Exception as move_error:
                    print(f"Could not move {file.name}. Check logs for details.")
                    logging.error(f"Error moving {file.name}: {move_error}")

    except Exception as read_error:
        print("Something went wrong while reading files.")
        logging.exception(f"Directory read error: {read_error}")
        return

    # Summary
    print("\nFinished organizing. Here's what was moved:")
    for category, files in moved_files.items():
        print(f"\n{category} ({len(files)} file{'s' if len(files) != 1 else ''}):")
        for name in files:
            print(f"   └─ {name}")

    print("\nAll done.")
    logging.info("Organizing completed successfully.")

if __name__ == "__main__":
    print("Welcome to the File Organizer")
    show_supported_file_types()
    user_input = input("Enter the folder path you'd like to organize\n(leave blank for current folder): ").strip()
    organize_files(user_input or '.')
