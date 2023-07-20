import subprocess

mongotool = input("Inserire percorso mongorestore: ")
detections_folder = input("Inserire percorso cartella dump del database detections: ")
grifs_folder = input("Inserire percorso cartella dump del database gridfs: ")


commands = [mongotool + "\\mongorestore", "-d", "detections", detections_folder]
p = subprocess.Popen(commands, shell=True)
p.wait()

commands = [mongotool + "\\mongorestore", "-d", "gridfs", grifs_folder]
p = subprocess.Popen(commands, shell=True)
p.wait()


