import os
import shutil
import re
from pathlib import Path

from block_markdown import markdown_to_html_node

def copy_to_dir(src, dst):
    if not os.path.exists(src):
        raise Exception("source directory not found")
    if not os.path.exists(dst):
        raise Exception("destination directory not found")
    
    dest_content = os.listdir(dst)
    if dest_content:
        shutil.rmtree(dst)
        os.makedirs(dst)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        if os.path.isfile(src_path):
            shutil.copy(src_path,dst_path)
            print(f"LOG: copyed {src_path} to {dst_path}")
        else:
            os.makedirs(dst_path)
            print(f"LOG: created new folder {dst_path}")
            copy_to_dir(src_path, dst_path)

def extract_title(markdown):
    if not re.match(r"^#\s+.+", markdown):
        raise Exception("invalid title format")
    return markdown.splitlines()[0].replace("# ", "", 1)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as file:
        md_content = file.read()
    
    with open(template_path) as file:
        template_content = file.read()

    html_final = (
        template_content
        .replace("{{ Title }}", extract_title(md_content))
        .replace("{{ Content }}", markdown_to_html_node(md_content).to_html())
        .replace("href=\"/", f"href=\"{basepath}")
        .replace("src=\"/", f"src=\"{basepath}")
    )
    dir_path = os.path.dirname(dest_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(dest_path, 'w', encoding="utf-8") as file:
        file.write(html_final)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
