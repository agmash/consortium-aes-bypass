import re
import binascii
from collections import OrderedDict
from Crypto.Cipher import AES
import cloudscraper
import requests

session = cloudscraper.create_scraper(interpreter='native', debug=False)

def makeCookie(response):
    if 'slowAES.decrypt' in response.text:
        try:
            cryptVars = OrderedDict(re.findall(r'(a|b|c)=toNumbers\("(.*?)"\)', response.text))

            check = binascii.hexlify(
                AES.new(
                    binascii.unhexlify(cryptVars['a']),
                    AES.MODE_CBC,
                    binascii.unhexlify(cryptVars['b'])
                ).decrypt(
                    binascii.unhexlify(cryptVars['c'])
                )
            ).decode('ascii')

            data = {
                'url': response.text.split('location.href="')[1].split('"')[0],
                'cookie': [
                    response.text.split('document.cookie="')[1].split('=')[0],
                    check
                ]
            }

            print(f"Setting Human Check to {data['cookie'][1]}")

            return data
        except:
            return 0
    else:
        return 0

def monitor(url):

    response = session.get(url)

    cookie = makeCookie(response)

    if cookie != 0:
        requests.utils.add_dict_to_cookiejar(
            session.cookies,
            {
                cookie['cookie'][0]: cookie['cookie'][1]
            }
        )

        url = cookie['url']

        return monitor(url)

    print(response.text)

monitor('https://www.consortium.co.uk/polar-skate-co-stripe-puffer-ivory-navy-pol-f19-stripepuffer-ivonvy.html')
