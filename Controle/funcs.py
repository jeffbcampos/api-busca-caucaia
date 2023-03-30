import dropbox
from dotenv import load_dotenv
load_dotenv()
import os

app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
client = dropbox.Dropbox(access_token)

def uploadImg(img):
    #Faça upload do arquivo para o Dropbox
    response = client.files_upload(img.read(), '/' + img.filename)
    # Recupere o URL público gerado pelo Dropbox
    settings = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
    url = client.sharing_create_shared_link_with_settings(response.path_display, settings=settings).url
    return url.replace('dl=0', 'raw=1')
    