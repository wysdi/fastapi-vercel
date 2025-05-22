import requests
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal

def parse_kurs():
    kurs = []
    
    # Scrape BCA
    url = 'https://www.bca.co.id/en/informasi/kurs'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='m-table-kurs').find('tbody').find_all('tr')
    for tr in results:
        row = tr.find_all('td')
        nama = row[0].text.strip()
        if nama == 'USD':
            kurs.append({
                'bank': 'BCA',
                'jual': Decimal(sub(r'[^\d.]', '', row[1].text.strip())),
                'beli': Decimal(sub(r'[^\d.]', '', row[2].text.strip()))
            })

    # Helper function to scrape rates from kursdollar.org
    def scrape_kursdollar(bank_name, bank_url):
        page = requests.get(bank_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', {'class': 'in_table'})
        if table:
            rows = table.find_all('tr')
            for i in range(len(rows)):
                cells = rows[i].find_all('td')
                if len(cells) > 2 and cells[1].text.strip() == 'Beli':
                    # Get buy rate
                    buy_text = cells[2].text.strip()
                    buy_rate = buy_text.split('(')[0].strip()
                    buy_rate = buy_rate.replace('.', '')  # Remove thousand separator
                    buy_rate = buy_rate.replace(',', '.')  # Convert decimal separator
                    buy_rate = Decimal(buy_rate)
                    
                    # Get sell rate from next row
                    if i + 1 < len(rows):
                        next_cells = rows[i + 1].find_all('td')
                        if len(next_cells) > 2:
                            sell_text = next_cells[1].text.strip()
                            sell_rate = sell_text.split('(')[0].strip()
                            sell_rate = sell_rate.replace('.', '')
                            sell_rate = sell_rate.replace(',', '.')
                            sell_rate = Decimal(sell_rate)
                            
                            # For kursdollar.org banks, we need to switch beli/jual
                            kurs.append({
                                'bank': bank_name,
                                'beli': sell_rate,  # Switched
                                'jual': buy_rate    # Switched
                            })
                            break

    # Scrape OCBC and Mandiri from kursdollar.org
    scrape_kursdollar('OCBC', 'https://kursdollar.org/bank/ocbc.php')
    scrape_kursdollar('MANDIRI', 'https://kursdollar.org/bank/mandiri.php')

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