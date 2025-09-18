from pathlib import Path


def collect_project_files(root_dir, extensions=('.py', '.html', '.txt')):
    root_path = Path(root_dir)
    file_contents = {}

    for file_path in root_path.rglob('*'):
        if file_path.is_file() and file_path.suffix in extensions:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_contents[str(file_path.relative_to(root_path))] = content
            except Exception as e:
                file_contents[str(file_path.relative_to(root_path))
                              ] = f"Error reading file: {str(e)}"

    return file_contents


def save_file_contents(output_file, file_contents):
    with open(output_file, 'w', encoding='utf-8') as f:
        for file_path, content in file_contents.items():
            f.write(f"\n\n--- File: {file_path} ---\n\n")
            f.write(content)


# Usage
root_dir = r'D:\Projects\10092025_v1'
output_file = r'D:\Projects\10092025_v1\project_files.txt'
file_contents = collect_project_files(root_dir)
save_file_contents(output_file, file_contents)
print(f"File contents saved to {output_file}")
