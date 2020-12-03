import http_request
from typing import Dict


def load_config() -> Dict:
    """
    导入配置信息
    :return:
    """
    config = {}
    with open('./http_request/config.txt', 'r') as f:
        lines = f.read().strip().split('\n')
        for line in lines:
            line = line.strip().split(',')
            config[line[0]] = line[1]
    return config


def main():
    config = load_config()
    http_request.automatic_report(config)


if __name__ == '__main__':
    main()



