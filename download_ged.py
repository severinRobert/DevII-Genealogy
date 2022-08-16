import requests
import os
from zipfile import ZipFile


# Download GEDCOM file from geneanet.org and unzip it 


s = requests.Session()

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
        "Cookie": "autolang=en; _ga_4QT8FMEX30=GS1.1.1659909436.4.0.1659909436.0; _ga=GA1.1.749358828.1659863750; REMEMBERME=R2VuZWFuZXRcQnVuZGxlXFVzZXJCdW5kbGVcRW50aXR5XFVzZXI6WTJKeWRXa3hOdz09OjE2NjU0MjczNzU6MTA5ZmM3NDhlNjNhYmUxZDg1MWFmOTY0OGFjNDZmOTU3YmQ2ZGY3YjY1ODZmNzc2N2Y2ZDAwMWFhYmU3MWQwMg%3D%3D; gntsess5=a48c616dab161f71fc93930eefa01b44; geopays=BEL; gntsess=4_cbrui17_87f6d0bcaa8e2cd68e07685f6c9f4380; autologin=cbrui17; tarteaucitron=!gajs=true!googletagmanager=true!facebook=true!twitter=true!dailymotion=true!vimeo=true!youtube=true; screenfix=0; dtjs=1660481832135",
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
