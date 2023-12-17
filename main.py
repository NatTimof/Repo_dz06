import sys
import scan
import shutil
import normalize
import re
from pathlib import Path


def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    #new_name = normalize.normalize(path.name.replace(".zip", ''))
    new_name = normalize.normalize(path.name) ###
    new_name = re.sub(r'(.zip|.gz|.tar)', '', new_name) ###
    
    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def new_folder_scan(child_folder):
    for item in folder.iterdir():
        if item.name == child_folder:
            child_folder_list = list()
            try:
                for child in item.iterdir():
                    child_folder_list.append(child.name)
            finally:
                    return child_folder_list


def main(folder_path):
    print(folder_path)
    scan.scan(folder_path)

    for file in scan.images_files:
        handle_file(file, folder_path, "images")

    for file in scan.documents_files:
        handle_file(file, folder_path, "documents")

    for file in scan.audio_files:
        handle_file(file, folder_path, "audio")

    for file in scan.video_files:
        handle_file(file, folder_path, "video")

    for file in scan.others:
        handle_file(file, folder_path, "other")

    for file in scan.archives:
        handle_archive(file, folder_path, "archives")
    
    remove_empty_folders(folder_path)



if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())

    print(f"images: {new_folder_scan("images")}")
    print(f"documents: {new_folder_scan("documents")}")
    print(f"audio: {new_folder_scan("audio")}")
    print(f"video: {new_folder_scan("video")}")
    print(f"unpacked archives: {new_folder_scan("archives")}")
    print(f"other: {new_folder_scan("other")}")
    print(f"All extensions: {scan.extensions}")
    print(f"Unknown extensions: {scan.unknown}")


#python main.py Temp