
def title():
    # example: team1 vs team2: game# - day# week# splitseason year
    title = "hello"
    return title

def description():
    # example:
    # title and link to previous video
    # full game title again
    # team1 with all players full names and gameIDs
    # team2 with all players full names and gameIDs

    description = "This is a description"
    return description

def category():
    category = "Gaming"
    return category

def tags():
    tags = "tag1, tag2, tag3"
    return tags

def default_language():
    default_language = "en"
    return default_language

def client_secrets():
    client_secrets = "filepath\client-secrets.json"
    return client_secrets

def playlist():
    playlist = "playlist1"
    return playlist

def privacy():
    privacy = "public"
    return privacy

def upload():
    test = """youtube-upload --title="IMT vs APX" --description="IMT vs APX" --category=Gaming --client-secrets=C:\youtube_upload\youtube-upload-master\client_secrets.json E:\Youtube\Test/test_export.mp4"""
    directory = 'E:/Youtube/Test/game/'
    with open(os.path.join(directory, 'upload.bat'), 'w') as OPATH:
        OPATH.writelines(['@echo off \n',
                            'echo Uploading G1:',
                          '\n',
                          test])
def main():
    upload()

main()