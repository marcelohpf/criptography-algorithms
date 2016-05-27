seed = "uma semente para a geração de um array com 256 posições"

def stream_generator(S,amount_bits):
    # operation &255 is equivalent to %256
    bits = []
    i,j=0,0
    for bit_count in range(amount_bits):
        i = (i+1)&255
        j = (j+ S[i])&255
        
        S[i],S[j] = S[j],S[i] # swap
        t = (S[i]+S[j])&255
        bits.append( S[t] )
    return bits
def initialize_S(seed):
    from datetime import datetime
    seed_len = len(seed)
    # Initialize
    S = [ x for x in range(256)]
    T = [ seed[x%seed_len] for x in range(256)]
    
    # Permute
    j=0
    for i in range(256):
        j = ( j + S[i]+ T[i]) &255
        S[i],S[j] = S[j],S[i]

    return S
if __name__ == "__main__":
    amount_bits = input("number of numbers to generate\n")
    S = initialize_S([ord(x) for x in seed])
    bits_random = stream_generator(S,int(amount_bits))
    file = open("random","w")
    [file.write( bin(number|256)[3:] ) for number in bits_random]
    file.close()
