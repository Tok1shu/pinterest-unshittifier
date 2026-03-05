import os
import random
import string
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

download_dir = os.path.expanduser("~/Downloads")
random_file_name_length = 8

os.chdir(download_dir)

files_extensions = [
    "jpg",
    "png",
    "jpeg",
    "gif",
    "webp"
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

def is_file_stable(filepath, delay=1):
    initial_size = -1
    while True:
        try:
            current_size = os.path.getsize(filepath)
            if current_size == initial_size and current_size > 0:
                return True
            initial_size = current_size
            time.sleep(delay)
        except OSError:
            return False

def process_once():
    no_ext_files = get_no_ext_files()
    for file in no_ext_files:
        filepath = os.path.join(download_dir, file)

        while not is_file_stable(filepath):
            if not os.path.exists(filepath):
                break

        if os.path.exists(filepath):
            new_name = generate_random_name()
            ext = infer_extension(file)
            rename_file(file, new_name)
            print(f"{file} -> {new_name}{ext}", flush=True)


class DownloadsHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_once()

    def on_moved(self, event):
        if not event.is_directory:
            process_once()

    def on_modified(self, event):
        if not event.is_directory:
            process_once()


def run_forever():
    process_once()

    event_handler = DownloadsHandler()
    observer = Observer()
    observer.schedule(event_handler, download_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    run_forever()
