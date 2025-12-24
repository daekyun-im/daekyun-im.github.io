#!/usr/bin/env python3
"""
Markdown Image Validator

Validates that base64-encoded images in markdown files are properly formatted.
"""

import re
import base64
import argparse
import json
import sys
import platform
from pathlib import Path
from datetime import datetime


def validate_markdown_images(md_path):
    """
    Validate base64 images in a markdown file.

    Args:
        md_path (str): Path to the markdown file

    Returns:
        dict: Validation results
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match base64 image data URIs
    pattern = r'!\[.*?\]\(data:image/(png|jpeg|jpg);base64,([A-Za-z0-9+/=]+)\)'

    matches = list(re.finditer(pattern, content))

    results = {
        'total_images': len(matches),
        'valid_images': 0,
        'invalid_images': 0,
        'errors': [],
        'image_sizes': []
    }

    print(f"\n{'='*60}")
    print(f"Validating: {md_path}")
    print(f"{'='*60}\n")

    for i, match in enumerate(matches, 1):
        image_type = match.group(1)
        base64_data = match.group(2)

        print(f"Image {i}/{len(matches)} ({image_type}):")

        # Check for newlines (should not exist)
        if '\n' in base64_data or '\r' in base64_data:
            error = f"  ❌ Contains newline characters"
            print(error)
            results['errors'].append(f"Image {i}: {error}")
            results['invalid_images'] += 1
            continue

        # Check if base64 is valid
        try:
            decoded = base64.b64decode(base64_data)
            size_kb = len(decoded) / 1024
            results['image_sizes'].append(size_kb)

            print(f"  ✓ Valid base64 data")
            print(f"  ✓ Size: {size_kb:.2f} KB")

            # Verify image header
            if image_type in ['png']:
                if decoded[:8] == b'\x89PNG\r\n\x1a\n':
                    print(f"  ✓ Valid PNG header")
                    results['valid_images'] += 1
                else:
                    error = "Invalid PNG header"
                    print(f"  ⚠️  {error}")
                    results['errors'].append(f"Image {i}: {error}")
                    results['invalid_images'] += 1

            elif image_type in ['jpeg', 'jpg']:
                if decoded[:2] == b'\xff\xd8':
                    print(f"  ✓ Valid JPEG header")
                    results['valid_images'] += 1
                else:
                    error = "Invalid JPEG header"
                    print(f"  ⚠️  {error}")
                    results['errors'].append(f"Image {i}: {error}")
                    results['invalid_images'] += 1

        except Exception as e:
            error = f"Failed to decode base64: {str(e)}"
            print(f"  ❌ {error}")
            results['errors'].append(f"Image {i}: {error}")
            results['invalid_images'] += 1

        print()

    # Print summary
    print(f"{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total images found: {results['total_images']}")
    print(f"Valid images: {results['valid_images']}")
    print(f"Invalid images: {results['invalid_images']}")

    if results['image_sizes']:
        total_size = sum(results['image_sizes'])
        avg_size = total_size / len(results['image_sizes'])
        print(f"\nTotal image size: {total_size:.2f} KB ({total_size/1024:.2f} MB)")
        print(f"Average image size: {avg_size:.2f} KB")

    if results['errors']:
        print(f"\n⚠️  ERRORS FOUND:")
        for error in results['errors']:
            print(f"  - {error}")
    else:
        print(f"\n✓ All images are valid!")

    print(f"{'='*60}\n")

    return results


def create_preview_html(md_path, output_path=None):
    """
    Create an HTML preview of the markdown file to test image rendering.

    Args:
        md_path (str): Path to the markdown file
        output_path (str): Output path for HTML file (optional)
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if output_path is None:
        md_file = Path(md_path)
        output_path = md_file.parent / f"{md_file.stem}_preview.html"

    # Simple markdown to HTML conversion for images
    # Replace markdown image syntax with HTML img tags
    html_content = re.sub(
        r'!\[([^\]]*)\]\((data:image/[^)]+)\)',
        r'<img src="\2" alt="\1" style="max-width: 100%; height: auto;">',
        content
    )

    # Replace code blocks
    html_content = re.sub(r'```python\n(.*?)\n```', r'<pre><code>\1</code></pre>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'```\n(.*?)\n```', r'<pre><code>\1</code></pre>', html_content, flags=re.DOTALL)

    # Wrap in HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Preview: {Path(md_path).name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            margin: 20px 0;
        }}
        pre {{
            background: #f6f8fa;
            padding: 16px;
            overflow: auto;
            border-radius: 6px;
        }}
        code {{
            font-family: 'Courier New', monospace;
        }}
    </style>
