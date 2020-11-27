from report import in_daily_report


def load_config():
    config = {}
    with open('./config.txt', 'r') as f:
        lines = f.read().strip().split('\n')
        for line in lines:
            line = line.strip().split(',')
            config[line[0]] = line[1]
    return config


def main():
    config = load_config()
    for _ in range(3):  # 连报多次，防止由于网络等因素，导致填报失败
        in_daily_report(config, is_moring=True)


if __name__ == '__main__':
    main()



