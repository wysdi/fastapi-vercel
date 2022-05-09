import requests
from bs4 import BeautifulSoup


def parse_kurs():

    url = 'https://www.bca.co.id/en/informasi/kurs'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='m-table-kurs').find('tbody').find_all('tr')
    kurs = []
    for tr in results:
        row = tr.find_all('td')
        nama = row[0].text.strip()
        if nama == 'USD':
            kurs.append({
                'bank': 'BCA',
                'jual': Decimal(sub(r'[^\d.]', '', row[1].text.strip())),
                'beli': Decimal(sub(r'[^\d.]', '', row[2].text.strip()))
            })

    return kurs


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