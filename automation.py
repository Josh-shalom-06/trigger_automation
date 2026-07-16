import subprocess
import os
import py_compile
import re

report = []

def add(line=""):
    print(line)
    report.append(line)

add("=" * 60)
add("PRE-MERGE VALIDATION REPORT")
add("=" * 60)

# ----------------------------------------------------
# Branch
# ----------------------------------------------------

branch = subprocess.check_output(
    ["git", "branch", "--show-current"]
).decode().strip()

add(f"Branch : {branch}")

if branch == "feature":
    add("Branch Validation : PASS\n")
else:
    add("Branch Validation : FAIL\n")

# ----------------------------------------------------
# Latest Commit
# ----------------------------------------------------

commit = subprocess.check_output(
    ["git", "log", "-1", "--pretty=%s"]
).decode().strip()

add(f"Latest Commit : {commit}")

bad_words = ["test", "temp", "abc", "wip"]

if any(word in commit.lower() for word in bad_words):
    add("Commit Message : FAIL\n")
else:
    add("Commit Message : PASS\n")

# ----------------------------------------------------
# Required Files
# ----------------------------------------------------

add("Required Files")

required = [
    "hello.py",
    "automation.py",
    "version.txt",
    ".github/workflows/feature_validation.yml",
    ".github/workflows/post_merge_validation.yml"
]

missing = False

for file in required:

    if os.path.exists(file):
        add(f"✓ {file}")

    else:
        add(f"✗ {file}")
        missing = True

if missing:
    add("\nRequired Files : FAIL\n")
else:
    add("\nRequired Files : PASS\n")

# ----------------------------------------------------
# Version Validation
# ----------------------------------------------------

add("Version Validation")

if os.path.exists("version.txt"):

    text = open("version.txt").read()

    version = re.search(r"Version\s*:\s*(.*)", text)
    build = re.search(r"Build\s*:\s*(.*)", text)

    if version and build:
        add(version.group(0))
        add(build.group(0))
        add("PASS\n")
    else:
        add("FAIL\n")

else:
    add("version.txt missing\n")

# ----------------------------------------------------
# Python Syntax
# ----------------------------------------------------

add("Python Syntax")

for file in ["hello.py", "automation.py"]:

    try:

        py_compile.compile(file, doraise=True)

        add(f"✓ {file}")

    except Exception as e:

        add(f"✗ {file}")
        add(str(e))

add()

# ----------------------------------------------------
# Changed Files
# ----------------------------------------------------

add("Files Changed")

try:

    files = subprocess.check_output(
        ["git", "diff", "--name-only", "origin/main"]
    ).decode().splitlines()

    if files:

        for f in files:
            add(f"✓ {f}")

    else:

        add("No files changed")

except:
    add("Unable to compare with origin/main")

add()

# ----------------------------------------------------
# Diff Statistics
# ----------------------------------------------------

add("Code Statistics")

try:

    stat = subprocess.check_output(
        ["git", "diff", "--shortstat", "origin/main"]
    ).decode()

    add(stat.strip())

except:
    add("Unavailable")

add()

# ----------------------------------------------------
# TODO Scanner
# ----------------------------------------------------

add("TODO Scan")

todo_found = False

for file in ["hello.py", "automation.py"]:

    with open(file) as f:

        for num, line in enumerate(f, 1):

            if "TODO" in line or "FIXME" in line:

                add(f"{file} : Line {num}")

                todo_found = True

if not todo_found:
    add("No TODOs found")

add()

# ----------------------------------------------------
# Final Result
# ----------------------------------------------------

add("=" * 60)
add("READY FOR REVIEW")
add("=" * 60)

with open("validation_report.txt", "w") as f:

    for line in report:
        f.write(line + "\n")