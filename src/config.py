import os
import yaml

path = os.getenv('APPDATA') + "/mobileorders"
config_file = "config.yml"
values = {}


def update_config(data):
    global values
    values = data

    with open(path + "/" + config_file, "w") as f:
        f.write(yaml.dump(data))


def create_config():
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

    if not os.path.exists(path + "/" + config_file):
        with open(path + "/" + config_file, "w") as f:
            f.write(yaml.dump(defaults()))

    global values
    values = yaml.safe_load(open(path + "/" + config_file, "r"))


def defaults():
    default_values = {
        "output_directory": os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
        "output_file_name": "Orders"
    }

    return default_values
