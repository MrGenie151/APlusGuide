import os
import markdown
import shutil

def build(build_path="./build"):
    """
    Build HTML files from markdown and copy other files to the specified build directory.

    Args:
        build_path (str): The path where the build files will be stored. Defaults to "./build".
    """
    # Load the HTML template
    with open("template.html") as f:
        template = f.read()

    files_to_build = []
    files_to_copy = []

    # Traverse the source directory to find markdown and other files
    for root, _, files in os.walk("./src"):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, "./src")

            if file.endswith(".md"):
                files_to_build.append((file_path, relative_path, file[:-3]))
            else:
                files_to_copy.append((file_path, relative_path, file))

    # Build HTML files from markdown
    for file_path, relative_path, file_name in files_to_build:
        new_file_path = os.path.join(build_path, relative_path, f"{file_name}.html")

        with open(file_path, "r") as f:
            file_content = f.read()

        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

        with open(new_file_path, "w") as f:
            f.write(template.replace("[[content]]", markdown.markdown(file_content)))

    # Copy non-markdown files to the build directory
    for file_path, relative_path, file_name in files_to_copy:
        dest_path = os.path.join(build_path, relative_path, file_name)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copyfile(file_path, dest_path)

if __name__ == "__main__":
    build()
    build("./docs")
