import hashlib as hl
import json
import datetime as dt
import string
import random

class Block(object):

    def __init__(self, prev_hash, content):
        super().__init__()
        self._prev_hash = prev_hash
        self._dt = str(dt.datetime.utcnow().timestamp())
        self._content = content

    def _concat_all(self):
        return self._prev_hash + self._dt + self._content

    def convert_dict(self):
        return {'p': self._prev_hash, 't': self._dt, 'c': self._content}

    def compute_block_hash(self):
        return hl.sha256(bytes(self._concat_all(), 'utf-8')).hexdigest()


def rand_hash():
    s = ''
    for _ in range(64):
        s += random.choice(['a','b','c','d','e','f'] + list(string.digits))
    return s


def build_bigboi(length, name):
    root = Block(rand_hash(), rand_hash())
    bc = [root]
    for i in range(1, length):
        bc.append(Block(bc[i-1].compute_block_hash(), rand_hash()))

    bcd = [block.convert_dict() for block in bc]

    with open(name, 'w') as f:
        f.write(json.dumps(bcd))

if __name__ == "__main__":
    ti = dt.datetime.now()
    build_bigboi(1000000, './data/bigboi2.json')
    tf = dt.datetime.now()
    print(tf - ti)