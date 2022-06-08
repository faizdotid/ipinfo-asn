#HAYOOOOO NGAPAIN
import requests
from bs4 import BeautifulSoup

class IP_INFO:

    def __init__(self, asn):
        self.asn = asn
        self.api = 'https://ipinfo.io/'+asn
    
    def lookup_asn(self):
        try:
            resp = requests.get(self.api,
                                headers={'User-Agent': 'Mozilla/5.0'}, timeout=70)
            if '404' in resp.text:
                print('Cant gathering information for ASN {}'.format(self.asn))
            else:
                soup = BeautifulSoup(resp.text,
                                    features='html.parser')
                self.get_info(soup)
                self.get_ipv4range(soup)
        except Exception as e:
            print(e)

    def get_info(self, soup):
        new_soup = soup.find('div', class_='card card-details mt-0')
        print('\n\tABOUT THIS ASN {}'.format(self.asn))
        print('{}'.format(new_soup.find('h2').text))
        infos = new_soup.find_all('tr')
        for info in infos:
            new_info = info.find_all('td')
            key = new_info[0].text.strip()
            value = new_info[1].text.strip()
            print('{}: {}'.format(key, value))
    
    def get_ipv4range(self, soup):
        ipv4s = soup.find_all('table', class_='table table-bordered table-md table-details')[0]
        print('\n\n\tIPV4 RANGE FOR ASN {}'.format(self.asn))
        tbody = ipv4s.find('tbody')
        trs = tbody.find_all('tr')
        for tr in trs:
            ip_range = tr.find('td').find('a').string
            print('IPv4 RANGE {}'.format(ip_range))
            with open('ipv4_range.txt', 'a') as f:
                f.write('{}\n'.format(ip_range))


def main():
    print('''
\tASN LOOKUP
''')
    asn = input('ASN ? ')
    ip_info = IP_INFO(asn)
    ip_info.lookup_asn()

if __name__ == '__main__':
    main()