import os

# from cx_Freeze import setup, Executable


def find_all_scripts(directory):
    script_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                script_list.append(os.path.relpath(os.path.join(root, file)))
    return script_list


def parse_requirements(requirements_file):
    with open(requirements_file, mode="r", encoding="utf-8") as file:
        return [line.strip() for line in file]


all_scripts = find_all_scripts("source")
print(all_scripts)

required_modules = parse_requirements("requirements.txt")
print(required_modules)


# build_exe_options = {"packages": ["os"], "includes": ["tkinter"]}
# executables=[Executable("source/main.py", base=base)]

# setup(
#     name="smwc-browser",
#     version="1.0",
#     description="A browser for SMW Central",
#     executables=[Executable(script) for script in all_scripts],
#     options={
#         "build_exe": {
#             "packages": required_modules,
#         }
#     },
# )
