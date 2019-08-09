#!/usr/bin/python3

from config import Config
from config import ServerState
from app import app

def main() -> None:
    config = Config()

    if config.state() == ServerState.CONFIGURATION:
        app.run(host='0.0.0.0',debug=True)

if __name__ == '__main__':
    main()