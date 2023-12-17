import sys
from pathlib import Path

images_files = list()
documents_files = list()
audio_files = list()
video_files = list()
archives = list()
folders = list()
others = list()
unknown = set()
extensions = set()

known_extensions = ('JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX',
                    'MP3', 'OGG', 'WAV', 'AMR', 'ZIP', 'GZ', 'TAR')

registered_extensions = {
    'images': images_files,
    'documents': documents_files,
    'audio': audio_files,
    'video': video_files,
    'arch': archives
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('images', 'documents', 'audio', 'video', 'archives', 'other'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            # try:
                if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
                    images_files.append(new_name)
                if extension in ('AVI', 'MP4', 'MOV', 'MKV'):
                    video_files.append(new_name)
                if extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
                    documents_files.append(new_name)
                if extension in ('MP3', 'OGG', 'WAV', 'AMR'):
                    audio_files.append(new_name)
                if extension in ('ZIP', 'GZ', 'TAR'):
                    archives.append(new_name)
                if extension not in known_extensions:
                    unknown.add(extension)
                    others.append(new_name)

                extensions.add(extension)

            # except KeyError:
                # unknown.add(extension)
                # others.append(new_name)



if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    folder = Path(path)

    scan(folder)

    print(f"images: {images_files}")
    print(f"documents: {documents_files}")
    print(f"audio: {audio_files}")
    print(f"video: {video_files}")
    print(f"arch (archives): {archives}")
    print(f"unkown: {others}")
    print(f"All extensions: {extensions}")
    print(f"Unknown extensions: {unknown}")
    print(f"Folder: {folders}")



#python scan.py Temp


