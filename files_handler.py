import json
import chardet
import markdown
from os import makedirs
from os.path import basename, dirname, exists, join, splitext


CYCLOPEADIA_DIRPATH = 'site/articles'


def load_config_file(path):
    with open(path, 'r', encoding='utf-8') as json_obj:
        return json.load(json_obj)


def define_md_file_charset(path):
    with open(path, 'rb') as md_obj:
        return chardet.detect(md_obj.read()).get('encoding')


def read_md(filepath, charset):
    with open(filepath, 'r', encoding=charset) as md_obj:
        return md_obj.read()


def convert_md_to_html(md_obj):
    extensions = ['codehilite', 'extra', 'smarty']
    html_obj = markdown.markdown(
        md_obj,
        extensions=extensions,
        output_format='html5'
    )
    return html_obj


def change_ext_from_md_to_html(article_info):
    source = article_info['source']
    article_name, extention = splitext(basename(source))
    new_extention = 'html'
    savename = '{}.{}'.format(article_name, new_extention)
    return savename


def create_article_url(article_info):
    source = article_info['source']
    directory = dirname(source)
    html_name = change_ext_from_md_to_html(article_info)
    url = join(CYCLOPEADIA_DIRPATH, directory, html_name)
    print(url)
    return url


def constract_dir_tree(configs, site_basepath):
    for article in configs['articles']:
        topic_dir = article['source'].split('/')[0]
        if not exists(join(site_basepath, topic_dir)):
            makedirs(join(site_basepath, topic_dir), exist_ok=True)


def write_html_file(filepath, rendered_page):
    with open(filepath, mode='w', encoding='utf-8') as html_file:
        html_file.write(rendered_page)
