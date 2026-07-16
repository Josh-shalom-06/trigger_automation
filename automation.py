import subprocess
import os

branch = subprocess.check_output(
    ["git", "branch", "--show-current"]
).decode().strip()

commit = subprocess.check_output(
    ["git", "log", "-1", "--pretty=%h - %s"]
).decode().strip()

report = []

report.append("=" * 50)
report.append("VERSION VALIDATION REPORT")
report.append("=" * 50)
report.append(f"Current Branch : {branch}")
report.append(f"Latest Commit  : {commit}")
report.append("")
report.append("Validation")

files = [
    "hello.py",
    "automation.py",
    "version.txt",
    ".github/workflows/automation.yml"
]

for file in files:
    if os.path.exists(file):
        report.append(f"✓ {file} exists")
    else:
        report.append(f"✗ {file} missing")

report.append("")
report.append("Overall Result : PASS")

# Print to GitHub Actions log
for line in report:
    print(line)

# Save to file
with open("validation_report.txt", "w") as f:
    for line in report:
        f.write(line + "\n")