</head>
<body>
    <h1>Preview: {Path(md_path).name}</h1>
    <hr>
    {html_content}
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Preview HTML created: {output_path}")
    print(f"  Open this file in a browser to check if images render correctly.")

    return str(output_path)


def collect_debug_info(md_path, ipynb_path=None):
    """
    Collect comprehensive debugging information for troubleshooting.

    Args:
        md_path (str): Path to the markdown file
        ipynb_path (str): Optional path to the original .ipynb file

    Returns:
        dict: Debug information
    """
    debug_info = {
        'timestamp': datetime.now().isoformat(),
        'system': {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'python_version': sys.version,
        },
        'files': {},
        'images': []
    }

    # Analyze markdown file
    md_file = Path(md_path)
    if md_file.exists():
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        debug_info['files']['markdown'] = {
            'path': str(md_file.absolute()),
            'size_kb': md_file.stat().st_size / 1024,
            'exists': True
        }

        # Extract image information
        pattern = r'!\[.*?\]\(data:image/(png|jpeg|jpg);base64,([A-Za-z0-9+/=\n\r\s]+)\)'
        matches = list(re.finditer(pattern, md_content))

        for i, match in enumerate(matches, 1):
            img_type = match.group(1)
            b64_data = match.group(2)

            img_info = {
                'index': i,
                'type': img_type,
                'base64_length': len(b64_data),
                'has_newlines': '\n' in b64_data or '\r' in b64_data,
                'has_spaces': ' ' in b64_data,
                'first_50_chars': b64_data[:50],
                'last_50_chars': b64_data[-50:],
            }

            # Try to decode
            try:
                # Clean the data first
                clean_data = b64_data.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                decoded = base64.b64decode(clean_data)
                img_info['decodable'] = True
                img_info['decoded_size_kb'] = len(decoded) / 1024
                img_info['file_header'] = str(decoded[:10])

                # Check image headers
                if img_type == 'png':
                    img_info['valid_header'] = decoded[:8] == b'\x89PNG\r\n\x1a\n'
                elif img_type in ['jpeg', 'jpg']:
                    img_info['valid_header'] = decoded[:2] == b'\xff\xd8'
            except Exception as e:
                img_info['decodable'] = False
                img_info['decode_error'] = str(e)

            debug_info['images'].append(img_info)

    # Analyze original .ipynb file if provided
    if ipynb_path:
        ipynb_file = Path(ipynb_path)
        if ipynb_file.exists():
            with open(ipynb_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)

            debug_info['files']['notebook'] = {
                'path': str(ipynb_file.absolute()),
                'size_kb': ipynb_file.stat().st_size / 1024,
                'exists': True
            }

            # Find images in notebook
            nb_images = []
            for cell_idx, cell in enumerate(notebook.get('cells', [])):
                if cell.get('cell_type') == 'code':
                    for output in cell.get('outputs', []):
                        if 'data' in output:
                            data = output['data']
                            if 'image/png' in data:
                                img_data = data['image/png']
                                nb_images.append({
                                    'cell_index': cell_idx,
                                    'type': 'png',
                                    'is_list': isinstance(img_data, list),
                                    'length': len(img_data) if isinstance(img_data, str) else len(''.join(img_data)),
                                    'has_newlines': '\n' in (img_data if isinstance(img_data, str) else ''.join(img_data)),
                                    'first_50': (img_data[:50] if isinstance(img_data, str) else ''.join(img_data)[:50])
                                })

            debug_info['notebook_images'] = nb_images
        else:
            debug_info['files']['notebook'] = {
                'path': str(ipynb_file.absolute()),
                'exists': False
            }

    return debug_info


