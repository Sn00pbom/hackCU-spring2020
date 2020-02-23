import os
import json


class TChatHistory():

    def __init__(self, history_num: str):
        super().__init__()
        self._entries = []
        self._history_num = history_num

    def add_entry(self, timestamp, author, alias, content):
        self._entries.append(
            {
                'time': timestamp,
                'author': author,
                'alias': alias,
                'content': content
            }
        )

    def save(self):
        history_path = './data/{}.json'.format(self._history_num)
        with open(history_path, 'w') as f:
            f.write(json.dumps(self._entries, indent=4))

    @staticmethod
    def load(history_path):
        # entry_path = './data/{}.json'.format(entrynum)
        history_num = history_path.replace('.json', '')
        with open('./data/' + history_path, 'r') as f:
            jsd = json.loads(f.read())
        ch = TChatHistory(history_num)
        ch._entries = jsd
        return ch


def populate_convos():
    convos = {}
    for entry_path in os.listdir('./data'):
        history_num = entry_path.replace('.json', '')
        convos[history_num] = TChatHistory.load(entry_path)
    return convos
