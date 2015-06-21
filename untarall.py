### untar only CSV files from local tar files 

import os
from os.path import join
import tarfile

folder = "."

for (dirname, dirs, files) in os.walk(folder):
    for filename in files:
        tar = tarfile.open(filename)
        for member in tar.getmembers():
            if os.path.splitext(member.name)[1] == ".csv":
                print(member)
                tar.extract(member)
        tar.close()
