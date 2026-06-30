import requests
import wget
import pylnk3
import sys


class API_Handler:
    def __init__(self):

        api_key_link = pylnk3.parse("data/API_KEY.txt.lnk")
        with open(api_key_link.path, "r") as file:
            self.api_key = file.read()

        self.headers = {"Content-Type": "application/json", "Accept": "application/json", "x-api-key": self.api_key}

        self.url = "https://api.curseforge.com/v1/"
        # self.url = 'https://www.curseforge.com/api/v1/' # used for downloads in browser

    def get_mainFileId(self, mod_id):
        response = requests.get(self.url + "mods/" + str(mod_id), headers=self.headers)
        mod_data = response.json()
        # return mod_data.get("data", []).get("mainFileId", "")
        # https://www.curseforge.com/api/v1/mods/931874/files/6853336/download
        # https://www.curseforge.com/api/v1/mods/{modid}/files/{fileid}/download

        # mainfile_id = mod_data.get("data", []).get("mainFileId", "")
        # r = requests.get('https://api.curseforge.com/v1/mods/' + str(mod_id) + '/files/' + str(mainfile_id) + '/download-url', headers = self.headers)
        # print(f"Response status code: {r.status_code}")
        # print(r)

        return mod_data.get("data", []).get("mainFileId", "")

    # Custom progress bar function
    def progress_bar(current, total, width=50):
        """
        Displays a progress bar in the console.
        :param current: Bytes downloaded so far
        :param total: Total bytes to download
        :param width: Width of the progress bar
        """
        progress_message = f"Downloading: {current / total * 100:.2f}% [{current}/{total} bytes]"
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    def download_mod(self, mod_id, mainfile_id):
        # url = self.url + 'mods/' + str(mod_id) + '/files/' + str(mainfile_id) + '/download'
        url = "https://www.curseforge.com/api/v1/mods/" + str(mod_id) + "/files/" + str(mainfile_id) + "/download"
        """ # response = requests.get(url, headers = self.headers)
        response = requests.get(url)

        if response.status_code == 200:
            filename = url.split("/")[-1]
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {url}: {response.status_code}") """

        try:
            print(f"Trying to download mod {mod_id} with main file {mainfile_id}")
            print(f"URL: {url}")
            filename = wget.download(url, out=f"downloads\\{mod_id}.zip")  # , bar=self.progress_bar)
            print(f"\nDownload complete: {filename}")
        except Exception as e:
            print(f"\nError downloading mod: {e}")

    def download_mod_entry(self, mod_id):
        response = requests.get(self.url + "mods/" + str(mod_id), headers=self.headers)
        if response.status_code == 200:
            mod_cf_data = response.json()
            # mod_library_entry = {}
            print("Mod entry " + str(mod_id) + " downloaded.")
            return mod_cf_data
        print("Failed to download mod info to update library.json entry.")

    def mod_search(self, params):
        r = requests.get(self.url + "mods/search", params, headers=self.headers)

        """ params={
        'gameId': '83374'
        } """
