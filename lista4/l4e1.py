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

if __name__ == '__main__':
    values = input_pqe()
    name = input("name file with the data")
    data = open(name,"r").read()

    # write direct in the file the encryption
    print("encrypting and writte in %s.crsa" % name)
    output = [pow(ord(x),values[PUBLIC_KEY],values[N_VALUE]) for x in data]
    open(name+".crsa","w").write("".join([chr(x) for x in output]))

    # write decifred text direct in file the decryption
    print("decrypting and writte in %s.drsa" % name)
    output = [pow(x,values[PRIVATE_KEY],values[N_VALUE]) for x in output]
    open(name+".drsa","w").write("".join([chr(x) for x in output]))
