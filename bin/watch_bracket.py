import sys
from pymongo import MongoClient
import hashlib


def mongodb_id_convert(id_val):
    return hashlib.md5(id_val).hexdigest()[:24]


def main(args):
    new_dict = dict()
    new_dict['_id'] = mongodb_id_convert(args[3])
    new_dict['league'] = args[1]
    new_dict['tournament_id'] = args[2]
    new_dict['bracket_id'] = args[3]
    new_dict['watched'] = True
    client = MongoClient()
    collection = client.lol.watched_brackets
    collection.update({'_id': mongodb_id_convert(args[3])}, new_dict, upsert=True)

if __name__ == "__main__":
    main(sys.argv)
