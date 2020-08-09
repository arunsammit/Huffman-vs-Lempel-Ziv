import numpy as np
import os
#from sklearn.preprocessing import normalize
import Huffman as huff
import LZ
#%%
with open('tpm.npy','rb') as f:
    tpm=np.load(f)
number_of_symbols=tpm.shape[0]
trivial_size=np.int((os.path.getsize("symbol_list.txt")/3)*np.ceil(np.log2(number_of_symbols)))

#%%
print('-----LZ Coding----')
total_no_of_symbols=np.int((os.path.getsize("symbol_list.txt")/3))
w = int(input('Enter the value of w(length of dictionary for LZ coding) '))
print(f"dictionary size --> {w}")
dictionary = LZ.generateDictionary(w, number_of_symbols,"symbol_list.txt")
LZ.generateLZCoding(w, dictionary,number_of_symbols,"symbol_list.txt")
print()
LZ_size=(os.path.getsize("data_binary_lz.txt"))

print()
#%%
print('-----Huffman Coding-----')
all_codes={}
all_reverse_codes={}
huffman_forest={}
huff.generate_huffman_codes(all_codes,all_reverse_codes,huffman_forest,tpm)
#printing huffman codes consructed
'''
print("Huffman codes:")
for symbol,tree in huffman_forest.items():
    print(f"Codes when prev symbol is: {symbol}")
    tree.pr()
    print()
'''
huff.HuffmanCoding(all_codes,"symbol_list.txt")
Huffman_size=os.path.getsize("data_binary_hff.txt")
#%%
print(f'bits required for trivial encoding --> {trivial_size}')
print(f'bits required for LZ encoding --> {LZ_size}')
print(f'bits required for huffman encoding --> {Huffman_size}')

print()
print("compression ratio:")
print(f"LZ     : {(LZ_size/trivial_size)*100}")
print(f"Huffman: {(Huffman_size/trivial_size)*100}")
