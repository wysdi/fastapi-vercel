import requests
from bs4 import BeautifulSoup


def parse_kurs():

    url = 'https://spreadsheets.google.com/feeds/list/1-NcBjMa6QOFHxMEpgtawvOlP8EQiPnCBsGaBU95mOSA/od6/public/values?alt=json&amp;callback=displayContent&_=1608704607798'
    data = requests.get(url).json()
    results = []
    for item in data['feed']['entry']:
        results.append({
            'bank': item['gsx$bank']['$t'],
            'beli': item['gsx$beli']['$t'],
            'jual': item['gsx$jual']['$t'],
        })

    return results


def parse_kebasa():

    url = 'https://infopasar.denpasarkota.go.id/?page=209&language=id&domain=&kategori_komoditas=KK001&pasar=PSR000002'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='table no-margin table-hover').find('tbody').find_all('tr')
    parent = ''
    data = []
    for tr in results:
        row = tr.find_all('td')
        nama = row[0].text
        if nama:
            parent = nama

        if len(row) > 1:
            jenis = row[1].text.replace('\n', '').replace('\t', '')
            harga = row[2].text.replace('\n', '').replace('\t', '')
            new_item = {
                'nama': parent,
                'jenis': jenis,
                'harga': harga
            }
            data.append(new_item)

    return data