import json
import uuid

def read_json_contents(file_path):
    with open(file_path) as f:
        return json.load(f)

def generate_uuid():
    return str(uuid.uuid4())