import os
import random
import string
import re

download_dir = os.path.expanduser("~/Downloads")
random_file_name_length = 8

os.chdir(download_dir)

files_extensions = [
    "jpg",
    "png",
    "jpeg",
    "gif"
]

def get_no_ext_files():
    no_ext_files = []
    for filename in os.listdir():
        if os.path.isfile(filename):
            name_part = filename.split('(')[0]

            if name_part in files_extensions:

                if filename == name_part or (
                        filename.startswith(name_part + '(') and
                        filename.endswith(')') and
                        filename[len(name_part) + 1:-1].isdigit()
                ): no_ext_files.append(filename)
    return no_ext_files


def infer_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    if ext:
        return ext

    m = re.fullmatch(r"([A-Za-z0-9]+)(?:\(\d+\))?", filename)
    if not m:
        return ""

    token = m.group(1).lower()
    if token in files_extensions:
        return "." + token

    return ""


def rename_file(file, new_name):
    ext = infer_extension(file)

    if os.path.splitext(new_name)[1]:
        target_name = new_name
    else:
        target_name = new_name + ext

    os.rename(
        os.path.join(download_dir, file),
        os.path.join(download_dir, target_name)
    )

def generate_random_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random_file_name_length))

if __name__ == "__main__":
    no_ext_files = get_no_ext_files()
    if no_ext_files:
        print("Files without extension:")
        for file in no_ext_files:
            new_name = generate_random_name()
            ext = infer_extension(file)
            rename_file(file, new_name)
            print(f" {file} -> {new_name}{ext}")
    else:
        print("No files without extension found.")