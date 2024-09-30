#!/usr/bin/env python

from notion_client import Client
import pyperclip
import sys
from datetime import datetime
import re

notion_token = 'secret_8j9tcjr9gGF5pXCW9iDRaH0Q2QE7NLCNx4d6LfZaaBa'
notion_database_id = '10dcef0dda3e806c97bbca362447a5fb'

# def parse_markdown(content):
#     blocks = []
#     lines = content.split('\n')
#     code_block = False
#     code_language = ''
#     code_content = []
#     list_type = None
#     list_items = []
#     equation_block = False
#     equation_content = []

#     def get_notion_language(lang):
#         lang_map = {
#             'plaintext': 'plain text',
#             'text': 'plain text',
#             # 添加更多的映射关系
#         }
#         return lang_map.get(lang.lower(), lang.lower())

#     def create_rich_text(text):
#         rich_text = []
#         parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`[^`\n]+`|~~.*?~~|\[.*?\]\(.*?\))', text)
#         for part in parts:
#             if part.startswith('**') and part.endswith('**'):
#                 rich_text.append({"type": "text", "text": {"content": part[2:-2]}, "annotations": {"bold": True}})
#             elif part.startswith('*') and part.endswith('*'):
#                 rich_text.append({"type": "text", "text": {"content": part[1:-1]}, "annotations": {"italic": True}})
#             elif part.startswith('`') and part.endswith('`') and '\n' not in part:
#                 rich_text.append({"type": "text", "text": {"content": part[1:-1]}, "annotations": {"code": True}})
#             elif part.startswith('~~') and part.endswith('~~'):
#                 rich_text.append({"type": "text", "text": {"content": part[2:-2]}, "annotations": {"strikethrough": True}})
#             elif part.startswith('[') and '](' in part and part.endswith(')'):
#                 link_text, link_url = re.match(r'\[(.*?)\]\((.*?)\)', part).groups()
#                 rich_text.append({"type": "text", "text": {"content": link_text, "link": {"url": link_url}}})
#             else:
#                 rich_text.append({"type": "text", "text": {"content": part}})
#         return rich_text

#     def flush_list():
#         nonlocal list_type, list_items
#         if list_items:
#             for item in list_items:
#                 blocks.append({
#                     "type": list_type,
#                     list_type: {
#                         "rich_text": create_rich_text(item)
#                     }
#                 })
#             list_type = None
#             list_items = []

#     for line in lines:
#         stripped_line = line.strip()
        
#         # 处理行间公式（公式块）
#         if stripped_line.startswith('\\[') and not equation_block:
#             equation_block = True
#             continue
#         elif stripped_line.endswith('\\]') and equation_block:
#             equation_content.append(stripped_line[:-2])
#             blocks.append({
#                 "type": "equation",
#                 "equation": {
#                     "expression": '\n'.join(equation_content)
#                 }
#             })
#             equation_block = False
#             equation_content = []
#             continue
#         elif equation_block:
#             equation_content.append(stripped_line)
#             continue
        
#         # 处理代码块
#         elif stripped_line.startswith('```') and not code_block:
#             code_block = True
#             code_language = stripped_line[3:].strip() or 'plain text'
#             continue
#         elif stripped_line.startswith('```') and code_block:
#             blocks.append({
#                 "type": "code",
#                 "code": {
#                     "language": get_notion_language(code_language),
#                     "rich_text": [{"type": "text", "text": {"content": '\n'.join(code_content)}}]
#                 }
#             })
#             code_block = False
#             code_language = ''
#             code_content = []
#             continue
#         elif code_block:
#             code_content.append(line)  # 保留原始行，包括前导空格
#             continue
#         elif line.startswith('#'):
#             flush_list()
#             heading_level = len(line.split()[0])
#             heading_text = line.lstrip('#').strip()
#             blocks.append({
#                 "type": f"heading_{heading_level}",
#                 f"heading_{heading_level}": {
#                     "rich_text": create_rich_text(heading_text)
#                 }
#             })
#         elif line.startswith('> '):
#             flush_list()
#             blocks.append({
#                 "type": "quote",
#                 "quote": {
#                     "rich_text": create_rich_text(line[2:])
#                 }
#             })
#         elif line.startswith('- ') or line.startswith('* '):
#             if list_type != "bulleted_list_item":
#                 flush_list()
#                 list_type = "bulleted_list_item"
#             list_items.append(line[2:])
#         elif re.match(r'^\d+\. ', line):
#             if list_type != "numbered_list_item":
#                 flush_list()
#                 list_type = "numbered_list_item"
#             list_items.append(re.sub(r'^\d+\. ', '', line))
#         elif line.startswith('- [ ] ') or line.startswith('- [x] '):
#             flush_list()
#             checked = line.startswith('- [x] ')
#             blocks.append({
#                 "type": "to_do",
#                 "to_do": {
#                     "rich_text": create_rich_text(line[6:]),
#                     "checked": checked
#                 }
#             })
#         elif line.startswith('---'):
#             flush_list()
#             blocks.append({"type": "divider", "divider": {}})
#         elif line.strip() == '':
#             flush_list()
#         else:
#             flush_list()
#             # 处理行内公式
#             parts = re.split(r'(\\\(.*?\\\))', line)
#             rich_text = []
#             for part in parts:
#                 if part.startswith('\\(') and part.endswith('\\)'):
#                     rich_text.append({
#                         "type": "equation",
#                         "equation": {
#                             "expression": part[2:-2]
#                         }
#                     })
#                 else:
#                     rich_text.extend(create_rich_text(part))
            
