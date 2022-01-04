import glob
import boto3
import yaml

def check_len(file:str, length:int=10) -> None:
    with open(file, mode='r') as f:
        questions = yaml.safe_load(f)['questions']
    if len(questions) < length:
        lesson = file.split('/')[1]
        print(f'"{lesson}" has less than {length} questions')

def get_lesson_id(file:str) -> str:
    with open(file, mode='r') as f:
        id = yaml.safe_load(f)['id']
    return id

if __name__ == '__main__':
    s3 = boto3.client('s3')
    q_files = glob.glob('[0-9]*/[0-9]*/.questions.yaml')
    # Lessons with questions
    lessons_with_qs = ['/'.join(q.split('/')[:2]) for q in q_files]
    lesson_files = [f + '/.lesson.yaml' for f in lessons_with_qs]
    ids = map(get_lesson_id, lesson_files)

    for id, file in zip(ids, q_files):
        check_len(file)
        s3.upload_file(file, 'aicore-questions', f'{id}.yaml')
