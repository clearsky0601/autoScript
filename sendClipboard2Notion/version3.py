#!/usr/bin/env python3

import sys
import pyperclip
import re
from notion_client import Client, APIResponseError
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
    
    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=properties,
            children=children
        )
    except APIResponseError as e:
        print(f"Error creating page: {e}")
        print("Problematic block:", children[2] if len(children) > 2 else "Not enough blocks")
        raise

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
            list_items, i = process_list(lines, i)
            blocks.extend(list_items)
        elif line.startswith('#'):
            heading_level = len(line.split()[0])
            blocks.append({f"heading_{heading_level}": {"rich_text": [{"type": "text", "text": {"content": line.lstrip('# ')}}]}})
        elif line.startswith('\\[') and line.endswith('\\]'):
            blocks.append({"equation": {"expression": line[2:-2]}})
        elif line == '\\[':
            equation_content = []
            i += 1
            while i < len(lines) and not lines[i].strip() == '\\]':
                equation_content.append(lines[i])
                i += 1
            if i < len(lines):
                blocks.append({"equation": {"expression": '\n'.join(equation_content)}})
        elif line.startswith('1. '):
            numbered_list, i = process_numbered_list(lines, i)
            blocks.append(numbered_list)
        elif line:
            paragraph = {"paragraph": {"rich_text": process_inline_elements(line)}}
            blocks.append(paragraph)
        i += 1
    
    # 添加调试输出
    for idx, block in enumerate(blocks):
        print(f"Block {idx}: {block}")
    
    return blocks

def process_code_block(lines, start):
    language = lines[start].strip('`').lower() or "plain text"
    code_content = []
    i = start + 1
    while i < len(lines) and not lines[i].strip().startswith('```'):
        code_content.append(lines[i])
        i += 1
    return {"code": {"language": language.strip(), "rich_text": [{"text": {"content": '\n'.join(code_content)}}]}}, i + 1

def process_numbered_list(lines, start):
    items = []
    i = start
    while i < len(lines) and lines[i].strip().startswith(f"{len(items) + 1}. "):
        items.append({"rich_text": process_inline_elements(lines[i].strip()[3:])})
        i += 1
    return {"numbered_list": {"children": [{"numbered_list_item": item} for item in items]}}, i

def process_inline_elements(text):
    elements = []
    pattern = r'(\*\*.*?\*\*)|(`.*?`)|(_.*?_)|(~~.*?~~)|(\\\(.*?\\\))'
    last_end = 0
    for match in re.finditer(pattern, text):
        if match.start() > last_end:
            elements.append({"type": "text", "text": {"content": text[last_end:match.start()]}})
        content = match.group()
        if content.startswith('**'):
            elements.append({"type": "text", "text": {"content": content[2:-2]}, "annotations": {"bold": True}})
        elif content.startswith('`'):
            elements.append({"type": "text", "text": {"content": content[1:-1]}, "annotations": {"code": True}})
        elif content.startswith('_'):
            elements.append({"type": "text", "text": {"content": content[1:-1]}, "annotations": {"italic": True}})
        elif content.startswith('~~'):
            elements.append({"type": "text", "text": {"content": content[2:-2]}, "annotations": {"strikethrough": True}})
        elif content.startswith('\\('):
            elements.append({"type": "equation", "equation": {"expression": content[2:-2]}})
        last_end = match.end()
    if last_end < len(text):
        elements.append({"type": "text", "text": {"content": text[last_end:]}})
    return elements

def process_list(lines, start):
    items = []
    i = start
    while i < len(lines) and lines[i].strip().startswith('- '):
        items.append({"bulleted_list_item": {"rich_text": process_inline_elements(lines[i].strip()[2:])}})
        i += 1
    return items, i

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