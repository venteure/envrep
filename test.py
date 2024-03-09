import os
import shutil
import unittest
from unittest.mock import patch
import tempfile
import filecmp
from pathlib import Path
from envrep import run


class TestDynamicEnvRep(unittest.TestCase):
    values = {
        "GREETINGS": "World",
        "ITEM1": "Apple",
        "ITEM2": "Banana",
        "ITEM3": "Cherry"
    }

    @patch.dict(os.environ, values)
    def test_dynamic_env_replication(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = Path(temp_dir) / "tests" / "test"
            goal_dir = Path(temp_dir) / "tests" / "goal"

            shutil.copytree("tests/test", test_dir)
            shutil.copytree("tests/goal", goal_dir)

            os.environ["INPUT_DIRECTORY"] = str(test_dir)

            run()

            mgs = "The output files do not match the expected results."
            self.assertTrue(self.compare_directories(test_dir, goal_dir), mgs)

    def compare_directories(self, dir1, dir2):
        """
            Compare two directories recursively.
            Files in each directory are assumed to be equal if their names and contents are equal.
        """
        dirs_cmp = filecmp.dircmp(dir1, dir2)
        if dirs_cmp.left_only or dirs_cmp.right_only or dirs_cmp.diff_files:
            return False
        for common_dir in dirs_cmp.common_dirs:
            new_dir1 = os.path.join(dir1, common_dir)
            new_dir2 = os.path.join(dir2, common_dir)
            if not self.compare_directories(new_dir1, new_dir2):
                return False
        return True


if __name__ == "__main__":
    unittest.main()
