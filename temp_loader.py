import os
import json


class TChatHistory():

    def __init__(self, id: str):
        super().__init__()
        self._entries = []
        self._id = id

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
        id_path = './data/{}.json'.format(self._id)
        with open(id_path, 'w') as f:
            f.write(json.dumps(self._entries, indent=4))

    @staticmethod
    def load(id_path):
        # entry_path = './data/{}.json'.format(entrynum)
        id = id_path.replace('.json', '')
        with open('./data/' + id_path, 'r') as f:
            jsd = json.loads(f.read())
        ch = TChatHistory(id)
        ch._entries = jsd
        return ch


def populate_convos():
    convos = {}
    for entry_path in os.listdir('./data'):
        history_num = entry_path.replace('.json', '')
        convos[history_num] = TChatHistory.load(entry_path)
    return convos
