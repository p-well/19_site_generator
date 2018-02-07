import json
import chardet
import markdown
from os import mkdir
from os.path import exists, join, splitext
from jinja2 import Environment, FileSystemLoader


CONFIG_FILEPATH = '.\config.json'


def load_config_file(path):
    with open(path, 'r', encoding='utf-8') as json_obj:
        return json.load(json_obj)


def get_configs_from_file(config_json):
    configs = list()
    for article in config_json.get('articles'):
        article_config = dict()
        article_config['title'] = article.get('title')
        article_config['source'] = article.get('source')
        article_config['dir'] = article_config['source'].split('/')[0]
        article_config['filename'] = article_config['source'].split('/')[1]
        configs.append(article_config)
    return configs

print(get_configs_from_file(load_config_file(CONFIG_FILEPATH)))

def define_md_file_charset(path):
    with open(path,'rb') as md_obj:
        charset = chardet.detect(md_obj.read()).get('encoding')
        return charset


def read_md(filepath, charset):
    with open(filepath, 'r', encoding = charset) as md_obj:
        return md_obj.read()


def convert_md_to_html(md_obj):
    extensions = ['codehilite', 'extra', 'smarty']
    html = markdown.markdown(md_obj, extensions=extensions, output_format='html5')
    return html


def create_site_structure(current_article_config_dict):
    if not exists('site'):
        mkdir('site')
    dirpath = current_article_config_dict['dir']
    if not exists(('site/{}').format(dirpath)):
        mkdir('site/{}'.format(dirpath))


def save_converted_html(dirpath, html_obj):
    


if __name__ == '__main__':
    configs = get_configs_from_file(load_config_file(CONFIG_FILEPATH))
    for article_configs in configs:
        article_filepath = 'articles/{}'.format(article_configs.get('source'))
        charset = define_md_file_charset(article_filepath)
        markdown_obj = read_md(article_filepath, charset)
        html_obj = convert_md_to_html(markdown_obj)
        create_site_structure(article_configs)

