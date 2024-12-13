import os
import markdown
import shutil

def build(build_path="./build"):
    template = ""
    with open("template.html") as f:
        template = f.read()

    files_to_build = []
    files_to_copy = []
    for root, dirs, files in os.walk("./src"):
        for file in files:
            if file[-3:] == ".md":
                print(os.path.relpath(root,"./src"))
                print(file[:-3])
                files_to_build.append([root + "/" + file,os.path.relpath(root,"./src"),file[:-3]])
            else:
                files_to_copy.append([root + "/" + file,os.path.relpath(root,"./src"),file])
    #print(files_to_build)

    for file_info in files_to_build:
        file_name = file_info[2]
        file_orig_path = file_info[0]
        file_rel_path = file_info[1]
        file_markdown = ""
        file_new_path = build_path + "/" + file_rel_path + "/" + file_name + ".html"

        with open(file_orig_path,"r") as f:
            file_markdown = f.read()
        
        os.makedirs(os.path.dirname(file_new_path), exist_ok=True)
        with open(file_new_path,"w") as f:
            f.write(template.replace("[[content]]",markdown.markdown(file_markdown)))

    for thing in files_to_copy:
        os.makedirs(os.path.dirname(file_new_path), exist_ok=True)
        shutil.copyfile(thing[0],build_path + "/" + thing[1] + "/" + thing[2])

if __name__ == "__main__":
    build("./docs")