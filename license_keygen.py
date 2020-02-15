#! python3

# License keygen for CatDV Backup Control Panel


mac_clean = "6C4008B9707E"  # enter user's Installation ID here
installationid = mac_clean.upper()  # convert to uppercase
# pad installationid to 16 digits and zip with 'Langrall' expressed as hex string
zipped = list(zip(installationid.join('0000'), list('4C616E6772616C6C')))
software_key = ''.join([i for sub in zipped for i in sub])  # zipped is a list of 2-tuples
# print("software_key:", software_key)

# vigenere encryption


def vign(txt='', key='', typ='d'):
    # universe of all possible characters.
    universe = list('1234567890ABCDEFGHJKLMNPQRSTUVWXYZ')  # alphanum, no 'I or 'O'
    uni_len = len(universe)
    if not txt:
        print('Needs text.')
        return
    if not key:
        print('Needs key.')
        return
    if typ not in ('d', 'e'):
        print('Type must be "d" or "e".')
        return
    if any(t not in universe for t in key):
        print('Invalid characters in the key. Must only use ASCII symbols.')
        return

    ret_txt = ''
    k_len = len(key)

    for i, l in enumerate(txt):
        if l not in universe:
            ret_txt += l
        else:
            txt_idx = universe.index(l)

            k = key[i % k_len]
            key_idx = universe.index(k)
            if typ == 'd':
                key_idx *= -1

            code = universe[(txt_idx + key_idx) % uni_len]

            ret_txt += code

    return(ret_txt)


def authenticate():
    print("software_key:", software_key)
    # end user software decrypts license key
    # # this is how encryption works:
    l_key = vign(software_key, software_key, 'e')
    print("encrypted:", l_key)  # this is the software license key
    customer_license = '-'.join(l_key[i:i+4] for i in range(0, len(l_key), 4))
    print("customer license:", customer_license)

    # this is how decryption workset            decrypted = vign(l_key, software_key, 'd')
    decrypted = vign(l_key, software_key, 'd')
    print("decrypted:", decrypted)
    if decrypted == software_key:
        # self.authenticated = True  # license is valid
        print("license is valid")


authenticate()
