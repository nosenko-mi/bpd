import string
from itertools import zip_longest


def ascii_to_binary(text):
    binary_code = ""
    for char in text:
        binary_code += format(ord(char), '08b')
    return binary_code


def binary_to_hamming(binary_code):
    hamming_code = ""
    
    m = len(binary_code)
    r = calc_redundant_bits(m)

    arr = pos_redundant_bits(binary_code, r)
    arr = calc_parity_bits(arr, r)
    
    return arr


def split_string_chunks(text: str, chunk_size: int):
  chunks = []
  for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])
  return chunks


def is_correct_chunk_size(size)->bool:
    return ((size & (size-1) == 0) and size != 0)


def encode_file(filename: str, chunk_size: int):
    if (not is_correct_chunk_size(chunk_size)):
        print('Chunk size is not power of 2')
        return

    with open(filename, 'r') as file:
        text = file.read()

    binary_code = ascii_to_binary(text)
    r = calc_redundant_bits(len(binary_code))

    chunks = [binary_code]
    if (len(binary_code) + r > chunk_size):
        chunks = split_string_chunks(binary_code, chunk_size=chunk_size-r)       

    result = []
    binary_code = ''
    hamming_code = ''
    for c in chunks:
        hamming_code = binary_to_hamming(c)
        result.append(hamming_code)

    result_text = " ".join(result)
    print(result_text)
    with open(filename + ".encoded", 'w') as encoded_file:
        encoded_file.write(result_text)


# https://www.geeksforgeeks.org/hamming-code-implementation-in-python/
        

def calc_redundant_bits(m):

    # Use the formula 2 ^ r >= m + r + 1
    # to calculate the no of redundant bits.
    # Iterate over 0 .. m and return the value
    # that satisfies the equation

    for i in range(m):
        if (2**i >= m + i + 1):
            return i


def pos_redundant_bits(data, r):

    # Redundancy bits are placed at the positions
    # which correspond to the power of 2.
    j = 0
    k = 1
    m = len(data)
    res = ''

    # If position is power of 2 then insert '0'
    # Else append the data
    for i in range(1, m + r+1):
        if (i == 2**j):
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1

    # The result is reversed since positions are
    # counted backwards. (m + r+1 ... 1)
    return res[::-1]


def calc_parity_bits(arr, r):
    n = len(arr)

    # For finding rth parity bit, iterate over
    # 0 to r - 1
    for i in range(r):
        val = 0
        for j in range(1, n + 1):

            # If position has 1 in ith significant
            # position then Bitwise OR the array value
            # to find parity bit value.
            if (j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])
                # -1 * j is given since array is reversed

        # String Concatenation
        # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
        arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:]
    return arr


def detect_error(arr, nr):
    n = len(arr)
    res = 0

    # Calculate parity bits again
    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if (j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])

        # Create a binary no by appending
        # parity bits together.

        res = res + val*(10**i)

    # Convert binary to decimal
    return int(str(res), 2)


def restore_data(arr:list)->list:
    m = len(arr)
    r = calc_redundant_bits(m)
    error_index = detect_error(arr, r)
    true_index = len(arr)-error_index
    if (error_index == 0):
        return arr

    if (arr[true_index] == '0'):
        arr[true_index] = '1'
    else:
        arr[true_index] = '0'
    print(f'error in position: {error_index}')
    return arr


def main():
    # original = "01101101001101111011100011010010100100"
    # restored = ''.join(restore_data(list(original)))
    # print(f'original: {original}\nrestored: {restored}')
    encoded = encode_file('input_text', 64)


if __name__ == "__main__":
    main()