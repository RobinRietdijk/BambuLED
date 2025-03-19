import ujson

CONFIG_PATH = "config.json"
Config = {}

# Load config from file into memory
def load_config():
    global Config
    try:
        with open(CONFIG_PATH, "r") as f:
            Config = ujson.load(f)
    except (OSError, ValueError):
        print("Failed to read config.")

# Save global config data to file
def save_config():
    global Config
    with open(CONFIG_PATH, 'w') as f:
        ujson.dump(Config, f)