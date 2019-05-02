import os
import yaml
from os import remove
from shutil import copy
from os.path import join, splitext
from markdown import markdown
from staticjinja import make_site

CWD = os.getcwd()
SETTINGS_FILE = os.environ['settings']
settings = yaml.load(open(SETTINGS_FILE).read())

OUTPUT_DIR = os.path.join(CWD, 'built/museo/')
TEMPLATE_DIR = os.path.join(CWD, 'source/templates/museum')
CONTENT_DIR = os.path.join(CWD, 'source/content/museum')

try:
    os.mkdir(OUTPUT_DIR)
except FileExistsError:
    pass


MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra'
]

SKIP_MARKDOWN = {"name"}


def build_context(content_dir, page):
    ctx = {}
    with open(join(content_dir, 'urna-%02d.md' % page), encoding='utf-8') as fh:
        section = "intro"
        section_lines = []
        for line in fh.readlines():
            if line.startswith(":"):
                if not section_lines:
                    section = line[1:].strip()
                    continue
                section_body = "\n".join(section_lines)
                if section not in SKIP_MARKDOWN:
                    section_body = markdown(section_body, extensions=MARKDOWN_EXTENSIONS)
                ctx[section] = section_body
                section = line[1:].strip()
                section_lines = []
            else:
                section_lines.append(line.strip())

        section_body = "\n".join(section_lines)
        ctx[section] = markdown(section_body, extensions=MARKDOWN_EXTENSIONS)

    ctx.update(settings['CTX'])
    return ctx


class copy_templates:
    def __init__(self):
        self.files = []

    def __enter__(self):
        total_urnas = range(1, 43)
        urn_base = join(TEMPLATE_DIR, 'urna.html')
        base, ext = splitext(urn_base)
        ctx = []
        urn_names = []
        for n in total_urnas:
            filename = 'urna-%02d%s' % (n, ext)
            new_name = join(TEMPLATE_DIR, filename)
            copy(urn_base, new_name)
            self.files.append(new_name)
            try:
                page_ctx = build_context(CONTENT_DIR, n)
                page_ctx.update({"number": "%02d" % n})
                ctx.append((filename, page_ctx))
                urn_names.append({
                    "name": page_ctx["name"],
                    "number": "%02d" % n,
                    "filename": filename
                })
            except FileNotFoundError:
                pass

        ctx.append(("index.html", {
            "urn_names": urn_names
        }))
        return ctx

    def __exit__(self, exc_type, exc_val, exc_tb):
        for fn in self.files:
            remove(fn)


def copy_contents():
    orig = join(CONTENT_DIR, "urna-01.md")
    for x in range(2, 43):
        dest = join(CONTENT_DIR, "urna-%02d.md" % x)
        copy(orig, dest)


if __name__ == '__main__':
    # copy_contents()
    with copy_templates() as contexts:
        site = make_site(
            searchpath=TEMPLATE_DIR,
            outpath=OUTPUT_DIR,
            contexts=contexts
        )
        site.render()
