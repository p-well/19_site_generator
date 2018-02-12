import json
import chardet
import markdown
from os import makedirs
from os.path import exists, join
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


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


def create_site_dirs_tree(config, site_basepath):
    topic_dir = config['source'].split('/')[0]
    if not exists(join(site_basepath, topic_dir)):
        makedirs(join(site_basepath, topic_dir), exist_ok=True)


def render_index_page(page_template, configs):
    index_page_content = defaultdict(list)
    for article in configs['articles']:
        article_filepath = join(
            'articles',
            article['source'].replace('md', 'html')
        )
        index_page_content[article['topic']].append(
            [article['title'],
             article_filepath]
        )
    loader = FileSystemLoader('templates', followlinks=True)
    env = Environment(loader=loader)
    template = env.get_template('{}'.format(page_template))
    return template.render(content=index_page_content)


def render_article_page(page_template, config, html_obj):
    loader = FileSystemLoader('templates', followlinks=True)
    env = Environment(loader=loader)
    template = env.get_template('{}'.format(page_template))
    content = {
        'html': html_obj,
        'title': config['title'],
        'topic': config['topic']
    }
    return template.render(content)


def create_index_page(site_basepath, rendered_page):
    index_html_filepath = join(site_basepath, 'index.html')
    with open(index_html_filepath, mode='w', encoding='utf-8') as html_file:
        html_file.write(rendered_page)


def create_article_page(site_basepath, rendered_page, config):
    article_md_name = config['source'].split('/')[1]
    article_html_name = article_md_name.replace('md', 'html')
    topic_dir = config['source'].split('/')[0]
    article_html_path = join(site_basepath, topic_dir, article_html_name)
    with open(article_html_path, mode='w', encoding='utf-8') as html_file:
        html_file.write(rendered_page)


if __name__ == '__main__':
    article_page_template = 'article_template.html'
    index_page_template = 'index_template.html'
    config_filepath = 'config.json'
    site_basepath = r'site\articles'
    configs = load_config_file(config_filepath)

    for config in configs['articles']:
        article_filepath = r'articles\{}'.format(config['source'])
        charset = define_md_file_charset(article_filepath)
        markdown_obj = read_md(article_filepath, charset)
        html_obj = convert_md_to_html(markdown_obj)
        create_site_dirs_tree(config, site_basepath)
        rendered_article_page = render_article_page(
            article_page_template,
            config,
            html_obj
        )
        create_article_page(
            site_basepath,
            rendered_article_page,
            config
        )
    rendered_index_page = render_index_page(index_page_template, configs)
    create_index_page(r'site', rendered_index_page)
