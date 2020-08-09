#import sys
import os
import numpy as np
#%%

def generateDictionary(w, number_of_symbols,sym_list):
    '''
    Reads the file sym_list and generates the dictionary required for LZ coding

    Parameters
    ----------
    w : integer denoting the length of Dictionary
        DESCRIPTION.
    number_of_symbols : integer denoting the number of symbols in character set
        DESCRIPTION.
    sym_list : A string containing the file name from which dictionary has to be constructed.

    Returns
    -------
    dictionary : returns a string of dictionary 

    '''
    file_read = open(sym_list, "r")
    no_of_bits = int(np.ceil(np.log2(number_of_symbols)))
    bit_symbols = [bin(i)[2:].zfill(no_of_bits) for i in range(number_of_symbols)]
    #print(bit_symbols)
    file_write = open("data_binary_lz.txt", "w+")
    dictionary = ''

    for chunk in iter(lambda: file_read.read(4), ''):
        symbol_no = int(chunk[1:2])
        dictionary = dictionary + chunk[:3]
        bit_symb = '1' + bit_symbols[symbol_no]
        file_write.write(bit_symb)
        if file_read.tell() >= w * 4:
            break

    file_read.close()
    file_write.close()
    return dictionary


def generateLZCoding(w, dictionary,number_of_symbols,sym_list):
    file_read = open(sym_list, "r")
    file_read.seek(w * 4)

    file_write = open("data_binary_lz.txt", "a")
    n_collections = {}
    bits_required=0
    no_of_bits = int(np.ceil(np.log2(number_of_symbols)))
    bit_symbols = [bin(i)[2:].zfill(no_of_bits) for i in range(number_of_symbols)]
    for chunk in iter(lambda: file_read.read(4), ''):
        sequence = chunk[:3]
        n, l = 0, -1
        prev_pos=file_read.tell()
        for chunk2 in iter(lambda: file_read.read(4), ''):
            p = dictionary.find(sequence) / 4
            if p < 0 :
                file_read.seek(prev_pos)
                break
            else:
                l, n = int(p), n + 1
            sequence = sequence + chunk2[:3]
            prev_pos=file_read.tell()

        #print("l - {0} || n - {1}  ||  sequence ".format(str(l), str(n)) + sequence[:-2])

        n_collections[n]=n_collections.get(n,0)+1
        if(n>1):
            n_bin, l_bin = bin(n)[2:], bin(l)[2:]
            l_bin = l_bin.zfill(2 * len(l_bin))
            n_bin = n_bin.zfill(2 * len(n_bin))
            bits_required+=len(n_bin)+len(l_bin)
            #print(n_bin,l_bin)
            file_write.write(l_bin + n_bin)
        else:
            file_write.write('1'+bit_symbols[int(chunk[1:2])])
            bits_required+=4
            
    file_read.close()
    file_write.close()
    print("Counts of sequences of various length for LZ coding")
    print(n_collections)
    return bits_required

#%%
if __name__=='__main__':
    with open('tpm.npy','rb') as f:
        tpm=np.load(f)
    total_no_of_symbols=np.int((os.path.getsize("symbol_list.txt")/3))
    w = 1000
    dictionary = generateDictionary(w, len(tpm),"symbol_list.txt")
    bits_required=generateLZCoding(w, dictionary,len(tpm),"symbol_list.txt")
    print(f"number of bits required for LZ coding is {bits_required+w*4}")

