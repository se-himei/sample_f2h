#!/usr/bin/env python3
"""
Figma Design Context to HTML/CSS Converter
Receives Figma design context and generates HTML and CSS files.
"""

import json
import sys
import re
import os
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """Sanitize a string to be used as a filename."""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'\s+', '_', name)
    return name.lower()


def parse_color(color_str: str) -> str:
    """Parse color from Figma format to CSS."""
    if not color_str:
        return "transparent"
    if color_str.startswith('#') or color_str.startswith('rgb'):
        return color_str
    return color_str


def extract_styles_from_node(node: dict, styles: dict) -> dict:
    """Extract CSS styles from a Figma node."""
    css = {}

    # Position and size
    if 'x' in node:
        css['left'] = f"{node['x']}px"
    if 'y' in node:
        css['top'] = f"{node['y']}px"
    if 'width' in node:
        css['width'] = f"{node['width']}px"
    if 'height' in node:
        css['height'] = f"{node['height']}px"

    # Background color
    if 'backgroundColor' in node:
        css['background-color'] = parse_color(node['backgroundColor'])
    if 'fills' in node and node['fills']:
        for fill in node['fills']:
            if fill.get('type') == 'SOLID' and fill.get('visible', True):
                color = fill.get('color', {})
                if isinstance(color, dict):
                    r = int(color.get('r', 0) * 255)
                    g = int(color.get('g', 0) * 255)
                    b = int(color.get('b', 0) * 255)
                    a = color.get('a', 1)
                    css['background-color'] = f"rgba({r}, {g}, {b}, {a})"

    # Border radius
    if 'cornerRadius' in node:
        css['border-radius'] = f"{node['cornerRadius']}px"

    # Opacity
    if 'opacity' in node and node['opacity'] < 1:
        css['opacity'] = str(node['opacity'])

    # Text styles
    if node.get('type') == 'TEXT':
        style = node.get('style', {})
        if 'fontSize' in style:
            css['font-size'] = f"{style['fontSize']}px"
        if 'fontWeight' in style:
            css['font-weight'] = str(style['fontWeight'])
        if 'fontFamily' in style:
            css['font-family'] = f"'{style['fontFamily']}', sans-serif"
        if 'lineHeightPx' in style:
            css['line-height'] = f"{style['lineHeightPx']}px"
        if 'textAlignHorizontal' in style:
            css['text-align'] = style['textAlignHorizontal'].lower()

    # Strokes (borders)
    if 'strokes' in node and node['strokes']:
        for stroke in node['strokes']:
            if stroke.get('type') == 'SOLID' and stroke.get('visible', True):
                color = stroke.get('color', {})
                if isinstance(color, dict):
                    r = int(color.get('r', 0) * 255)
                    g = int(color.get('g', 0) * 255)
                    b = int(color.get('b', 0) * 255)
                    weight = node.get('strokeWeight', 1)
                    css['border'] = f"{weight}px solid rgb({r}, {g}, {b})"

    # Effects (shadows)
    if 'effects' in node:
        shadows = []
        for effect in node['effects']:
            if effect.get('type') == 'DROP_SHADOW' and effect.get('visible', True):
                color = effect.get('color', {})
                r = int(color.get('r', 0) * 255)
                g = int(color.get('g', 0) * 255)
                b = int(color.get('b', 0) * 255)
                a = color.get('a', 0.25)
                offset = effect.get('offset', {'x': 0, 'y': 4})
                radius = effect.get('radius', 4)
                shadows.append(f"{offset['x']}px {offset['y']}px {radius}px rgba({r}, {g}, {b}, {a})")
        if shadows:
            css['box-shadow'] = ', '.join(shadows)

    return css


def generate_class_name(node: dict, index: int) -> str:
    """Generate a CSS class name for a node."""
    name = node.get('name', f'element-{index}')
    name = sanitize_filename(name)
    return f"{name}_{index}"


