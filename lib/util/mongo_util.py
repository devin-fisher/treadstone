import hashlib

def mongodb_id_convert(id):
    return hashlib.md5(id).hexdigest()[:24]

if __name__ == "__main__":
    print(mongodb_id_convert('95ada0b9-bece-48cc-bd48-d9ee5bde901e'))