import os
import yaml
from os.path import join
from markdown import markdown
from staticjinja import make_site

CWD = os.getcwd()
SETTINGS_FILE = os.environ['settings']
settings = yaml.load(open(SETTINGS_FILE).read())

OUTPUT_DIR = os.path.join(CWD, 'built/')
TEMPLATE_DIR = os.path.join(CWD, 'source/templates')
CONTENT_DIR = os.path.join(CWD, 'source/content')

try:
    os.mkdir(OUTPUT_DIR)
except FileExistsError:
    pass


MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra'
]


def build_context(content_dir):
    pages = [
        'home',
        'contact',
        'objectives',
        'sales',
        'community',
        'pic_of_the_month',
    ]
    ctx = {
        'pages': {}
    }
    for page in pages:
        with open(join(content_dir, '%s.md' % page), encoding='utf-8') as fh:
            body = fh.read()
            content = markdown(body, extensions=MARKDOWN_EXTENSIONS)
            ctx['pages'][page.replace('-', '_')] = content

    ctx.update(settings['CTX'])
    return ctx


if __name__ == '__main__':
    site = make_site(
        searchpath=TEMPLATE_DIR,
        outpath=OUTPUT_DIR,
        contexts=[('index.html', build_context(CONTENT_DIR))]
    )
    site.render()
