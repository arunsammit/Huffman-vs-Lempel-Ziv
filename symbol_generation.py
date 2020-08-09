import numpy as np
import sys
#from sklearn.preprocessing import normalize


def checkErgodic(tpm):
    '''
    

    Parameters
    ----------
    tpm : it is n*n dimensional numpy matrix containing transition probability matrix.

    Returns
    -------
    TYPE: it return a boolean value true if the given transition probability matrix is ergodic and otherwise false

    '''
    tpm = np.array(tpm)
    if len(tpm) != len(tpm[0]):
        print("Not Square Matrix")
        return False
    for i in range(len(tpm)):
        if tpm[i][i] == 1.0:
            print("p_ii is found to be 1")
            return False
    return np.any(np.sum(tpm, axis=0) != 0)



def generateSymbols(tpm,total_no_of_symbols,sym_list):
    '''
    

    Parameters
    ----------
    tpm : it is a n*n dimensional numpy array
    total_no_of_symbols : it is an integer denoting the number of symbols that we want to generate
    sym_list : it is a string type variable denoting the name of file in which we want to save the generated output.

    Returns
    The function doesn't return anything

    '''
    if not checkErgodic(tpm):
        print("Not Ergodic")
        return False
    number_of_symbols = len(tpm)
    symbol_list = ['a' + str(i).zfill(2) for i in range(number_of_symbols)]
    file = open(sym_list, 'w+')

    
    current_symbol = symbol_list[0]

    for i in range(total_no_of_symbols):
        file.write(current_symbol + " ")
        symbol_no = int(current_symbol[1:])
        current_symbol=np.random.choice(
          symbol_list, 
          p=tpm[symbol_no]
        )
        sys.stdout.write("\r Completing %f%%" % (float(i + 1) * 100 / float(total_no_of_symbols)))
        sys.stdout.flush()

    file.close()
    return 
tpm = np.random.uniform(low=0,high=100,size=(33,33))
tpm = tpm/tpm.sum(axis=1,keepdims=True)
#tpm = np.array([[.4, .11, .15, .04, .3], [ 0.05, .38,.33, .04, .2 ], [.55, .09, 0.11, .14, .11],[.35, .05, .05, .44, .11],[.2,.04,.06,.5,.2]])
tpm_size=tpm.shape[0]
with open('tpm.npy','wb') as f:
    np.save(f,tpm)

total_no_of_symbols=1000000
number_of_symbols=tpm.shape[0]
print("TPM")
print(tpm)

print()
#%%
generateSymbols(tpm,total_no_of_symbols,'symbol_list.txt')

