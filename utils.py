import os


def get_module_paths():
    return [p for p in os.listdir() if os.path.isdir(p) and p[0] != "."]


def get_lesson_paths():
    paths = []
    modules = get_module_paths()
    for module in modules:
        lesson_names = [m for m in os.listdir(module)]
        lesson_names = [
            ln for ln in lesson_names if os.path.isdir(os.path.join(module, ln))
        ]

        for lesson in lesson_names:
            if lesson == "Extra":
                continue
            path = os.path.join(module, lesson)
            paths.append(path)
    return paths
