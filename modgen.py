import os
import sys
import uuid
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape

script_version = "1.0.0"

games = {"Outward": "Outward"}

values = {
    "name": "ModTemplate",
    "guid": "mod.template",
    "author": "ModAuthor",
    "version_number": "1.0.0",
    "website_url": "",
    "description": "This is a mod",
    "bepinex_version": "5.4.18",
    "project_prefix": "",
}


def read_value(text, name, default=None):
    new_val = input("{0} ({1}): ".format(text, default if default else values[name]))
    if new_val:
        values[name] = new_val
    elif default:
        values[name] = default


projects_root = sys.argv[1] if len(sys.argv) > 1 else ""

print("##### ModGen {0} #####".format(script_version))

# Game selector
print("Select game:")
game_list = []
index = 0
for game_id, disp_name in games.items():
    game_list.append(game_id)
    print("{0}: {1}".format(index, disp_name))
    index += 1
game = game_list[int(input("> "))]
print("Selected game: {0}".format(games[game]))


# Patcher or not
create_patcher = (input("> Create patcher project [y/n]? (n)") == "y")


# Generator params
print("Please enter mod generator parameters (default value is in parentheses)".format(script_version))
read_value("> Mod name (.NET project name: no spaces and special characters)", "name")
read_value("> Author", "author")
read_value("> Mod GUID", "guid", "{0}.{1}".format(values["author"].lower(), values["name"].lower()))
read_value("> Version number", "version_number")
read_value("> Website URL", "website_url")
read_value("> Mod description", "description")
read_value("> BepInEx version", "bepinex_version")
read_value("> Mod project prefix", "project_prefix", game)

mod_project_name = values["project_prefix"]+values["name"]
mod_root = os.path.join(projects_root, mod_project_name)

# Create folder structure
os.makedirs(os.path.join(mod_root, "meta"))
os.makedirs(os.path.join(mod_root, "plugin", "Properties"))
if create_patcher:
    os.makedirs(os.path.join(mod_root, "patcher", "Properties"))


# Render files
values["plugin_uuid"] = str(uuid.uuid4())
values["patcher_uuid"] = str(uuid.uuid4())

env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())

print("Writing project files")
for template_name in env.list_templates(filter_func=lambda tname: True if create_patcher else not tname.startswith("patcher") ):
    template = env.get_template(template_name)
    file_name = template_name.replace(".jinja2", "")
    file_name = file_name.replace("Mod.sln", "{0}.sln".format(mod_project_name))
    file_name = file_name.replace("Plugin.cs", "{0}.cs".format(values["name"]))
    file_name = file_name.replace("Patcher.cs", "{0}Patcher.cs".format(values["name"]))
    output_file = os.path.join(mod_root, file_name)
    print("> {0}".format(output_file))
    template.stream(values).dump(output_file)


# Generate manifest.json
print("Writing manifest.json")
manifest = {"name": values["name"],
            "author": values["author"],
            "version_number": values["version_number"],
            "website_url": values["website_url"],
            "description": values["description"],
            "dependencies": [],
            "artifacts": {
                "plugin": [],
                "patcher": []
            }}
if game == "Outward":
    manifest["dependencies"] = [
        "BepInEx-BepInExPack_Outward-{0}".format(values["bepinex_version"])
    ]

with open(os.path.join(mod_root, "meta", "manifest.json"), "w") as fp:
    json.dump(manifest, fp, indent=4)

print("Done!")
input("Press any key to exit")
