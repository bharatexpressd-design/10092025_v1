import subprocess
import os

files = [
    'logistics/admin.py',
    'logistics/models.py',
    'logistics/views.py',
    'logistics/urls.py',
    'marketing/models.py',
    'marketing/admin.py',
    'marketing/views.py',
    'marketing/urls.py',
    'ecommerce/urls.py'
]

for file in files:
    print(f"Checking {file}...")
    result = subprocess.run(['python', '-m', 'py_compile', file], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{file}: OK")
    else:
        print(f"{file}: ERROR\n{result.stderr}")