from concurrent.futures import ThreadPoolExecutor, wait
from alive_progress import alive_bar
from colorama import Fore, init
import requests, json, os, urllib, re

init()
url = "https://members.luscious.net/graphqli/?"
album_id = None # ID de Manga, Hentai o Porno. Dejar en None para uno random

check = False
json_file = f"album_{album_id}.json"
os.makedirs(f"files/{json_file}", exist_ok=True)
if not os.path.exists(f"files/{json_file}/{json_file}"): 
    open(f"files/{json_file}/{json_file}", 'w').write("[]")
    check = True

# FUNCTIONS #
def get_random_album():
    # Entrar a un apartafo random y coger un album random

    return album_id

def download(title, url, bar):
    global json_file

    extension = re.findall(r'\.[0-9a-z]+$', url.lower())[0].lower()
    if os.path.isfile(f"files/{json_file}/{title}{extension}"):
        bar()
        return
        
    try: urllib.request.urlretrieve(url, f"files/{json_file}/{title}{extension}")
    except Exception as error:
        print(f"{Fore.LIGHTRED_EX}[{Fore.LIGHTWHITE_EX}-{Fore.LIGHTRED_EX}] Failed in url: {url} - Error: {str(error)}{Fore.LIGHTCYAN_EX}\n")

    bar.text(f"- {title}")
    bar()

def mass_download():
    file = open(f"files/{json_file}/{json_file}", "r", encoding='utf8')
    data = file.read()
    file.close()

    data = json.loads(data)
    lenght = len(data)

    futures = []
    print(Fore.LIGHTWHITE_EX)
    with alive_bar(lenght, title="Descargando", enrich_print=False) as bar:
        with ThreadPoolExecutor(max_workers=1000) as executor:
            for item in data:
                future = executor.submit(download, item["title"], item["url"], bar)
                futures.append(future)
    wait(futures)

def save(temp):
    file = open(f"files/{json_file}/{json_file}", "r", encoding='utf8')
    data = file.read()
    file.close()

    data = json.loads(data)
    for x in temp:
        if not x in data:
            data.append(x)
            print(Fore.LIGHTGREEN_EX + "[·] Recolectando... Added", end="\r")
        else: print(Fore.LIGHTRED_EX + "[·] Recolectando... Repeated", end="\r")

    file = open(f"files/{json_file}/{json_file}", "w+", encoding='utf8')
    file.write(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
    file.close()

def sender(n_page):
    global album_id, url

    if album_id is None: get_random_album()

    s_data = {
        "query": "query AlbumListOwnPictures($input: PictureListInput!) {\n  picture {\n    list(input: $input) {\n      info {...FacetCollectionInfo\n    }\n    items {\n      __typename\n      id\n      title\n      resolution\n      url_to_original\n      url_to_video\n      is_animated\n      url\n      thumbnails {\n        size\n        url\n      }\n    }\n    }\n  }\n}\nfragment FacetCollectionInfo on FacetCollectionInfo {\n  page\n  has_next_page\n  has_previous_page\n  total_items\n  total_pages\n  items_per_page\n  url_complete\n}",
        "variables": {
            "input": {
                "filters": [
                    {
                        "name": "album_id",
                        "value": str(album_id)
                    }
                ],
                "display": "rating_all_time",
                "page": int(n_page)
            }
        },
        "operationName": "AlbumListOwnPictures"
    }

    resp = requests.post(url, json=s_data)
    return resp.json()

def main():
    global check

    if not check: respuesta = input(Fore.LIGHTMAGENTA_EX + "[·] ¿Desea hacer todo el proceso? (S/n): ")
    else: respuesta = "S"

    if respuesta.lower() != "n":
        resp = sender(1)
        if len(resp["data"]["picture"]["list"]["items"]) == 0: return "[·] No es un album"

        info = resp["data"]["picture"]["list"]["info"]
        total_pages = info["total_pages"]
        total_items = info["total_items"]
        url_complete = info["url_complete"]

        print(total_pages)
        print(Fore.LIGHTCYAN_EX + f"[·] Total de archivos a recolectar: {total_items}")
        for i in range(int(total_pages)+1):
            if i == 0: continue

            resp = sender(i)
            items = resp["data"]["picture"]["list"]["items"]

            temp = []
            for item in items:
                type_name = item["__typename"]
                title = item["title"]
                f_url = item["url_to_original"]

                temp.append({"type_name":type_name, "title":title, "url":f_url})
            
            save(temp)

    print(Fore.LIGHTGREEN_EX + "\n\n[·] Descargando...")
    mass_download()
    print(Fore.LIGHTGREEN_EX + "[·] Proceso finalizado con exito!" + Fore.RESET)

if __name__ == "__main__":
    ret = main()
    if ret: print(Fore.LIGHTRED_EX + ret)