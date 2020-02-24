import os, shutil

for file in os.listdir('file/'):
    shutil.move(os.path.join("file/", file), "D:\\")
