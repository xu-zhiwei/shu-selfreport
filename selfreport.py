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
    in_daily_report(config, is_moring=True)


if __name__ == '__main__':
    main()



