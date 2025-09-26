import requests
import wget

class API_Handler():
    def __init__(self):

        with open('data/API_KEY.txt', 'r') as file:
            self.api_key = file.read()

        self.headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': self.api_key
        }

        self.url = 'https://api.curseforge.com/v1/'
        # self.url = 'https://www.curseforge.com/api/v1/' # used for downloads in browser

    def get_download_link(self, mod_id):
        response = requests.get(self.url + 'mods/' + str(mod_id), headers = self.headers)
        mod_data = response.json()
        # return mod_data.get("data", []).get("mainFileId", "")
        # https://www.curseforge.com/api/v1/mods/931874/files/6853336/download
        # https://www.curseforge.com/api/v1/mods/{modid}/files/{fileid}/download

        # mainfile_id = mod_data.get("data", []).get("mainFileId", "")
        # r = requests.get('https://api.curseforge.com/v1/mods/' + str(mod_id) + '/files/' + str(mainfile_id) + '/download-url', headers = self.headers)
        # print(f"Response status code: {r.status_code}")
        # print(r)

        return mod_data.get("data", []).get("mainFileId", "")

    def download_mod(self, mod_id, mainfile_id):
        # url = self.url + 'mods/' + str(mod_id) + '/files/' + str(mainfile_id) + '/download'
        url = 'https://www.curseforge.com/api/v1/mods/' + str(mod_id) + '/files/' + str(mainfile_id) + '/download'
        """ # response = requests.get(url, headers = self.headers)
        response = requests.get(url)

        if response.status_code == 200:
            filename = url.split("/")[-1]
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {url}: {response.status_code}") """

        wget.download(url, "mod.zip")

    def update_library_data(self, mod_id):
        return None
        
    def mod_search(self, params):
        r = requests.get(self.url + 'mods/search', params, headers = self.headers)
        
        """ params={
        'gameId': '83374'
        } """