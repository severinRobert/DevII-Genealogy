import requests
import os
from zipfile import ZipFile
from secrets import Secrets

# Download GEDCOM file from geneanet.org and unzip it 

sec = Secrets()
s = requests.Session()
print(type(s))
s.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-GPC": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
)

r = s.get(
    "https://my.geneanet.org/arbre/save.php",
    params={"view": "save", "action": "save", "typefile": "arbre", "status": "done"},
    headers={
        "Host": "my.geneanet.org",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://my.geneanet.org/arbre/save.php?view=save",
        "Cookie": sec.secrets["geneanet"]["cookie"],
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    },
)

file = open("ged.zip", "w+b")
file.write(r.content)
file.close

ZipFile("ged.zip").extractall()

os.remove("ged.zip")
