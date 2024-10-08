#!/usr/bin/env python

from notion_client import Client
import pyperclip
import sys
from datetime import datetime
import re

notion_token = 'secret_8j9tcjr9gGF5pXCW9iDRaH0Q2QE7NLCNx4d6LfZaaBa'
notion_database_id = '10dcef0dda3e806c97bbca362447a5fb'

def parse_markdown(content):
    lines = content.split('\n')
    blocks = []
    stack = [(0, blocks)]
    code_block = False
    code_language = ''
    code_content = []

    def get_notion_language(lang):
        lang_map = {
            'plaintext': 'plain text',
            'text': 'plain text',
        }
        return lang_map.get(lang.lower(), lang.lower())

    def create_rich_text(text):
        rich_text = []
        parts = re.split(r'(\\\(.*?\\\))', text)
        for part in parts:
            if part.startswith('\\(') and part.endswith('\\)'):
                rich_text.append({
                    "type": "equation",
                    "equation": {
                        "expression": part[2:-2]
                    }
                })
            else:
                sub_parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`[^`\n]+`|~~.*?~~|\[.*?\]\(.*?\))', part)
                for sub_part in sub_parts:
                    if sub_part.startswith('**') and sub_part.endswith('**'):
                        rich_text.append({"type": "text", "text": {"content": sub_part[2:-2]}, "annotations": {"bold": True}})
                    elif sub_part.startswith('*') and sub_part.endswith('*'):
                        rich_text.append({"type": "text", "text": {"content": sub_part[1:-1]}, "annotations": {"italic": True}})
                    elif sub_part.startswith('`') and sub_part.endswith('`') and '\n' not in sub_part:
                        rich_text.append({"type": "text", "text": {"content": sub_part[1:-1]}, "annotations": {"code": True}})
                    elif sub_part.startswith('~~') and sub_part.endswith('~~'):
                        rich_text.append({"type": "text", "text": {"content": sub_part[2:-2]}, "annotations": {"strikethrough": True}})
                    elif sub_part.startswith('[') and '](' in sub_part and sub_part.endswith(')'):
                        link_text, link_url = re.match(r'\[(.*?)\]\((.*?)\)', sub_part).groups()
                        rich_text.append({"type": "text", "text": {"content": link_text, "link": {"url": link_url}}})
                    else:
                        rich_text.append({"type": "text", "text": {"content": sub_part}})
        return rich_text

    def get_indent_level(line):
        return len(line) - len(line.lstrip())

    def add_block(block, indent):
        while stack and indent <= stack[-1][0]:
            stack.pop()
        
        if not stack:
            blocks.append(block)
            if block['type'] in ['bulleted_list_item', 'numbered_list_item', 'to_do']:
                stack.append((indent, [block]))
        else:
            parent = stack[-1][1]
            parent.append(block)
            if block['type'] in ['bulleted_list_item', 'numbered_list_item', 'to_do']:
                if 'children' not in block:
                    block['children'] = []
                stack.append((indent, block['children']))

    for line in lines:
        stripped_line = line.strip()
        indent = get_indent_level(line)

        if code_block:
            if stripped_line.startswith('```'):
                add_block({
                    "type": "code",
                    "code": {
                        "language": get_notion_language(code_language),
                        "rich_text": [{"type": "text", "text": {"content": '\n'.join(code_content)}}]
                    }
                }, indent)
                code_block = False
            else:
                code_content.append(line)
            continue

        if stripped_line.startswith('```'):
            code_block = True
            code_language = stripped_line[3:].strip() or 'plain text'
            code_content = []
            continue

        list_match = re.match(r'^(\s*)([*-]|\d+\.)\s', line)
        if list_match:
            list_type = "bulleted_list_item" if list_match.group(2) in ['*', '-'] else "numbered_list_item"
            content = line[list_match.end():].strip()
            add_block({
                "type": list_type,
                list_type: {
                    "rich_text": create_rich_text(content)
                }
            }, indent)
        elif line.startswith('#'):
            heading_level = len(line.split()[0])
            heading_text = line.lstrip('#').strip()
            add_block({
                "type": f"heading_{heading_level}",
                f"heading_{heading_level}": {
                    "rich_text": create_rich_text(heading_text)
                }
            }, indent)
        elif line.startswith('> '):
            add_block({
                "type": "quote",
                "quote": {
                    "rich_text": create_rich_text(line[2:])
                }
            }, indent)
        elif line.startswith('- [ ] ') or line.startswith('- [x] '):
            checked = line.startswith('- [x] ')
            add_block({
                "type": "to_do",
                "to_do": {
                    "rich_text": create_rich_text(line[6:]),
                    "checked": checked
                }
            }, indent)
        elif line.startswith('---'):
            add_block({"type": "divider", "divider": {}}, indent)
        elif stripped_line == '':
            add_block({"type": "paragraph", "paragraph": {"rich_text": []}}, indent)
        else:
            add_block({
                "type": "paragraph",
                "paragraph": {
                    "rich_text": create_rich_text(line)
                }
            }, indent)

    return blocks

def handle_special_elements(content):
    # 处理表格
    content = re.sub(r'\n\|.*?\|.*?\n', lambda m: f"\n[表格]\n{m.group()}\n", content)
    
    # 处理图片
    content = re.sub(r'!\[(.*?)\]\((.*?)\)', r'[图片: \1](\2)', content)
    
    # 处理公式块
    content = re.sub(r'\$\$(.*?)\$\$', r'[公式块]\n\1\n', content, flags=re.DOTALL)
    
    # 处理行内公式
    content = re.sub(r'\$(.*?)\$', r'[行内公式: \1]', content)
    
    return content

def create_notion_page(client, database_id, title, content):
    try:
        blocks = parse_markdown(content)
        new_page = client.pages.create(
            parent={"database_id": database_id},
            properties={"Title": {"title": [{"text": {"content": title}}]}},
            children=blocks
        )
        print(f"成功创建新页面: {new_page['url']}")
    except Exception as e:
        print(f"创建页面时出错: {str(e)}")
        print("错误的块结构:")
        for i, block in enumerate(blocks):
            print(f"Block {i}: {block}")
        print("尝试以纯文本形式创建页面...")
        try:
            new_page = client.pages.create(
                parent={"database_id": database_id},
                properties={"Title": {"title": [{"text": {"content": title}}]}},
                children=[{"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}}]
            )
            print(f"成功以纯文本形式创建新页面: {new_page['url']}")
        except Exception as e:
            print(f"以纯文本形式创建页面时也出错: {str(e)}")

def main():
    client = Client(auth=notion_token)

    # 获取命令行参数作为标题
    if len(sys.argv) < 2:
        print("请提供标题作为命令行参数")
        return
    title = sys.argv[1]

    # 获取用户输入
    topic = input("请输入Topic (按回车跳过): ").strip()
    tags = input("请输入Tags (用逗号分隔, 按回车跳过): ").strip()

    # 获取剪贴板内容
    content = pyperclip.paste()

    # 处理特殊元素
    content = handle_special_elements(content)

    # 准备新页面的属性
    new_page = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Topic": {"rich_text": [{"text": {"content": topic}}]} if topic else None,
        "Tags": {"multi_select": [{"name": tag.strip()} for tag in tags.split(',') if tag.strip()]} if tags else None,
        "Date": {"date": {"start": datetime.now().isoformat()}},
        "Checkbox": {"checkbox": False}
    }

    # 移除空值
    new_page = {k: v for k, v in new_page.items() if v is not None}

    # 创建新页面
    create_notion_page(client, notion_database_id, title, content)

if __name__ == '__main__':
    main()