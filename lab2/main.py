import pyDes

def text_to_binary(text):
    binary_code = ""
    for char in text:
        binary_code += format(ord(char), '08b')
    return binary_code


def hex_to_binary(hex_string):
    hex = hex_string.replace(" ", "")
    string = bin(int(hex, 16))[2:]
    string = string.zfill(4 * (len(hex)))
    return string


def encrypt_decrypt(data, key):
    desObj = pyDes.des(key=key)
    encrypted = desObj.encrypt(data)
    decrypted = desObj.decrypt(encrypted)

    print(f'key: {key}, raw data: {data}\n encrypted data: {encrypted.hex()}\n decrypted data: {decrypted}')


def main():

    key, data = "", ""
    with open('./lab2_input', 'r') as file:
        text = file.read()
        splitted = text.split(';')
        data = splitted[0]
        key = splitted[1]

    encoded_data = data.encode('ascii')


    encrypt_decrypt(encoded_data, key)

    print('-----------------------------')
    
    hex1 = '01 23 45 67 89 AB CD EF'
    key1= 'FE FE FE FE FE FE FE FE'
    s1 = bytearray.fromhex(hex1)

    hex2 = '00 00 00 00 00 00 00 00'
    key2 = '00 00 00 00 00 00 00 00'
    s2 = bytearray.fromhex(hex2)

    hex3 = '01 23 45 67 89 AB CD EF'
    key3 = 'FE DC BA 98 76 54 32 10'
    s3 = bytearray.fromhex(hex3)

    print('Example 1')
    encrypt_decrypt(s1, bytearray.fromhex(key1))

    print('Example 2')
    encrypt_decrypt(s2, bytearray.fromhex(key2))

    print('Example 2')
    encrypt_decrypt(s3, bytearray.fromhex(key3))



if __name__ == "__main__":
    main()