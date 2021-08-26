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
import urllib.parse

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

    def create_or_update_challenge(self, challenge):
        self._request(f"{API_ROOT}/content/challenge", challenge)

    def _request(self, url, payload_yaml):
        response = requests.post(url, data=json.dumps(payload_yaml))
        print(response)
        assert response.status_code == 200


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

        # CREATE MODULE ENTRY
        module_meta = get_meta(os.path.join(module_path, ".module.yaml"))
        # print(module_meta)
        module_meta["name"] = module_path.split("/")[-1]
        module_meta["unit_id"] = unit_meta["id"]
        try:
            client.create_or_update_module(module_meta)
        except AssertionError:
            print(f'Creating module "{module_path}" failed')
            continue

        lesson_paths = get_lesson_paths_in_module(module_path)

        # CREATE LESSON ENTRIES
        for lesson_path in lesson_paths:
            lesson_meta = get_meta(os.path.join(lesson_path, ".lesson.yaml"))
            lesson_meta["name"] = lesson_path.split("/")[-1]
            lesson_meta["module_id"] = module_meta["id"]

            requires_notebook = True
            if "requires_notebook" in lesson_meta:
                requires_notebook = lesson_meta.pop(
                    "requires_notebook"
                )  # remove from meta

            # ADD STUDY GUIDE COL
            if os.path.exists(os.path.join(lesson_path, "Study Guide.md")):
                with open(os.path.join(lesson_path, "Study Guide.md"), "r") as f:
                    lesson_meta["study_guide"] = f.read()
            else:
                print(f'Study Guide.md not found for lesson "{lesson_path}"')

            # ADD NOTEBOOK COLAB LINK
            if os.path.exists(os.path.join(lesson_path, "Notebook.ipynb")):
                public_repo_name = sys.argv[-1].split("/")[-1].replace("-Private", "")
                colab_link = f"https://colab.research.google.com/github/life-efficient/{public_repo_name}/blob/main/{lesson_path}/Notebook.ipynb"
                colab_link = urllib.parse.quote(colab_link, safe="%/:")
                lesson_meta["notebook_url"] = colab_link

            # CREATE LESSON ENTRY
            try:
                client.create_or_update_lesson(lesson_meta)
            except AssertionError:
                print(f'Creating lesson "{lesson_path}" failed')
                continue

            # CREATE QUIZ ENTRY
            quiz_path = get_quiz_path_in_lesson(lesson_path)
            if os.path.exists(quiz_path):
                with open(quiz_path) as f:
                    quiz = yaml.safe_load(f)
                quiz["lesson_id"] = lesson_meta["id"]
                try:
                    client.create_or_update_quiz(quiz)
                except AssertionError:
                    print(f'Creating quiz "{quiz_path}" failed')
            else:
                print(f'Quiz not found for lesson "{lesson_path}"')

            # CREATE CHALLENGE ENTRIES
            if requires_notebook and os.path.exists(
                os.path.join(lesson_path, ".challenges.yaml")
            ):
                with open(os.path.join(lesson_path, ".challenges.yaml"), "r") as f:
                    challenges = yaml.safe_load(f)
                for challenge in challenges:
                    challenge["lesson_id"] = lesson_meta["id"]
                    try:
                        client.create_or_update_challenge(challenge)
                    except AssertionError:
                        print(f'Creating challenge "{challenge["name"]}" failed')
                        continue
            else:
                print(f'Challenges.yaml not found for lesson "{lesson_path}"')
            # with open
