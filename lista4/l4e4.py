import os,sys
import random
#print("importing sha1 lib and json lib")
from hashlib import sha1
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("importing l4e4 with functions to process ecc")
from lista4.l4e2 import *
from lista1.l1e2 import extend_euclids

PRIVATE_KEY=0
PUBLIC_KEY=1
R=0
S=1

INV_MULT=1

def key_generation(n,pointG,a,p):
    """Create a pair of key for (private key, public key)
        private key (PK) in range (1 .. order -1)
        public key is the point PK*G
    """
    private_key = random.randint(1,n-1) # 0x6FAB034934E4C0FC9AE67F5B5659A9D7D1FEFD187EE09FD4  
    public_key = multiplication(private_key,pointG,a,p)
    return (private_key,public_key)

def digital_signature(message,n,pointG,a,p,keys):
    """Implement the algorith of ECDSA
        the pair (r,s) is the signature
    """
    r,s = 0,0
    while r == 0 or s == 0:
        k = random.randint(1,n-1) # 0x37D7CA00D2C7B0E5E412AC03BD44BA837FDD5B28CD3B0021
        x,y = multiplication(k,pointG,a,p)
        r = x % n
        t = extend_euclids(k,n)[INV_MULT]%n
        assert (1 == (k*t)%n )
        
        # Use sha1 to generate the hash value and convert the string hex to int
        hash_message = int(sha1(message.encode('ascii')).hexdigest(),16)
        s = (t*(hash_message +keys[PRIVATE_KEY]*r))%n
        #print(s)
    return (r,s)

def digital_verification(signature,message,n,pointG,a,p,keys):
    """Give a message and a signature pair (r,s) make the verification
           of signature.
    """
    hash_message = int(sha1(message.encode("ascii")).hexdigest(),16)
    inverse_s= extend_euclids(signature[S],n)[INV_MULT]%n

    assert (1 == (inverse_s * signature[S]) %n)
    
    u1,u2 = (hash_message*inverse_s)%n, (signature[R]*inverse_s)%n
    # X = u1*G + u2*Q, where Q is the public key
    pointX = point_sum(
                    multiplication(u1,pointG,a,p),
                    multiplication(u2,keys[PUBLIC_KEY],a,p),
                    a,p)
 
    is_valid = False
    # 0< s,r < n-1 and X != O
    if (pointX != POINT_O and 
            (0 < signature[S] < n-1 or 0 < signature[R] < n-1)):
        verification = pointX[0] %n
        is_valid = (verification == signature[R])

    return is_valid

def signature(file_name,n,pointG,a,p):
    keys = key_generation(n,pointG,a,p)
    print("Pair of keys: ",keys)
    print('*'*80)
    with open(file_name,"r") as file_message:
        message = file_message.read()
    
    signature = digital_signature(message,n,pointG,a,p,keys)
    with open(file_name+".sig","w") as file_signature:
        output = json.dumps({'keys': keys[PUBLIC_KEY],
                            'signature':signature})
        file_signature.write(output)

def verification(file_name,n,pointG,a,p):
    with open(file_name+".sig","r") as file_signature:
        input_data = json.loads(file_signature.read())
        signature = input_data['signature']
        keys = (0,input_data['keys'])
    with open(file_name,"r") as file_message:
        message = file_message.read()
    valid = digital_verification(signature,message,n,pointG,a,p,keys)
    assert valid

if __name__ == '__main__':
    # NIST Curve P-192:
    a = -3
    b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
    p = 6277101735386680763835789423207666416083908700390324961279
    pointG = (0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012,
                0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811)

    n = 0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22831 # define_order(pointG,a,p)
    print("Global parameters used:")
    print("Elipse curve: a = %d,b = %d"%(a,b))
    print("Prime p = %d"%p)
    print("Point base for ecc ",pointG)
    print("Order off point base G: %d"%n)
 
    option = input("Enter \na - assign\nv - vefiry\n")
    file_name = input("Enter with file name with message\n")
    if option == "a":
        signature(file_name,n,pointG,a,p)
    elif option == 'v':
        verification(file_name,n,pointG,a,p)
    else:
        print("Invalid option")