#             blocks.append({
#                 "type": "paragraph",
#                 "paragraph": {
#                     "rich_text": rich_text
#                 }
#             })

#     flush_list()
#     return blocks


# def parse_markdown(content):
#     blocks = []
#     lines = content.split('\n')
#     code_block = False
#     code_language = ''
#     code_content = []
#     list_type = None
#     list_items = []
#     equation_block = False
#     equation_content = []

#     def get_notion_language(lang):
#         lang_map = {
#             'plaintext': 'plain text',
#             'text': 'plain text',
#             # 添加更多的映射关系
#         }
#         return lang_map.get(lang.lower(), lang.lower())

#     def create_rich_text(text):
#         rich_text = []
#         parts = re.split(r'(\\\(.*?\\\)|\\\[.*?\\\])', text)
#         for part in parts:
#             if part.startswith('\\(') and part.endswith('\\)'):
#                 rich_text.append({
#                     "type": "equation",
#                     "equation": {
#                         "expression": part[2:-2]
#                     }
#                 })
#             elif part.startswith('\\[') and part.endswith('\\]'):
#                 rich_text.append({
#                     "type": "equation",
#                     "equation": {
#                         "expression": part[2:-2]
#                     }
#                 })
#             else:
#                 sub_parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`[^`\n]+`|~~.*?~~|\[.*?\]\(.*?\))', part)
#                 for sub_part in sub_parts:
#                     if sub_part.startswith('**') and sub_part.endswith('**'):
#                         rich_text.append({"type": "text", "text": {"content": sub_part[2:-2]}, "annotations": {"bold": True}})
#                     elif sub_part.startswith('*') and sub_part.endswith('*'):
#                         rich_text.append({"type": "text", "text": {"content": sub_part[1:-1]}, "annotations": {"italic": True}})
#                     elif sub_part.startswith('`') and sub_part.endswith('`') and '\n' not in sub_part:
#                         rich_text.append({"type": "text", "text": {"content": sub_part[1:-1]}, "annotations": {"code": True}})
#                     elif sub_part.startswith('~~') and sub_part.endswith('~~'):
#                         rich_text.append({"type": "text", "text": {"content": sub_part[2:-2]}, "annotations": {"strikethrough": True}})
#                     elif sub_part.startswith('[') and '](' in sub_part and sub_part.endswith(')'):
#                         link_text, link_url = re.match(r'\[(.*?)\]\((.*?)\)', sub_part).groups()
#                         rich_text.append({"type": "text", "text": {"content": link_text, "link": {"url": link_url}}})
#                     else:
#                         rich_text.append({"type": "text", "text": {"content": sub_part}})
#         return rich_text

#     def flush_list():
#         nonlocal list_type, list_items
#         if list_items:
#             for item in list_items:
#                 blocks.append({
#                     "type": list_type,
#                     list_type: {
#                         "rich_text": create_rich_text(item)
#                     }
#                 })
#             list_type = None
#             list_items = []

#     for line in lines:
#         stripped_line = line.strip()
        
#         # 处理行间公式（公式块）
#         if (stripped_line.startswith('\\[') and stripped_line.endswith('\\]')) or equation_block:
#             if not equation_block:
#                 equation_block = True
#                 equation_content.append(stripped_line[2:-2])
#             elif stripped_line.endswith('\\]'):
#                 equation_content.append(stripped_line[:-2])
#                 blocks.append({
#                     "type": "equation",
#                     "equation": {
#                         "expression": '\n'.join(equation_content)
#                     }
#                 })
#                 equation_block = False
#                 equation_content = []
#             else:
#                 equation_content.append(stripped_line)
#             continue
        
