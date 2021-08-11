import unittest
import os
from unittest.case import skipIf
from parameterized import parameterized
import yaml


def testFails(test):
    """Evaluates whether a test fails - used for skipping tests"""
    try:
        test()
        return False
    except:
        return True


def get_module_paths():
    return [p for p in os.listdir() if os.path.isdir(p) and p[0] != "."]


def get_lesson_paths():
    paths = []
    modules = get_module_paths()
    for module in modules:
        # print("module:", module)
        lesson_names = [m for m in os.listdir(module)]
        lesson_names = [
            ln for ln in lesson_names if os.path.isdir(os.path.join(module, ln))
        ]

        for lesson in lesson_names:
            if lesson == "Extra":
                continue
            # print("lesson:", lesson)
            path = os.path.join(module, lesson)
            paths.append(path)
    # print(paths)
    return paths


class FileNamingConvention(unittest.TestCase):
    @parameterized.expand(get_module_paths())
    def test_module_numbered(self, module_path):
        try:
            assert module_path.split("/")[-1].split(".")[0].isdigit()
        except:
            raise NameError(f"Module not numbered ({module_path})")

    @parameterized.expand(get_lesson_paths())
    def test_lesson_numbered(self, lesson_path):
        try:
            assert lesson_path.split("/")[-1].split(".")[0].isdigit()
        except:
            raise NameError(f"Lesson not numbered ({lesson_path})")


class MissingMetaDataFiles(unittest.TestCase):
    @parameterized.expand(get_lesson_paths())
    def test_missing_lesson_meta_file(self, path):
        files = os.listdir(path)
        try:
            assert ".lesson.yaml" in files
        except:
            raise FileNotFoundError(
                f"Lesson meta file (`.lesson.yaml`) not found in {path}"
            )

    @parameterized.expand(get_module_paths())
    def test_missing_module_meta_file(self, module_path):
        files = os.listdir(module_path)
        try:
            assert ".module.yaml" in files
        except:
            raise FileNotFoundError(
                f"Module meta file (`.module.yaml`) not found in {module_path}"
            )

    def test_missing_unit_meta_file(self):
        files = os.listdir()
        try:
            assert ".unit.yaml" in files
        except:
            raise FileNotFoundError(
                "Unit meta file (`.unit.yaml`) not found in repository root"
            )


class FileContent(unittest.TestCase):
    def check_key(self, file_path, key):
        with open(file_path) as f:
            file_contents_yaml = yaml.safe_load(f)
        try:
            assert key in file_contents_yaml
        except:
            raise AssertionError(f"'{key}' key not found in {file_path}")

    def check_yaml_format(self, file_path, type_of_contents):
        with open(file_path) as f:
            file_contents_yaml = yaml.safe_load(f)
        try:
            assert type(file_contents_yaml) == type_of_contents
        except:
            raise AssertionError(f"{file_path} is not a {type_of_contents}")

    def check_meta_file_content(self, meta_file_directory, meta_file_name):
        module_meta_path = os.path.join(meta_file_directory, meta_file_name)
        self.check_key(module_meta_path, "description")
        self.check_yaml_format(module_meta_path, dict)

    def skip_if_file_doesnt_exist(self, fp):
        if os.path.exists(fp):
            pass
        else:
            self.skipTest(f"Test skipped as {fp} not found")

    @skipIf(
        testFails(MissingMetaDataFiles().test_missing_unit_meta_file),
        "Test skipped as `.unit.yaml` not found",
    )
    def test_unit_meta_content(self):
        self.check_key(".unit.yaml", "description")
        self.check_yaml_format(".unit.yaml", dict)

    @parameterized.expand(get_module_paths())
    def test_module_meta_content(self, module_path):
        self.skip_if_file_doesnt_exist(os.path.join(module_path, ".module.yaml"))
        self.check_meta_file_content(module_path, ".module.yaml")

    @parameterized.expand(get_lesson_paths())
    def test_lesson_meta_content(self, lesson_path):
        self.skip_if_file_doesnt_exist(os.path.join(lesson_path, ".lesson.yaml"))
        self.check_meta_file_content(lesson_path, ".lesson.yaml")


class MissingLessonContent(unittest.TestCase):
    # @parameterized.expand(get_lesson_paths())
    # def test_missing_quiz(self, lesson_path):
    #     files = os.listdir(lesson_path)
    #     try:
    #         assert ".quiz.yaml" in files
    #     except:
    #         raise FileNotFoundError('Quiz file not found')

    # @parameterized.expand(get_lesson_paths())
    # def test_missing_challenges(self, lesson_path):
    #     files = os.listdir(lesson_path)
    #     try:
    #         assert ".challenges.yaml" in files
    #     except:
    #         raise FileNotFoundError(
    #             f"Challenges file (`.challenges.yaml`) not found in {lesson_path}"
    #         )

    @parameterized.expand(get_lesson_paths())
    def test_missing_lesson(self, lesson_path):
        files = os.listdir(lesson_path)
        try:
            assert "Lesson.ipynb" in files
        except:
            raise FileNotFoundError(
                f"Lesson notebook (`Lesson.ipynb`) not found in {lesson_path}"
            )


class Challenges(unittest.TestCase):
    @parameterized.expand(get_lesson_paths())
    def test_challenges_length(lesson_path):
        """Tests enough challenges are in the .challenges.yaml file"""
        with open(os.path.join(lesson_path, ".challenges.yaml")) as f:
            challenges = yaml.safe_load(f)
        try:
            assert len(challenges) > 0
        except:
            raise AssertionError(
                f"Lesson {lesson_path} has no challenges in the .challenges.yaml file"
            )
        try:
            assert len(challenges) > 3
        except:
            raise AssertionError(
                f"Lesson {lesson_path} has too few challenges in the .challenges.yaml file"
            )


unittest.main(verbosity=2, exit=True)
