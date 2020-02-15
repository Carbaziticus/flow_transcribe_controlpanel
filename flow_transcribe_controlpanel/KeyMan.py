#! python3

# KeyMan.py
# KeyManager authentication employing Vegenere decryption

# import os
import SysInfo
import CPio
import FileInfo


class authentication():
    # catdvBackuControlPanel app gets user machine eth0 MAC address at launch,
    # strips out the colons, converts to upper case.
    # Here we zipper the MAC address with an embedded magic token, e.g.:
    # 'Langrall': 4c 61 6e 67 72 61 6c 6c (16 digits, all caps, no spaces)
    # this becomes the user's unique and private "product key".
    # user emails their installation ID (cleaned up MAC address) to developer
    # Magic token is known to developer
    # developer deduces user's "product key" by zippering token with installation ID.
    # developer encrypts the product key and emails this as a "license" back to the user
    # user enters license, and we attempt to decrypt it into the product key here.
    def __init__(self):
        self.authenticated = False  # assume unlicensed
        self.installationid = SysInfo.macAddress().upper()
        print("installation ID: ", self.installationid)
        # pad installationid to 16 digits and zip with 'Langrall' expressed as hex string
        zippered = list(zip(self.installationid.join('0000'), list('4C616E6772616C6C')))
        self.product_key = ''.join([i for sub in zippered for i in sub]
                                   )  # zippered is a list of 2-tuples
        self.cp_license = CPio.readCP(FileInfo.licensePath())
        if self.cp_license.sections() == []:  # test if cp object is empty (no sections)
            print("no license file")  # infer that cp did not find a valid license.txt file
            # preserve case in the cp key names
            self.cp_license.optionxform = lambda option: option
            # initialize the cp_license object with a section, two keys and no values
            self.cp_license['License'] = {'Registered to': '',
                                          'Registration code': ''}
        else:  # set registered_to and license_key from cp obj
            self.registered_to = self.cp_license['License']['Registered to']
            self.license_key = self.cp_license['License']['Registration code']
            print("license file found")
            self.authenticate()  # attempt to authenticate

    def authenticate(self):  # test the license_key
        # end user software decrypts license key
        test_key = self.license_key.replace('-', '')  # remove hyphens for test
        print("test_key: ", test_key)
        # print("product_key: ", self.product_key)
        decrypted = vign(test_key, self.product_key, 'd')
        # print("decrypted:", decrypted)
        if decrypted == self.product_key:
            self.authenticated = True  # license is valid
            # update cp_license object if changed and write it to disk
            if self.registered_to != self.cp_license.get('License', 'Registered to') or \
                    self.license_key != self.cp_license.get('License', 'Registration code'):
                self.cp_license.set('License', 'Registered to', self.registered_to)
                self.cp_license.set('License', 'Registration code', self.license_key)
                CPio.writeCP(self.cp_license, FileInfo.licensePath())
        else:
            self.authenticated = False  # license is not valid
        print("authenticated:", self.authenticated)


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

#  licensing options/ideas for uniquely identifying the host system:
# print(hex(uuid.getnode()))  # MAC address, unformatted (but which nic?)
# print(':'.join(re.findall('..', '%012x' % uuid.getnode())))  # MAC address formatted
# if SysInfo.system() == 'Darwin':
#     cmd = "ifconfig en0 | grep 'ether' | awk '{print $2}'"
#     result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True)
#     print(result)
#     result = result.stdout.strip()  # logic board serial number
#     mac_address_en0 = result.decode('UTF8')
#     print(mac_address_en0)
# elif SysInfo.system() == 'Windows':
#     cmd = "ipconfig /all | find \"Physical Address\""
#     result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True)
#     result = result.stdout.strip()
#     mac_address = result.decode('UTF8')
#     mac_address = mac_address.split(': ')
#     print(mac_address[1])  # a currently connected ethernet hardware interface address

# print(socket.gethostname())  # hostname
#
# cmd = "system_profiler SPHardwareDataType | grep 'Serial Number' | awk '{print $4}'"
# result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True)
# serial_number = result.stdout.strip()  # logic board serial number
# print(serial_number)
