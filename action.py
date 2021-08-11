import yaml
from typeform import Typeform

# GET CREDENTIALS
with open("creds.json") as f:
    token = yaml.safe_load(f)["typeform_token"]

# GET QUIZ YAML
quiz_file = "example_unit/0. First Module/0. First Module's First Lesson/.quiz.yaml"
with open(quiz_file) as f:
    quiz = yaml.safe_load(f)

# INITIALISE TYPEFORM CLIENT
tf = Typeform(token=token)
forms = tf.forms


def format_quiz(quiz):
    """Takes in our quiz format and converts it to that required by typeform"""
    with open("quiz_template.yaml") as f:
        template = yaml.safe_load(f)
    template["title"] = quiz["name"]
    template["fields"] = [
        {
            "ref": f"question-{q_idx}",
            "title": q["question"],
            "type": "multiple_choice",
            "properties": {
                "allow_multiple_selection": True,
                "choices": [
                    {"ref": f"option-{op_idx}", "label": option["option"]}
                    for op_idx, option in enumerate(q["options"])
                ],
            },
        }
        for q_idx, q in enumerate(quiz["questions"])
    ]

    return template


# GET ENTRIES OF EXISTING QUIZZES # TODO convert to actual SQL db
local_store_fp = "local_quiz_db_store.yaml"
with open(local_store_fp) as f:
    quiz_ids = yaml.safe_load(f)
print("quizzes", quiz_ids)
if not quiz_ids:
    quiz_ids = {}


def get_typeform_quiz_id(local_quiz_id):
    return quiz_ids[local_quiz_id]


# CHECK IF FORM EXISTS
try:
    typeform_quiz_id = get_typeform_quiz_id(
        quiz["id"]
    )  # check it exists in local storage
    forms.get(typeform_quiz_id)  # double check it exists in typeform
    exists = True
except KeyError:
    print("Form not in local db")
    exists = False
except:
    print("Form not in typeform")
    exists = False
print("Exists?", exists)

local_quiz_id = quiz.pop("id")

# def create_or_update_quiz(quiz):
# CREATE FORM IF IT DOESNT EXIST
if not exists:
    print("Creating", local_quiz_id)
    response = forms.create(format_quiz(quiz))
    typeform_quiz_id = response["id"]
    quiz_ids[local_quiz_id] = typeform_quiz_id
    with open(local_store_fp, "w") as f:
        yaml.dump(quiz_ids, f)

# UPDATE FORM IF IT EXISTS
else:
    print("Updating", local_quiz_id)
    # typeform_quiz_id = get_typeform_quiz_id(quiz["id"])
    response = forms.update(typeform_quiz_id, format_quiz(quiz))


# create_or_update_quiz(quiz)


# class Quiz:
#     def create_or_update():
#     def __update():
#     def __create(self):
