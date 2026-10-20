import os
from pathlib import Path

from notion_client import Client
from notion_git_sync.sync import Config, NotionSync

def main():
    token = os.environ["NOTION_TOKEN"].strip()
    parent = os.environ["NOTION_PARENT_ID"].strip()

    if not token:
        raise ValueError("NOTION_TOKEN environment variable is not set")
    if not parent:
        raise ValueError("NOTION_PARENT_ID environment variable is not set")

    output_dir = Path("docs/notion")
    output_dir.mkdir(parents=True, exist_ok=True)

    config = Config(
        notion_client=Client(auth=token),
        parent_ids=[parent],
        output_dir=output_dir,
        required_frontmatter=set(),
    )

    changed = NotionSync(config).sync()
    print(f"Synced {len(changed)} pages")
    print(f"Changed pages: {', '.join(str(file) for file in changed)}")

if __name__ == "__main__":
    main()