def save_debug_report(debug_info, output_path=None):
    """
    Save debug information to a file for issue reporting.

    Args:
        debug_info (dict): Debug information dictionary
        output_path (str): Output path for the debug report
    """
    if output_path is None:
        output_path = f"debug_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("DEBUG REPORT - Jupyter Notebook to Markdown Converter\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"Generated: {debug_info['timestamp']}\n\n")

        # System info
        f.write("SYSTEM INFORMATION\n")
        f.write("-" * 70 + "\n")
        for key, value in debug_info['system'].items():
            f.write(f"{key}: {value}\n")
        f.write("\n")

        # File info
        f.write("FILE INFORMATION\n")
        f.write("-" * 70 + "\n")
        for file_type, info in debug_info['files'].items():
            f.write(f"\n{file_type.upper()}:\n")
            for key, value in info.items():
                f.write(f"  {key}: {value}\n")
        f.write("\n")

        # Image info
        f.write("IMAGE ANALYSIS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total images found in markdown: {len(debug_info.get('images', []))}\n\n")

        for img in debug_info.get('images', []):
            f.write(f"Image {img['index']} ({img['type']}):\n")
            for key, value in img.items():
                if key != 'index':
                    f.write(f"  {key}: {value}\n")
            f.write("\n")

        # Notebook images if available
        if 'notebook_images' in debug_info:
            f.write("ORIGINAL NOTEBOOK IMAGES\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total images in notebook: {len(debug_info['notebook_images'])}\n\n")
            for i, img in enumerate(debug_info['notebook_images'], 1):
                f.write(f"Notebook Image {i}:\n")
                for key, value in img.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")

        # Issue template
        f.write("\n" + "=" * 70 + "\n")
        f.write("ISSUE REPORT TEMPLATE\n")
        f.write("=" * 70 + "\n\n")
        f.write("Copy the information below when reporting an issue:\n\n")
        f.write("## Problem Description\n")
        f.write("[Describe how images appear when broken - not showing, garbled, etc.]\n\n")
        f.write("## Environment\n")
        f.write(f"- OS: {debug_info['system']['platform']}\n")
        f.write(f"- Python: {debug_info['system']['python_version'].split()[0]}\n\n")
        f.write("## Files\n")
        f.write(f"- Markdown file size: {debug_info['files'].get('markdown', {}).get('size_kb', 'N/A'):.2f} KB\n")
        f.write(f"- Number of images: {len(debug_info.get('images', []))}\n\n")
        f.write("## Image Issues\n")

        problematic = [img for img in debug_info.get('images', [])
                      if not img.get('decodable', True) or img.get('has_newlines', False)]
        if problematic:
            f.write(f"Found {len(problematic)} potentially problematic images:\n")
            for img in problematic:
                f.write(f"- Image {img['index']}: ")
                if not img.get('decodable'):
                    f.write(f"Not decodable - {img.get('decode_error', 'Unknown error')}\n")
                elif img.get('has_newlines'):
                    f.write("Contains newlines in base64 data\n")
        else:
            f.write("No obvious issues detected in image encoding.\n")

        f.write("\n## Full Debug Data\n")
        f.write("See sections above for detailed analysis.\n\n")

    print(f"\n✓ Debug report saved to: {output_path}")
    print(f"  Share this file when reporting issues for faster troubleshooting!")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Validate base64 images in markdown files'
    )
    parser.add_argument('markdown', help='Path to the markdown file')
    parser.add_argument('--preview', action='store_true',
                       help='Create HTML preview file')
    parser.add_argument('--debug', action='store_true',
                       help='Generate debug report with detailed diagnostics')
    parser.add_argument('--notebook', help='Path to original .ipynb file (for debug mode)')

    args = parser.parse_args()

    # Validate images
    results = validate_markdown_images(args.markdown)

    # Create preview if requested
    if args.preview:
        print()
        create_preview_html(args.markdown)

    # Generate debug report if requested
    if args.debug:
        print()
        print("Collecting debug information...")
        debug_info = collect_debug_info(args.markdown, args.notebook)
        save_debug_report(debug_info)

    # Exit with error code if validation failed
    if results['invalid_images'] > 0:
        exit(1)


if __name__ == '__main__':
    main()
