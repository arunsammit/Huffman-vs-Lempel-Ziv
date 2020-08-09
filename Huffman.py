import numpy as np
from functools import total_ordering
from queue import Queue
#tpm = np.array([[.5, .25, .20, .04, .01], [.8, 0.05, .1, .04, .01 ], [.65, .09, 0.11, .14, .01],[.75, .05, .05, .14, .01],[.7,.1,.04,.06,.1]])

import heapq
@total_ordering
class myNode:
    '''
    It is a class for node of the priority queue.
    '''
    def __init__(self,symbol,prob):
        self.symbol=symbol
        self.prob=prob
        self.left=None
        self.right=None
    def __lt__(self,other):
        return self.prob<other.prob
    def __eq__(self,other):
        return (self.prob==other.prob) and (self.symbol==other.symbol)
    def pr(self):
        q=Queue(0)
        q.put((self,''))
        while not(q.empty()):
            curr_node,curr_str=q.get()
            if curr_node.symbol is not None:
                print(f"{curr_node.symbol}: {curr_node.prob} -->  {curr_str}")
            if curr_node.left is not None:
                q.put((curr_node.left,curr_str+'0'))
            if curr_node.right is not None:
                q.put((curr_node.right,curr_str+'1'))
        
#%%
def _make_initial_heap(p_row):
    number_of_symbols=p_row.shape[0]
    symbol_list = ['a' + str(i).zfill(2) for i in range(number_of_symbols)]
    d=list(zip(symbol_list,p_row))
    heap=[]
    for sym,prob in d:
        curr_myNode=myNode(sym,prob)
        heapq.heappush(heap,curr_myNode)
    return heap
    
def _make_huffman_tree(heap):
    while(len(heap)>1):
        n1=heapq.heappop(heap)
        n2=heapq.heappop(heap)
        merged=myNode(None,n1.prob+n2.prob)
        merged.left=n1
        merged.right=n2
        heapq.heappush(heap,merged)
    return heap[0]
def _get_huff_codes(root,codes,reverse_codes,current=''):
    '''
    Get Huffman's coding(variable length codes) for each symbol
    given the huffman tree root node --> root and saves the codes
    in codes dictionary and reverse_codes in reverse_codes dictionary
    
    '''
    if root is not None:
        if root.symbol is not None:
            codes[root.symbol]=current
            reverse_codes[current]=root.symbol
            return
        _get_huff_codes(root.left,codes,reverse_codes,current+'0')
        _get_huff_codes(root.right,codes,reverse_codes,current+'1')
    return
    
#%%

def generate_huffman_codes(all_codes,all_reverse_codes,huffman_forest,tpm):
    '''
    builds variable length codewords according to huffman coding 
    algorithm given the tpm
    
    '''
    for i in range(tpm.shape[0]):
        init_heap=_make_initial_heap(tpm[i])
        curr_huff_tree=_make_huffman_tree(init_heap)
        huffman_forest['a'+str(i).zfill(2)]=curr_huff_tree
        codes={}
        reverse_codes={}
        _get_huff_codes(curr_huff_tree,codes,reverse_codes)
        all_codes['a'+str(i).zfill(2)]=codes
        all_reverse_codes['a'+str(i).zfill(2)]=reverse_codes
    return
def HuffmanCoding(all_codes,sym_list):
    '''
    Encodes the file symbol_list.txt using huffman encoding algorithm
    and saves the encoded file as data_binary_hff.txt
    
    '''
    number_of_symbols = len(all_codes)
    file_read = open(sym_list, "r")
    file_write = open("data_binary_hff.txt", "w")
    chunk=file_read.read(4)
    prev_symbol = chunk[:3]
    no_of_bits = int(np.ceil(np.log2(number_of_symbols)))
    symbols_trivial = [bin(i)[2:].zfill(no_of_bits) for i in range(number_of_symbols)]
    file_write.write(symbols_trivial[int(chunk[1:])])
    for chunk in iter(lambda: file_read.read(4), ''):
        curr_symbol = chunk[:3]
        file_write.write(all_codes[prev_symbol][curr_symbol])
        prev_symbol = curr_symbol
    file_write.close()
    file_read.close()

#%%
if __name__=='__main__':
    with open('tpm.npy','rb') as f:
        tpm=np.load(f)
    number_of_symbols=tpm.shape[0]
    all_codes={}
    all_reverse_codes={}
    huffman_forest={}
    generate_huffman_codes(all_codes,all_reverse_codes,huffman_forest,tpm)
    #printing huffman codes consructed
    print("Huffman codes:")
    for symbol,tree in huffman_forest.items():
        print(f"Codes when prev symbol is: {symbol}")
        tree.pr()
        print()
    HuffmanCoding(all_codes,"symbol_list.txt")
     

 
    
        
        
    
    
