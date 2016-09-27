import hashlib

def mongodb_id_convert(id):
    return hashlib.md5(id).hexdigest()[:24]