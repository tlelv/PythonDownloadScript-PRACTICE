import os
import shutil
import time
import logging
from os.path import exists, splitext

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "/Users/treysonle/Downloads"
dest_dir_sfx = "/Users/treysonle/Desktop/Sound"
dest_dir_music = "/Users/treysonle/Desktop/Music"
dest_dir_video = "/Users/treysonle/Desktop/Downloaded Videos"
dest_dir_image = "/Users/treysonle/Desktop/Downloaded Images"

def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # If file exists, adds a number to the end of the filename
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        unique_name = makeUnique(dest, name)
        os.rename(entry, unique_name)
    shutil.move(entry, dest)

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:  #Loops all the files in the folder
                name =  entry.name
                dest = source_dir
                if name.endswith('.wav') or name.endswith('.mp3'):
                    if entry.stat().st_size < 25000000 or "SFX" in name:
                        dest = dest_dir_sfx
                    else:
                        dest = dest_dir_music
                    move(dest, entry, name)
                elif name.endswith('.mov') or name.endswith('.mp4'): #If file is a vide
                    dest = dest_dir_video
                    move(dest, entry, name)
                elif name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png'):
                    dest = dest_dir_image
                    move(dest, entry, name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()