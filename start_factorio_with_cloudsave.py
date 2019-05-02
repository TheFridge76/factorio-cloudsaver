import os
import os.path
import shutil
import re
import subprocess
import configparser

def get_saves(path, exclude_autosave = False):
    saves = list(filter(lambda x: x.endswith(".zip"), os.listdir(path)))
    if (exclude_autosave):
        saves = list(filter(lambda x: not x.startswith("_autosave"), saves))
    return saves

config = configparser.ConfigParser()
config.read("cloudsave.ini")
local_save_location = os.path.expandvars(config["locations"]["local"].strip('"'))
cloud_save_location = os.path.expandvars(config["locations"]["cloud"].strip('"'))
game_location = os.path.expandvars(config["locations"]["game"].strip('"'))
exclude_autosave = config.getboolean("options", "exclude_autosave")

cloud_saves = get_saves(cloud_save_location, exclude_autosave)
local_saves = get_saves(local_save_location, exclude_autosave)

for save in cloud_saves:
    if (save in local_saves):
        if (os.stat(os.path.join(local_save_location, save)).st_mtime + 30 < os.stat(os.path.join(cloud_save_location, save)).st_mtime):
            print("Cloud version of save " + save + " is more recent than local version. Replace the local save? (y/n)")
            selection = input()
            if (selection == "y"):
                shutil.copyfile(os.path.join(cloud_save_location, save), os.path.join(local_save_location, save))
                os.utime(os.path.join(cloud_save_location, save))
    else:
        shutil.copyfile(os.path.join(cloud_save_location, save), os.path.join(local_save_location, save))

subprocess.run(game_location)

cloud_saves = get_saves(cloud_save_location, exclude_autosave)
local_saves = get_saves(local_save_location, exclude_autosave)

for save in local_saves:
    if (save in cloud_saves):
        if (os.stat(os.path.join(cloud_save_location, save)).st_mtime + 30 < os.stat(os.path.join(local_save_location, save)).st_mtime):
            print("Local version of save " + save + " is more recent than cloud version. Replace the cloud save? (y/n)")
            selection = input()
            if (selection == "y"):
                shutil.copyfile(os.path.join(local_save_location, save), os.path.join(cloud_save_location, save))
                os.utime(os.path.join(local_save_location, save))
    else:
        shutil.copyfile(os.path.join(local_save_location, save), os.path.join(cloud_save_location, save))