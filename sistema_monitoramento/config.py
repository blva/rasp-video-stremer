import json
from enum import Enum

STATE_KEY = 'state'
CONFIG_FILE = 'config.json'

class ServerState(Enum):
    CONFIGURATION = 0
    WORKING = 1

class Config:
    def __init__(self):
        self.data = {}

    def update(self):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as json_file:
            self.data = json.load(json_file)
    
    def save(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def state(self) -> 'ServerState':
        self.update()
        return ServerState(self.data[STATE_KEY])

    def write_state(self, state: 'ServerState') -> None:
        self.data[STATE_KEY] = state.value
        self.save()