def process_node(node: dict, styles: dict, elements: list, depth: int = 0, index_counter: list = None):
    """Recursively process Figma nodes."""
    if index_counter is None:
        index_counter = [0]

    node_type = node.get('type', 'UNKNOWN')

    # Skip invisible nodes
    if not node.get('visible', True):
        return None

    class_name = generate_class_name(node, index_counter[0])
    index_counter[0] += 1

    css_props = extract_styles_from_node(node, styles)

    element = {
        'tag': 'div',
        'class': class_name,
        'content': '',
        'children': [],
        'css': css_props
    }

    # Determine HTML tag based on node type
    if node_type == 'TEXT':
        element['tag'] = 'p'
        element['content'] = node.get('characters', '')
    elif node_type == 'VECTOR' or node_type == 'STAR' or node_type == 'POLYGON':
        element['tag'] = 'div'
    elif node_type == 'FRAME' or node_type == 'GROUP' or node_type == 'COMPONENT':
        element['tag'] = 'div'
        element['css']['position'] = 'relative'
    elif node_type == 'RECTANGLE':
        element['tag'] = 'div'
    elif node_type == 'ELLIPSE':
        element['tag'] = 'div'
        element['css']['border-radius'] = '50%'
    elif node_type == 'IMAGE':
        element['tag'] = 'img'

    # Process children
    children = node.get('children', [])
    for child in children:
        child_element = process_node(child, styles, elements, depth + 1, index_counter)
        if child_element:
            element['children'].append(child_element)

    return element


def generate_html(element: dict, indent: int = 0) -> str:
    """Generate HTML from element structure."""
    spaces = '  ' * indent
    tag = element['tag']
    class_name = element['class']
    content = element.get('content', '')
    children = element.get('children', [])

    if tag == 'img':
        return f'{spaces}<img class="{class_name}" src="" alt="{class_name}">\n'

    html = f'{spaces}<{tag} class="{class_name}">'

    if children:
        html += '\n'
        for child in children:
            html += generate_html(child, indent + 1)
        html += f'{spaces}</{tag}>\n'
    elif content:
        html += f'{content}</{tag}>\n'
    else:
        html += f'</{tag}>\n'

    return html


def collect_css(element: dict, css_rules: list):
    """Collect CSS rules from element structure."""
    class_name = element['class']
    css_props = element.get('css', {})

    if css_props:
        css_rules.append({
            'selector': f'.{class_name}',
            'properties': css_props
        })

    for child in element.get('children', []):
        collect_css(child, css_rules)


def generate_css(css_rules: list, page_name: str) -> str:
    """Generate CSS from collected rules."""
    css = f"/* CSS for {page_name} */\n\n"
    css += "/* Reset and base styles */\n"
    css += "* {\n  margin: 0;\n  padding: 0;\n  box-sizing: border-box;\n}\n\n"

    for rule in css_rules:
        css += f"{rule['selector']} {{\n"
        for prop, value in rule['properties'].items():
            css += f"  {prop}: {value};\n"
        css += "}\n\n"

    return css


def convert_figma_to_html_css(design_context: dict, page_name: str, output_dir: str = 'output'):
    """Main conversion function."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    safe_page_name = sanitize_filename(page_name)

    # Get the root node
    root = design_context if isinstance(design_context, dict) else {}

    # If design_context has a 'document' key, use that
    if 'document' in root:
        root = root['document']

    # Process the design
    styles = {}
    elements = []

    root_element = process_node(root, styles, elements)

    if root_element is None:
        root_element = {
            'tag': 'div',
            'class': 'container',
            'content': '',
            'children': [],
            'css': {'width': '100%', 'min-height': '100vh'}
        }

    # Generate HTML
    html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_name}</title>
    <link rel="stylesheet" href="{safe_page_name}.css">
</head>
<body>
{generate_html(root_element, 1)}</body>
</html>
'''

    # Collect and generate CSS
    css_rules = []
    collect_css(root_element, css_rules)
    css_content = generate_css(css_rules, page_name)

    # Write files
    html_file = output_path / f'{safe_page_name}.html'
    css_file = output_path / f'{safe_page_name}.css'

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)

    print(f"Generated: {html_file}")
    print(f"Generated: {css_file}")

    return str(html_file), str(css_file)


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python figma_to_html.py <page_name> <output_dir>")
        print("Reads design context JSON from stdin")
        sys.exit(1)

    page_name = sys.argv[1]
    output_dir = sys.argv[2]

    # Read JSON from stdin
    try:
        design_context = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        html_file, css_file = convert_figma_to_html_css(design_context, page_name, output_dir)
        print(f"Successfully generated HTML and CSS for '{page_name}'")
    except Exception as e:
        print(f"Error converting design: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
