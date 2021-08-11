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

# GET ENTRIES OF EXISTING QUIZZES # TODO convert to actual SQL db
local_store_fp = "local_quiz_db_store.yaml"
with open(local_store_fp) as f:
    quiz_ids = yaml.safe_load(f)
print("quizzes", quiz_ids)
if not quiz_ids:
    quiz_ids = {}

# CHECK IF FORM EXISTS
exists = True
try:
    typeform_quiz_id = quiz_ids[quiz["id"]]  # check it exists in local storage
    forms.get(typeform_quiz_id)  # double check it exists in typeform
except KeyError:
    print("Form not in local db")
    exists = False
except:
    print("Form not in typeform")
    exists = False
print("Exists?", exists)

local_quiz_id = quiz.pop("id")

# CREATE FORM IF IT DOESNT EXIST
if not exists:
    print("Creating", local_quiz_id)
    response = forms.create(quiz)
    typeform_quiz_id = response["id"]
    quiz_ids[local_quiz_id] = typeform_quiz_id
    with open(local_store_fp, "w") as f:
        yaml.dump(quiz_ids, f)

# UPDATE FORM IF IT EXISTS
else:
    print("Updating", local_quiz_id)
    response = forms.update(typeform_quiz_id, quiz)
