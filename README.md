# Luscious-Downloader
A program made for download Manga and Albums

# How to use
```py
album_id = None # ID de Manga, Hentai or Porn. None for random
```
You can get the ID from the URL, for example in
https://members.luscious.net/albums/big-hentai-collection-updates_397309/

The ID is `397309`

You can just put `None` for download a random album in `(Manga, Hentai or Porn)`

# Storage
The files are store in a folder named `files`, each ID code have his folder with his files and his `.json`

The `.json` contains a list with all files like:
```json
{
    "title": "file1",
    "type_name": "Picture",
    "url": "file1_url.png"
}
```

# To Do List
- [ ] Finish the random album
- [ ] Translate to Ensglish (Actually in Spanish)
- [ ] GUI
- [ ] Album name for folder name