import os
import json
from datetime import datetime

CATALOG_FILE = "PROJECTS.md"
PROJECTS_DIR = "."  

def read_project_metadata(folder):
    project_json = os.path.join(folder, "project.json")
    readme_file = os.path.join(folder, "README.md")

    if not os.path.exists(project_json):
        return None

    with open(project_json, "r", encoding="utf-8") as f:
        meta = json.load(f)

    # Fallback: extract short description from README
    if not meta.get("description") and os.path.exists(readme_file):
        with open(readme_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            meta["description"] = first_line.replace("#", "").strip()

    return meta


def generate_markdown_table(projects):
    header = "| Project | Description | Tech Stack | Status | Repo | Deployment | Docs |\n"
    header += "|----------|--------------|-------------|---------|-------|-------------|------|\n"

    rows = []
    for p in projects:
        name = f"**{p.get('name', '-') }**"
        desc = p.get("description", "-")
        stack = ", ".join(p.get("stack", []))
        status = p.get("status", "-")
        repo = f"[GitHub]({p['repo']})" if p.get("repo") else "—"
        deploy = p.get("deployment", "—")
        docs = f"[Docs]({p['docs']})" if p.get("docs") else "—"

        rows.append(f"| {name} | {desc} | {stack} | {status} | {repo} | {deploy} | {docs} |")

    return header + "\n".join(rows)


def main():
    projects = []

    for item in os.listdir(PROJECTS_DIR):
        if os.path.isdir(item) and not item.startswith("."):
            meta = read_project_metadata(item)
            if meta:
                projects.append(meta)

    if not projects:
        print("⚠️ No projects with project.json found.")
        return

    # Sort alphabetically
    projects.sort(key=lambda x: x["name"].lower())

    md = "# 🗂️ Project Catalog\n\n"
    md += "Auto-generated project index.\n\n"
    md += generate_markdown_table(projects)
    md += f"\n\n_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_\n"

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"✅ Updated {CATALOG_FILE} with {len(projects)} projects.")


if __name__ == "__main__":
    main()
