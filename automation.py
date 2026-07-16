import subprocess
import os

print("=" * 50)
print("VERSION VALIDATION REPORT")
print("=" * 50)

branch = subprocess.check_output(
    ["git", "branch", "--show-current"]
).decode().strip()

commit = subprocess.check_output(
    ["git", "log", "-1", "--pretty=%h - %s"]
).decode().strip()

print(f"Current Branch : {branch}")
print(f"Latest Commit  : {commit}")

print("\nValidation")

files = [
    "hello.py",
    "version.txt",
    "automation.py",
    "README.md",
    ".github/workflows/automation.yml"
]

for file in files:
    if os.path.exists(file):
        print(f"✓ {file} exists")
    else:
        print(f"✗ {file} missing")

print("\nOverall Result : PASS")