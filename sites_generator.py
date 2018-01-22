import os
import json
from os.path import basename, join, splitext
import chardet
import markdown


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


def define_charset(path):
    with open(path,'rb') as md_file_obj:
        charset = chardet.detect(md_file_obj.read()).get('encoding')
        print(charset)
        return charset


def read_md(filepath, charset):
    with open(filepath, 'r', encoding = charset) as md_file_obj:
        return md_file_obj.read()


def convert_md_to_html(md_file_obj):
    html = markdown.markdown(md_file_obj)
    return html


def read_json(path):
    with open(path, 'r') as json_file_obj:
        return json.load(json_file_obj)




files = get_files_list('C:\projects\devman')
md_files = choose_md_files(files)
print(md_files)
for file in md_files:
    print(file)
    charset = define_charset(file)
    print(convert_md_to_html(read_md(file, charset)))