import os
from notion_client import Client

# 从环境变量获取 Notion Token
notion_token = os.getenv("NOTION_TOKEN")

# 创建Notion客户端
notion = Client(auth=notion_token)

# 页面ID
page_id = "112cef0dda3e80ff9f03e2ba31341cb6"

# 添加内容的函数
def append_to_notion_page():
    # 生成需要追加的块结构
    blocks = [
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "冰箱里的物品"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": "水果"}}],
                        },
                    },
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": "橘子"}}],
                        },
                    },
                ],
            },
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "板凳上的物品"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": "杯子"}}],
                        },
                    },
                ],
            },
        },
    ]

    # 向指定页面追加块内容
    notion.blocks.children.append(page_id, children=blocks)


# 执行函数
append_to_notion_page()


def append_more_to_notion_page():
    # 生成需要追加的块结构
    blocks = [
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "git diff：如果你想查看具体哪些地方不同，可以使用git diff命令。以下命令可以用来比较本地分支和远程分支："}}],
                "children": [
                    {
                        "object": "block",
                        "type": "code",
                        "code": {
                            "rich_text": [{"type": "text", "text": {"content": "git diff <remote>/<branch>"}}],
                            "language": "bash"
                        },
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "或者如果你想看所有分支的不同："}}],
                        },
                    },
                    {
                        "object": "block",
                        "type": "code",
                        "code": {
                            "rich_text": [{"type": "text", "text": {"content": "git diff --stat <remote>"}}],
                            "language": "bash"
                        },
                    },
                ],
            },
        }
    ]

    # 向指定页面追加块内容
    notion.blocks.children.append(page_id, children=blocks)

# 执行函数
append_more_to_notion_page()