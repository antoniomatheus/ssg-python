import os
import shutil
from src.process import generate_page

STATIC_DIR = "static"
PUBLIC_DIR = "public"


def main():
    public_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", PUBLIC_DIR)
    )
    static_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", STATIC_DIR)
    )

    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    shutil.copytree(static_path, public_path)

    markdown_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "content/index.md")
    )
    template_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "assets/template.html")
    )
    output_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "public/index.html")
    )

    generate_page(markdown_path, template_path, output_path)


main()
