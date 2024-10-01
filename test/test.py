#!/usr/bin/env python3

import sys
import pyperclip
import re
from notion_client import Client
from datetime import datetime

# 替换为您的实际 Notion API 密钥和数据库 ID
NOTION_API_KEY = "secret_8j9tcjr9gGF5pXCW9iDRaH0Q2QE7NLCNx4d6LfZaaBa"
DATABASE_ID = "10dcef0d-da3e-806c-97bb-ca362447a5fb"

notion = Client(auth=NOTION_API_KEY)

def create_page(title, content, topic, tags):
    properties = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Topic": {"rich_text": [{"text": {"content": topic}}]},
        "Tags": {"multi_select": [{"name": tag.strip()} for tag in tags.split(",") if tag.strip()]},
        "Date": {"date": {"start": datetime.now().isoformat()}}
    }
    
    children = convert_markdown_to_blocks(content)
    
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties=properties,
        children=children
    )

def convert_markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('```'):
            code_block, i = process_code_block(lines, i)
            blocks.append(code_block)
        elif line.startswith('- '):
            list_block, i = process_list(lines, i)
            blocks.append(list_block)
        elif line.startswith('#'):
            heading_level = len(line.split()[0])
            blocks.append({f"heading_{heading_level}": {"rich_text": [{"type": "text", "text": {"content": line.lstrip('# '), "link": None}}]}})
        elif line.startswith('\\[') and line.endswith('\\]'):
            blocks.append({"equation": {"expression": line[2:-2]}})
        elif line:
            paragraph = {"paragraph": {"rich_text": process_inline_elements(line)}}
            blocks.append(paragraph)
        i += 1
    return blocks

def process_code_block(lines, start):
    language = lines[start].strip('`').lower() or "plain text"
    code_content = []
    i = start + 1
    while i < len(lines) and not lines[i].strip().startswith('```'):
        code_content.append(lines[i])
        i += 1
    return {"code": {"language": language, "rich_text": [{"text": {"content": '\n'.join(code_content)}}]}}, i + 1

def process_list(lines, start):
    def build_list_item(content, children=None):
        item = {"bulleted_list_item": {"rich_text": process_inline_elements(content)}}
        if children:
            item["bulleted_list_item"]["children"] = children
        return item

    def process_nested_list(current_indent, current_index):
        items = []
        i = current_index
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not stripped.startswith('- '):
                break
            indent = len(line) - len(line.lstrip())
            if indent < current_indent:
                break
            if indent > current_indent:
                children, i = process_nested_list(indent, i)
                items[-1]["bulleted_list_item"]["children"] = children
            else:
                items.append(build_list_item(stripped[2:]))
                i += 1
        return items, i

    initial_indent = len(lines[start]) - len(lines[start].lstrip())
    list_items, end_index = process_nested_list(initial_indent, start)
    
    if len(list_items) == 1:
        return list_items[0], end_index
    else:
        return {"bulleted_list_item": {"rich_text": [{"text": {"content": ""}}], "children": list_items}}, end_index

def process_inline_elements(text):
    elements = []
    pattern = r'(\*\*.*?\*\*)|(`.*?`)|(_.*?_)|(~~.*?~~)|(\\\(.*?\\\))'
    last_end = 0
    for match in re.finditer(pattern, text):
        if match.start() > last_end:
            elements.append({"type": "text", "text": {"content": text[last_end:match.start()]}})
        content = match.group()
        if content.startswith('**'):
            elements.append({"type": "text", "text": {"content": content[2:-2], "link": None}, "annotations": {"bold": True, "italic": False, "strikethrough": False, "underline": False, "code": False, "color": "default"}})
        elif content.startswith('`'):
            elements.append({"type": "text", "text": {"content": content[1:-1], "link": None}, "annotations": {"bold": False, "italic": False, "strikethrough": False, "underline": False, "code": True, "color": "default"}})
        elif content.startswith('_'):
            elements.append({"type": "text", "text": {"content": content[1:-1], "link": None}, "annotations": {"bold": False, "italic": True, "strikethrough": False, "underline": False, "code": False, "color": "default"}})
        elif content.startswith('~~'):
            elements.append({"type": "text", "text": {"content": content[2:-2], "link": None}, "annotations": {"bold": False, "italic": False, "strikethrough": True, "underline": False, "code": False, "color": "default"}})
        elif content.startswith('\\('):
            elements.append({"type": "equation", "equation": {"expression": content[2:-2]}})
        last_end = match.end()
    if last_end < len(text):
        elements.append({"type": "text", "text": {"content": text[last_end:], "link": None}, "annotations": {"bold": False, "italic": False, "strikethrough": False, "underline": False, "code": False, "color": "default"}})
    return elements

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: ./sendClipboard2Notion.py \"页面标题\"")
        sys.exit(1)

    title = sys.argv[1]
    content = pyperclip.paste()

    topic = input("输入主题 (或直接按回车跳过): ").strip()
    tags = input("输入标签 (用逗号分隔，或直接按回车跳过): ").strip()

    create_page(title, content, topic, tags)
    print(f"页面 '{title}' 已成功创建在 Notion 数据库中。")