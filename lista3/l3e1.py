
def stream_generator(S,amount_bits):
    bits = []
    i,j=0,0
    for bit_count in range(amount_bits):
# operation &255 is equivalent to %256
        i = (i+1)&255
        j = (j+ S[i])&255
        
        S[i],S[j] = S[j],S[i] # swap
        t = (S[i]+S[j])&255
        bits.append( S[t] )
    return bits
    
def initialize_S(seed):
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
    seed =  "uma semente para a geração de um array com 256 posições"
    S = initialize_S([ord(x) for x in seed])
    bits_random = stream_generator(S,int(amount_bits))
    file = open("random","w")
    print("Escrevendo dados gerados aleatoriamente no arquivo random")
    [file.write( bin(number|256)[3:] ) for number in bits_random]
    file.close()
