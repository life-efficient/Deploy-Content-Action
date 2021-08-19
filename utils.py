import os
import yaml


def get_meta(filepath):
    print(filepath)
    with open(filepath) as f:
        meta = yaml.safe_load(f)
    return meta


def get_module_paths():
    return [
        p for p in os.listdir() if os.path.isdir(p) and p[0] != "." and p != "Extra"
    ]


def get_lesson_paths():
    paths = []
    modules = get_module_paths()
    for module_path in modules:
        lesson_paths = get_lesson_paths_in_module(module_path)
        paths.extend(lesson_paths)
    return paths


def get_lesson_paths_in_module(module_path):
    lesson_names = [m for m in os.listdir(module_path)]
    lesson_names = [
        ln for ln in lesson_names if os.path.isdir(os.path.join(module_path, ln))
    ]

    lesson_paths = []
    for lesson in lesson_names:
        if lesson == "Extra":
            continue
        path = os.path.join(module_path, lesson)
        lesson_paths.append(path)
    return lesson_paths


def get_quiz_path_in_lesson(lesson_path):
    return os.path.join(lesson_path, ".quiz.yaml")


def get_quiz_paths():
    lesson_folder_paths = get_lesson_paths()
    for lesson_folder_path in lesson_folder_paths:
        get_quiz_path_in_lesson(lesson_folder_path)
