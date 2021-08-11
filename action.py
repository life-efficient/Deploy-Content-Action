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

# CHECK IF FORM EXISTS
exists = True
try:
    forms.get(quiz["id"])
except:
    exists = False
print("Exists?", exists)

# CREATE FORM IF IT DOESNT EXIST
forms.create(

# UPDATE FORM IF IT EXISTS
