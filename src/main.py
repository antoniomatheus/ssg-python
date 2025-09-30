import os
import shutil
import sys
from src.process import generate_pages_recursively

STATIC_DIR = "static"
OUTPUT_DIR = "docs"


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    public_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", OUTPUT_DIR)
    )
    static_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", STATIC_DIR)
    )

    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    shutil.copytree(static_path, public_path)

    content_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "content")
    )
    template_filepath = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "assets/template.html")
    )
    output_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", OUTPUT_DIR)
    )

    generate_pages_recursively(content_dir, template_filepath, output_dir, basepath)


main()
