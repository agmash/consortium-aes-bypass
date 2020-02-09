import re
import binascii
from collections import OrderedDict
from Crypto.Cipher import AES

def makeCookie(self, response):
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
                'url':response.text.split('location.href="')[1].split('"')[0],
                'cookie':[
                    response.text.split('document.cookie="')[1].split('=')[0],
                    check
                ]
            }

            self.status(f"Setting Human Check to {data['cookie'][1]}")

            return data
        except:
            return 0
    else:
        return 0
