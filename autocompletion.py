import requests
from secrets import Secrets

session = requests.Session()

session.headers.update(
    {
        "Host": "gw.geneanet.org",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://gw.geneanet.org",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
)
def search(location):
    sec = Secrets()
    r = session.post(
        "https://gw.geneanet.org/setup/api/index.php",
        params={
            "sourcename": sec.secrets["geneanet"]["sourcename"],
            "type": "w",
            "lang": "en",
            "iz": "6",
            "arbre": "autocomplete",
        },
        headers={
            "Cookie": sec.secrets["geneanet"]["cookie"]
        },
        data={"data": f"%08%02%10%01%1A%01{location}%20%14"},
    )
    print(r.content.split(b'\n'))
    return r.content.split(b'\n')
