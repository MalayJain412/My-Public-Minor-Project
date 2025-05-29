import os

# Root directory to start searching from
ROOT_DIR = r"D:\ML Folders\ml_env\GitHub\My-Public-Minor-Project"

# File extensions to include
INCLUDE_EXTENSIONS = {'.py', '.js', '.css', '.html', '.txt'}

# Output file where combined code will be saved
OUTPUT_FILE = os.path.join(ROOT_DIR, "all_code_snippets.txt")

def should_include(file_name):
    return os.path.splitext(file_name)[1] in INCLUDE_EXTENSIONS

def copy_code_snippets():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for dirpath, _, filenames in os.walk(ROOT_DIR):
            for filename in filenames:
                if should_include(filename):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            outfile.write(f"\n\n----- File: {file_path} -----\n")
                            outfile.write(content)
                    except Exception as e:
                        print(f"Could not read {file_path}: {e}")

    print(f"\n✅ Code snippets copied to: {OUTPUT_FILE}")

if __name__ == "__main__":
    copy_code_snippets()
