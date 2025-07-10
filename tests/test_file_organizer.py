import unittest
import os
from pathlib import Path
import shutil
from file_organizer import FileOrganizer

class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_dir")
        self.test_dir.mkdir(exist_ok=True)
        (self.test_dir / "test.txt").write_text("Sample document")
        (self.test_dir / "image.jpg").write_bytes(b"fake_image_data")
        (self.test_dir / "song.mp3").write_bytes(b"fake_audio_data")
        self.organizer = FileOrganizer(str(self.test_dir))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_organize_files(self):
        stats = self.organizer.organize(dry_run=False)
        self.assertGreater(stats['moved'], 0)
        self.assertTrue((self.test_dir / "Documents" / "test.txt").exists())
        self.assertTrue((self.test_dir / "Images" / "image.jpg").exists())
        self.assertTrue((self.test_dir / "Audio" / "song.mp3").exists())

    def test_dry_run(self):
        stats = self.organizer.organize(dry_run=True)
        self.assertEqual(stats['moved'], 0)

if __name__ == '__main__':
    unittest.main()
