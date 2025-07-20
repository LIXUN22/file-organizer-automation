import os
import shutil
from pathlib import Path
from collections import defaultdict

# Updated file type categories
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

def print_supported_types():
    print("Supported file types by category:\n")
    for category, extensions in FILE_TYPES.items():
        ext_list = ', '.join(sorted(extensions))
        print(f"  {category:<10} → {ext_list}")
    print()

def organize_files(folder_path='.'):
    folder = Path(folder_path).resolve()
    summary = defaultdict(list)

    if not folder.exists() or not folder.is_dir():
        print(" Invalid directory. Exiting.")
        return

    print(f"\nOrganizing files in: {folder}\n")

    for file in folder.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            moved = False
            for category, extensions in FILE_TYPES.items():
                if ext in extensions:
                    target_dir = folder / category
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_dir / file.name))
                    summary[category].append(file.name)
                    moved = True
                    break
            if not moved:
                target_dir = folder / 'Others'
                target_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(target_dir / file.name))
                summary['Others'].append(file.name)

    # Summary Report
    print(" Organizing Complete!\n")
    for category, files in summary.items():
        print(f" {category} - {len(files)} file(s)")
        for f in files:
            print(f"   └─ {f}")
    print("\n All done!")

# === Entry point ===
if __name__ == "__main__":
    print("\n Enhanced File Organizer")
    print_supported_types()
    user_path = input(" Enter the folder path to organize (default = current): ").strip()
    organize_files(user_path or '.')
