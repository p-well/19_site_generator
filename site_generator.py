from os.path import join
from collections import defaultdict, OrderedDict
from jinja2 import Environment, FileSystemLoader
from livereload import Server

import files_handler

INDEX_PATH = 'site/index.html'
CYCLOPEADIA_DIRPATH = 'site/articles'
CONFIG_PATH = 'config.json'
ARTICLE_TEMPLATE = 'article_template.html'
INDEX_TEMPLATE = 'index_template.html'


def render_index(env, config):
    unordered_content = defaultdict(list)
    for article in config['articles']:
        url = files_handler.create_article_url(article)
        unordered_content[article['topic']].append([article['title'], url])
    slugs_english, titles_russian = [], []
    for topic in config['topics']:
        slugs_english.append(topic['slug'])
        titles_russian.append(topic['title'])
    content_to_order = [
        (key, unordered_content.get(key)) for key in slugs_english
    ]
    ordered_content = OrderedDict(content_to_order)
    ordered_content_russian_titles = OrderedDict(
        zip(titles_russian, ordered_content.values())
    )
    rendered_index = env.get_template(INDEX_TEMPLATE).render(
            content=ordered_content_russian_titles
    )
    files_handler.write_html_file(INDEX_PATH, rendered_index)


def render_articles(env, config):
    for article in config['articles']:
        md_filepath = r'articles/{}'.format(article['source'])
        charset = files_handler.define_md_file_charset(md_filepath)
        markdown_obj = files_handler.read_md(md_filepath, charset)
        html_obj = files_handler.convert_md_to_html(markdown_obj)
        savename = files_handler.change_ext_from_md_to_html(article)
        savedir = article['source'].split('/')[0]
        savepath = join(CYCLOPEADIA_DIRPATH, savedir, savename)
        context = {
            'html': html_obj,
            'title': article['title'],
            'topic': article['topic']
        }
        rendered_article = env.get_template(ARTICLE_TEMPLATE).render(context)
        files_handler.write_html_file(savepath, rendered_article)


def make_site():
    config = files_handler.load_config_file(CONFIG_PATH)
    files_handler.constract_dir_tree(config, CYCLOPEADIA_DIRPATH)
    loader = FileSystemLoader('templates', followlinks=True)
    env = Environment(loader=loader)
    render_index(env, config)
    render_articles(env, config)


if __name__ == '__main__':
    make_site()
    server = Server()
    server.watch('templates/article_template.html', make_site)
    server.watch('templates/index_template.html', make_site)
    server.watch('articles/*/*.md', make_site)
    server.serve(root='site/')
