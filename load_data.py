import glob
import subprocess

# mongotool address
mongotool = r'C:\Program Files\MongoDB\Tools\100\bin\mongoimport.exe'

# name of mongodb database
mydatabase = "detections"

# directory path containing the files to upload
dir_path = r'C:\Users\giuli\Desktop\ProgettoNoSQL\dataset_freight_transport_data'

# search all .csv files inside a specific folder
# *.csv means file name with .csv extension
files = glob.glob1(dir_path, "*.csv")

# import all files to mongodb
for file in files:
    commands = [mongotool, '--db', mydatabase,
                '--collection', file[:-4],
                '--file', dir_path + "\\" + file,
                '--type', 'csv',
                '--headerline']
    subprocess.Popen(commands, shell=True)
