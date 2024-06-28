# coding:utf-8
import os

import yaml


class OkxConfig:
    """
    欧易相关的配置
    """
    api_key: str
    api_secret_key: str
    passphrase: str

    def __init__(self, api_key, api_secret_key, passphrase):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.passphrase = passphrase


class Config:
    """
    程序需要的配置信息
    """
    okx: OkxConfig

    def __init__(self, okx: OkxConfig):
        self.okx = okx


def init_config() -> Config:
    # 获取当前脚本所在文件夹路径
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    project_name = 'cryptocurrency-quantitative-robot'
    root_path = current_file_path[:current_file_path.find(project_name) + len(project_name)]
    # 获取yaml文件路径
    yaml_path = os.path.join(root_path, "config.yml")

    # open方法打开直接读出来
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config_str = f.read()

    d = yaml.load(config_str, Loader=yaml.FullLoader)  # 用load方法转字典

    okx_config = OkxConfig(d['okx']['api_key'], d['okx']['api_secret_key'], d['okx']['passphrase'])
    return Config(okx_config)


config = init_config()

if __name__ == '__main__':
    print(config)
