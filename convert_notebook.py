#!/usr/bin/env python3
"""
Jupyter Notebook to Jekyll Markdown Converter

This script converts Jupyter notebooks (.ipynb) to Jekyll-compatible Markdown files,
including embedded images (matplotlib, seaborn plots) as base64-encoded data URIs.
"""

import json
import base64
import argparse
import os
from datetime import datetime
from pathlib import Path


def convert_notebook_to_markdown(notebook_path, output_path=None, title=None,
                                 categories="coding", tags=None):
    """
    Convert a Jupyter notebook to Jekyll Markdown format.
    All images are embedded as base64-encoded data URIs for a single-file solution.

    Args:
        notebook_path (str): Path to the .ipynb file
        output_path (str): Output path for the .md file (optional)
        title (str): Post title (optional, defaults to filename)
        categories (str): Post categories (default: "coding")
        tags (list): Post tags (default: ["python", "jupyter"])

    Returns:
        str: Path to the generated Markdown file
    """
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Get notebook name for default title
    notebook_name = Path(notebook_path).stem
    if title is None:
        title = notebook_name.replace('-', ' ').replace('_', ' ').title()

    if tags is None:
        tags = ["python", "jupyter"]

    # Prepare output path
    if output_path is None:
        # Use current working directory with date prefix
        today = datetime.now().strftime('%Y-%m-%d')
        output_filename = f"{today}-{notebook_name}.md"
        output_path = Path.cwd() / output_filename
    else:
        output_path = Path(output_path)

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Start building the markdown content
    markdown_lines = []

    # Add Jekyll front matter
    markdown_lines.append("---")
    markdown_lines.append("layout: single")
    markdown_lines.append(f'title: "{title}"')
    markdown_lines.append(f"categories: {categories}")
    markdown_lines.append(f"tag: {tags}")
    markdown_lines.append("toc: true")
    markdown_lines.append("author_profile: false")
    markdown_lines.append("---")
    markdown_lines.append("")

    # Process each cell
    for cell_idx, cell in enumerate(notebook.get('cells', [])):
        cell_type = cell.get('cell_type', '')

        if cell_type == 'markdown':
            # Add markdown cells directly
            source = cell.get('source', [])
            if isinstance(source, list):
                markdown_lines.extend(source)
            else:
                markdown_lines.append(source)
            markdown_lines.append("")

        elif cell_type == 'code':
            # Add code cell
            source = cell.get('source', [])
            if isinstance(source, list):
                code = ''.join(source)
            else:
                code = source

            # Skip empty cells
            if code.strip():
                markdown_lines.append("```python")
                markdown_lines.append(code.rstrip())
                markdown_lines.append("```")
                markdown_lines.append("")

            # Process outputs
            outputs = cell.get('outputs', [])
            for output in outputs:
                output_type = output.get('output_type', '')

                # Handle stream output (print statements)
                if output_type == 'stream':
                    text = output.get('text', [])
                    if isinstance(text, list):
                        text = ''.join(text)
                    if text.strip():
                        markdown_lines.append("```")
                        markdown_lines.append(text.rstrip())
                        markdown_lines.append("```")
                        markdown_lines.append("")

                # Handle execution results (display output)
                elif output_type in ['execute_result', 'display_data']:
                    data = output.get('data', {})

                    # Handle images (PNG, JPEG, SVG)
                    if 'image/png' in data:
                        image_data = data['image/png']
                        # Embed as base64 data URI
                        markdown_lines.append(f"![output](data:image/png;base64,{image_data})")
                        markdown_lines.append("")

                    elif 'image/jpeg' in data:
                        image_data = data['image/jpeg']
                        # Embed as base64 data URI
                        markdown_lines.append(f"![output](data:image/jpeg;base64,{image_data})")
                        markdown_lines.append("")

                    elif 'image/svg+xml' in data:
                        svg_data = data['image/svg+xml']
                        if isinstance(svg_data, list):
                            svg_data = ''.join(svg_data)
                        markdown_lines.append(svg_data)
                        markdown_lines.append("")

                    # Handle HTML output (e.g., pandas DataFrames)
                    elif 'text/html' in data:
                        html = data['text/html']
                        if isinstance(html, list):
                            html = ''.join(html)
                        markdown_lines.append(html)
                        markdown_lines.append("")

                    # Handle plain text output
                    elif 'text/plain' in data:
                        text = data['text/plain']
                        if isinstance(text, list):
                            text = ''.join(text)
                        if text.strip():
                            markdown_lines.append("```")
                            markdown_lines.append(text.rstrip())
                            markdown_lines.append("```")
                            markdown_lines.append("")

                # Handle errors
                elif output_type == 'error':
                    traceback = output.get('traceback', [])
                    if traceback:
                        markdown_lines.append("```python")
                        markdown_lines.append('\n'.join(traceback))
                        markdown_lines.append("```")
                        markdown_lines.append("")

    # Write the markdown file
    markdown_content = '\n'.join(markdown_lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"✓ Converted notebook to: {output_path}")
    print(f"✓ All images embedded as base64 - ready to upload!")

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Jupyter notebooks to Jekyll Markdown format (images embedded as base64)'
    )
    parser.add_argument('notebook', help='Path to the .ipynb file')
    parser.add_argument('-o', '--output', help='Output path for the .md file')
    parser.add_argument('-t', '--title', help='Post title')
    parser.add_argument('-c', '--categories', default='coding', help='Post categories')
    parser.add_argument('--tags', nargs='+', default=['python', 'jupyter'],
                       help='Post tags')

    args = parser.parse_args()

    convert_notebook_to_markdown(
        notebook_path=args.notebook,
        output_path=args.output,
        title=args.title,
        categories=args.categories,
        tags=args.tags
    )


if __name__ == '__main__':
    main()
