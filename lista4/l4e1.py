import sys,os
print("importing miller_rabin and extended algorithm from lista1 and lista 3")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lista3.l3e2 import miller_rabin
from lista1.l1e2 import extend_euclids

N_VALUE=0
PUBLIC_KEY=1
PRIVATE_KEY=2

def input_prime():
    """Read the input of a prime number and validate it with miller_rabin
    to determine if number is compose
    """

    p = int(input("Input the prime value\n"))

    # 10 is a good value to miller_rabin, with probability of < 0.00001
    while(not miller_rabin(p,10)): 
        p = input("Number is not prime, digit other: ")

    return p

def input_pqe():
    """Make the read of values for calculate number n, and public key
        
        The n value is the multiplication of 2 primes
        The e value is the private key
        The d value is the public key
        return (n,e,d)
    """
    p,q = input_prime(),input_prime()
    rest,d,e = 0,0,0
    fi_n = (p-1)*(q-1) # Totient function of euclides
    while(rest != 1):
        e = int(input("enter with public key number"))
        # e = 1 mod (p-1 * q-1), d = e^-1 mod (p-1 * q-1)
        rest,d = extend_euclids(e,fi_n)
    print("keys (pri,pub): (%d,%d)" %(d,e))
    d %= fi_n # Transform in positive if d is negative
    return (p*q,e,d)

def cipher(data,values):
    output = []
    for x in data:
        # x^Pubkey mod n
        cipher_data = pow(ord(x), values[PUBLIC_KEY],values[N_VALUE])
        output.append(cipher_data)
    return output

def decipher(data,values):
    output = []
    for x in data:
        # x^PrivKey mod n
        decipher_data = pow(ord(x),values[PRIVATE_KEY],values[N_VALUE])
        output.append(decipher_data)
    return output

if __name__ == '__main__':
    values = input_pqe()
    name = input("name file with the data\n")
    data = open(name,"r").read()
    option = input("Select \ne - encrypt\nd - decrypt\n")
    if option == 'e':
        # write direct in the file the encryption
        output = cipher(data,values)
        print("encrypting and writte in %s.crsa" % name)
        with open(name+".crsa","w") as file_cipher:
            file_cipher.write("".join([chr(x) for x in output]))
    elif option == 'd':
        # write decifred text direct in file the decryption
        print("decrypting and writte in %s.drsa" % name)
        output = decipher(data,values)
        with open(name+".drsa","w") as file_decipher:
            file_decipher.write("".join([chr(x) for x in output]))
    else:
        print("Invalid option")
