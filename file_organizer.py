import os
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Set


class FileOrganizer:
    def __init__(self, target_directory: str = None):
        self.target_dir = Path(target_directory or Path.cwd())
        self.logger = self.setup_logging()
        self.file_types: Dict[str, Set[str]] = {
            'Documents': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages', '.xls', '.xlsx', '.csv', '.ppt', '.pptx', '.odp'},
            'Images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico', '.raw', '.heic', '.avif'},
            'Videos': {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v', '.3gp', '.mpg', '.mpeg'},
            'Audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.aiff'},
            'Archives': {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tar.gz', '.tar.bz2'},
            'Code': {'.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.rs', '.ts', '.jsx', '.vue'},
        }
        self.extension_map = {ext: category for category, exts in self.file_types.items() for ext in exts}

        self.stats = {
            'moved': 0,
            'skipped': 0,
            'errors': 0,
            'folders_created': 0
        }

    def setup_logging(self):
        logger = logging.getLogger("FileOrganizer")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler('file_organizer.log')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        return logger

    def get_category(self, file_path: Path) -> str:
        return self.extension_map.get(file_path.suffix.lower(), 'Others')

    def ensure_folder(self, folder: Path):
        if not folder.exists():
            folder.mkdir(parents=True)
            self.stats['folders_created'] += 1
            self.logger.info(f"Created folder: {folder}")

    def move_file(self, source: Path, destination: Path):
        try:
            if destination.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                destination = destination.with_name(f"{destination.stem}_{timestamp}{destination.suffix}")

            shutil.move(str(source), str(destination))
            self.stats['moved'] += 1
            self.logger.info(f"Moved: {source.name} → {destination.parent.name}/")
        except Exception as e:
            self.logger.error(f"Failed to move {source.name}: {e}")
            self.stats['errors'] += 1

    def organize(self, dry_run: bool = False) -> Dict[str, int]:
        if not self.target_dir.exists():
            self.logger.error(f"Directory does not exist: {self.target_dir}")
            return self.stats

        files = [f for f in self.target_dir.iterdir() if f.is_file()]
        self.logger.info(f"{'DRY RUN: ' if dry_run else ''}Found {len(files)} file(s) in {self.target_dir}")

        for file in files:
            if file.name.startswith('.') or file.name == 'file_organizer.log':
                self.stats['skipped'] += 1
                continue

            category = self.get_category(file)
            dest_folder = self.target_dir / category
            destination = dest_folder / file.name

            if dry_run:
                self.logger.info(f"[Dry Run] Would move: {file.name} → {category}/")
                continue

            self.ensure_folder(dest_folder)
            self.move_file(file, destination)

        return self.stats

    def print_summary(self):
        print("\n" + "=" * 40)
        print("📦 FILE ORGANIZATION SUMMARY")
        print("=" * 40)
        for key, value in self.stats.items():
            print(f"{key.capitalize():<17}: {value}")
        print("=" * 40)

    def show_supported_types(self):
        print("\nSupported File Types:")
        print("-" * 30)
        for category, extensions in self.file_types.items():
            print(f"{category:<10}: {', '.join(sorted(extensions))}")


def main():
    print("File Organizer - Minimalist Edition")
    print("=" * 40)

    target = input("Target directory (leave blank for current): ").strip()
    directory = target or os.getcwd()
    organizer = FileOrganizer(directory)

    if input("Show supported file types? (y/n): ").lower() == 'y':
        organizer.show_supported_types()

    dry_run = input("Do a dry run first? (y/n): ").lower() == 'y'
    stats = organizer.organize(dry_run=dry_run)
    organizer.print_summary()

    if dry_run and stats['moved'] == 0 and stats['errors'] == 0:
        if input("\nProceed with actual file move? (y/n): ").lower() == 'y':
            print("\nOrganizing files...")
            organizer.stats = {k: 0 for k in organizer.stats}
            organizer.organize(dry_run=False)
            organizer.print_summary()


if __name__ == "__main__":
    main()
