from pathlib import Path
import os

dest = Path("pathpy_output.txt")

def createFile(dest):
    exists = dest.exists()

    with open(dest, "w") as f:
        if exists:
            f.write("Update text goes here")
            print("updated file")
        else:
            f.write("created file")
            print("created file")

createFile(dest)

print(dest.exists(), "exists")
print("Running from:", os.getcwd())