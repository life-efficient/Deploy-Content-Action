import yaml
from utils import (
    get_lesson_paths_in_module,
    get_meta,
    get_module_paths,
    get_quiz_path_in_lesson,
)
import os
import requests
import json
import sys

print(sys.argv)

API_ROOT = "https://pn4p83f4o6.execute-api.eu-west-1.amazonaws.com/prod"
# API_ROOT = "http://localhost:8000"


class Client:
    def create_or_update_unit(self, unit_meta):
        self._request(f"{API_ROOT}/content/unit", unit_meta)

    def create_or_update_module(self, module_meta):
        self._request(f"{API_ROOT}/content/module", module_meta)

    def create_or_update_lesson(self, lesson_meta):
        self._request(f"{API_ROOT}/content/lesson", lesson_meta)

    def create_or_update_quiz(self, quiz):
        self._request(f"{API_ROOT}/content/quiz", quiz)

    def _request(self, url, payload_yaml):
        response = requests.post(url, data=json.dumps(payload_yaml))
        print(response)


if __name__ == "__main__":

    client = Client()

    # CREAT UNIT ENTRY
    unit_meta = get_meta(".unit.yaml")
    # unit_meta["name"] = os.path.dirname(os.path.realpath(__file__)).split("/")[-1] # local
    unit_meta["name"] = (
        sys.argv[-1].split("/")[-1].replace("-Private", "")
    )  # folder name is passed in as cli arg and will be the private version
    assert "action.py" not in unit_meta["name"]
    client.create_or_update_unit(unit_meta)

    # CREATE MODULE ENTRIES
    for module_path in get_module_paths():
        module_meta = get_meta(os.path.join(module_path, ".module.yaml"))
        module_meta["name"] = module_path.split("/")[-1]
        module_meta["unit_id"] = unit_meta["id"]
        client.create_or_update_module(module_meta)

        lesson_paths = get_lesson_paths_in_module(module_path)

        # CREATE LESSON ENTRIES
        for lesson_path in lesson_paths:
            lesson_meta = get_meta(os.path.join(lesson_path, ".lesson.yaml"))
            lesson_meta["name"] = lesson_path.split("/")[-1]
            lesson_meta["module_id"] = module_meta["id"]
            client.create_or_update_lesson(lesson_meta)

            # CREATE QUIZ ENTRY
            quiz_path = get_quiz_path_in_lesson(lesson_path)
            with open(quiz_path) as f:
                quiz = yaml.safe_load(f)
            quiz["lesson_id"] = lesson_meta["id"]
            client.create_or_update_quiz(quiz)