#         # 处理代码块
#         elif stripped_line.startswith('```') and not code_block:
#             code_block = True
#             code_language = stripped_line[3:].strip() or 'plain text'
#             continue
#         elif stripped_line.startswith('```') and code_block:
#             blocks.append({
#                 "type": "code",
#                 "code": {
#                     "language": get_notion_language(code_language),
#                     "rich_text": [{"type": "text", "text": {"content": '\n'.join(code_content)}}]
#                 }
#             })
#             code_block = False
#             code_language = ''
#             code_content = []
#             continue
#         elif code_block:
#             code_content.append(line)  # 保留原始行，包括前导空格
#             continue
#         elif line.startswith('#'):
#             flush_list()
#             heading_level = len(line.split()[0])
#             heading_text = line.lstrip('#').strip()
#             blocks.append({
#                 "type": f"heading_{heading_level}",
#                 f"heading_{heading_level}": {
#                     "rich_text": create_rich_text(heading_text)
#                 }
#             })
#         elif line.startswith('> '):
#             flush_list()
#             blocks.append({
#                 "type": "quote",
#                 "quote": {
#                     "rich_text": create_rich_text(line[2:])
#                 }
#             })
#         elif line.startswith('- ') or line.startswith('* '):
#             if list_type != "bulleted_list_item":
#                 flush_list()
#                 list_type = "bulleted_list_item"
#             list_items.append(line[2:])
#         elif re.match(r'^\d+\. ', line):
#             if list_type != "numbered_list_item":
#                 flush_list()
#                 list_type = "numbered_list_item"
#             list_items.append(re.sub(r'^\d+\. ', '', line))
#         elif line.startswith('- [ ] ') or line.startswith('- [x] '):
#             flush_list()
#             checked = line.startswith('- [x] ')
#             blocks.append({
#                 "type": "to_do",
#                 "to_do": {
#                     "rich_text": create_rich_text(line[6:]),
#                     "checked": checked
#                 }
#             })
#         elif line.startswith('---'):
#             flush_list()
#             blocks.append({"type": "divider", "divider": {}})
#         elif line.strip() == '':
#             flush_list()
#         else:
#             flush_list()
#             blocks.append({
#                 "type": "paragraph",
#                 "paragraph": {
#                     "rich_text": create_rich_text(line)
#                 }
#             })

#     flush_list()
#     return blocks


def parse_markdown(content):
    blocks = []
    lines = content.split('\n')
    code_block = False
    code_language = ''
    code_content = []
    list_type = None
    list_items = []
    equation_block = False
    equation_content = []

    def get_notion_language(lang):
        lang_map = {
            'plaintext': 'plain text',
            'text': 'plain text',
            # 添加更多的映射关系
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

    def flush_list():
        nonlocal list_type, list_items
        if list_items:
            for item in list_items:
                blocks.append({
                    "type": list_type,
                    list_type: {
                        "rich_text": create_rich_text(item)
                    }
                })
            list_type = None
            list_items = []

    def process_equation(equation):
        return {
            "type": "equation",
            "equation": {
                "expression": equation.strip()
            }
        }

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()
        
        # 处理行间公式（公式块）
        if stripped_line.startswith('\\[') and stripped_line.endswith('\\]'):
            # 样式二：单行公式块
            blocks.append(process_equation(stripped_line[2:-2]))
            i += 1
        elif stripped_line.startswith('\\['):
            # 样式一：多行公式块
            equation_content = []
            while i < len(lines) and not lines[i].strip().endswith('\\]'):
                equation_content.append(lines[i].strip())
                i += 1
            if i < len(lines):
                equation_content.append(lines[i].strip()[:-2])  # 去掉结尾的 \]
            blocks.append(process_equation('\n'.join(equation_content)[2:]))  # 去掉开头的 \[
            i += 1
        
        # 处理代码块
        elif stripped_line.startswith('```') and not code_block:
            code_block = True
            code_language = stripped_line[3:].strip() or 'plain text'
            code_content = []
            i += 1
        elif stripped_line.startswith('```') and code_block:
            blocks.append({
                "type": "code",
                "code": {
                    "language": get_notion_language(code_language),
                    "rich_text": [{"type": "text", "text": {"content": '\n'.join(code_content)}}]
                }
            })
            code_block = False
            i += 1
        elif code_block:
            code_content.append(line)
            i += 1
        elif line.startswith('#'):
            flush_list()
            heading_level = len(line.split()[0])
            heading_text = line.lstrip('#').strip()
            blocks.append({
                "type": f"heading_{heading_level}",
                f"heading_{heading_level}": {
                    "rich_text": create_rich_text(heading_text)
                }
            })
            i += 1
        elif line.startswith('> '):
            flush_list()
            blocks.append({
                "type": "quote",
                "quote": {
                    "rich_text": create_rich_text(line[2:])
                }
            })
            i += 1
        elif line.startswith('- ') or line.startswith('* '):
            if list_type != "bulleted_list_item":
                flush_list()
                list_type = "bulleted_list_item"
            list_items.append(line[2:])
            i += 1
        elif re.match(r'^\d+\. ', line):
            if list_type != "numbered_list_item":
                flush_list()
                list_type = "numbered_list_item"
            list_items.append(re.sub(r'^\d+\. ', '', line))
            i += 1
        elif line.startswith('- [ ] ') or line.startswith('- [x] '):
            flush_list()
            checked = line.startswith('- [x] ')
            blocks.append({
                "type": "to_do",
                "to_do": {
                    "rich_text": create_rich_text(line[6:]),
                    "checked": checked
                }
            })
            i += 1
        elif line.startswith('---'):
            flush_list()
            blocks.append({"type": "divider", "divider": {}})
            i += 1
        elif line.strip() == '':
            flush_list()
            i += 1
        else:
            flush_list()
            blocks.append({
                "type": "paragraph",
                "paragraph": {
                    "rich_text": create_rich_text(line)
                }
            })
            i += 1

    flush_list()
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