#!/usr/bin/env python3
"""
Markdown Image Validator

Validates that base64-encoded images in markdown files are properly formatted.
"""

import re
import base64
import argparse
from pathlib import Path


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


def main():
    parser = argparse.ArgumentParser(
        description='Validate base64 images in markdown files'
    )
    parser.add_argument('markdown', help='Path to the markdown file')
    parser.add_argument('--preview', action='store_true',
                       help='Create HTML preview file')

    args = parser.parse_args()

    # Validate images
    results = validate_markdown_images(args.markdown)

    # Create preview if requested
    if args.preview:
        print()
        create_preview_html(args.markdown)

    # Exit with error code if validation failed
    if results['invalid_images'] > 0:
        exit(1)


if __name__ == '__main__':
    main()
