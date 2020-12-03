import web_browser.report as browser_report
import http_request
import os
from typing import Dict


def load_config() -> Dict:
    """
    导入配置信息
    :return:
    """
    config = {}
    with open(os.path.join(__file__.split('/selfreport.py')[0], 'config.txt'), 'r') as f:
        lines = f.read().strip().split('\n')
        for line in lines:
            line = line.strip().split(',')
            config[line[0]] = line[1]
    return config


def main():
    config = load_config()
    if config['method'] == 'http':
        http_request.automatic_report(config)
    elif config['method'] == 'browser':
        browser_report.in_daily_report(config, is_moring=False)


if __name__ == '__main__':
    main()



