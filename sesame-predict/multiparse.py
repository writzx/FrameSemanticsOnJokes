import os

jokedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "jokes")

from predict_onepass import parse_file

def get_path(file):
    return os.path.join(jokedir, file)

files = []

for file in os.listdir(jokedir):
    if file.endswith(".txt"):
        files.append(get_path(file))

for file in files:
    parse_file(file, f"{os.path.splitext(file)[0]}-frames.frames")