from os.path import join
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from livereload import Server

import files_handler

INDEX_PATH = 'site/index.html'
CYCLOPEADIA_DIRPATH = 'site/articles'
CONFIG_PATH = 'config.json'
ARTICLE_TEMPLATE = 'article_template.html'
INDEX_TEMPLATE = 'index_template.html'


def render_index(env, configs):
    index_content = defaultdict(list)
    for article in configs['articles']:
        path = join('articles', article['source'].replace('md', 'html'))
        index_content[article['topic']].append([article['title'], path])
    rendered_index = env.get_template(INDEX_TEMPLATE).render(
            content=index_content
        )
    files_handler.write_html_file(INDEX_PATH, rendered_index)


def render_articles(env, configs):
    for config in configs['articles']:
        article_filepath = r'articles/{}'.format(config['source'])
        charset = files_handler.define_md_file_charset(article_filepath)
        markdown_obj = files_handler.read_md(article_filepath, charset)
        html_obj = files_handler.convert_md_to_html(markdown_obj)
        savename = files_handler.change_ext_from_md_to_html(config['source'])
        savedir = config['source'].split('/')[0]
        savepath = join(CYCLOPEADIA_DIRPATH, savedir, savename)
        context = {
            'html': html_obj,
            'title': config['title'],
            'topic': config['topic']
        }
        rendered_article = env.get_template(ARTICLE_TEMPLATE).render(context)
        files_handler.write_html_file(savepath, rendered_article)


def make_site():
    configs = files_handler.load_config_file(CONFIG_PATH)
    files_handler.constract_dir_tree(configs, CYCLOPEADIA_DIRPATH)
    loader = FileSystemLoader('templates', followlinks=True)
    env = Environment(loader=loader)
    render_index(env, configs)
    render_articles(env, configs)


if __name__ == '__main__':
    make_site()
    server = Server()
    server.watch(ARTICLE_TEMPLATE, make_site)
    server.watch(INDEX_TEMPLATE, make_site)
    server.serve(root='site/')