import os

import yaml

YAML_FILE_PATH = "config/config.yaml"


# 加载 YAML 文件
def load_yaml():
    if os.path.exists(YAML_FILE_PATH):
        with open(YAML_FILE_PATH, "r") as file:
            return yaml.safe_load(file) or {"users": []}
    return {"users": []}


# 保存 YAML 文件
def save_yaml(data):
    with open(YAML_FILE_PATH, "w") as file:
        yaml.dump(data, file)
