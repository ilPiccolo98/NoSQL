import glob
import subprocess
import shutil
import os

mongotool = input("Inserire percorso mongofiles: ")
dir_path = input("Inserire percorso dei file geoJson: ")


files = glob.glob1(dir_path, "*.json")
os.chdir(mongotool)


for file in files:
    if file != "bruxelles.json":
        shutil.copy(dir_path + "\\" + file, mongotool + "\\" + file)
        commands = [mongotool + "\\mongofiles", "-d", "gridfs", "put", file]
        subprocess.Popen(commands, shell=True).wait()
        os.remove(mongotool + "\\" + file)

