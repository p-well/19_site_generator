import os
from os.path import basename, join, splitext


def get_files_list(path):
    files_list = []
    for dirpath, subdirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(dirpath, file)
            files_list.append((dirpath, file))
    return files_list

 
def choose_md_files(files_list):
    md_files_list = []
    for dirpath, file in files_list:
        if file.endswith('md'):
            md_files_list.append(join(dirpath, file))
    return md_files_list    
    
    
files = get_files_list('C:\Temp\kadantsev')
md_files = choose_md_files(files)
print(md_files)  
