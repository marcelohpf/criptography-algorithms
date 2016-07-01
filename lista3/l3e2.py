import random
def miller_rabin(n,t):
    prime = True
    # Verify odd
    if n&1:
        k,q = determine_k_q(n)
        # Make the verifications
        count_t = 0
        while count_t < t and prime:
            a = random.randrange(2,n-1)
            prime = verify_a(a,n,k,q)
            count_t += 1
    else:
        prime = False
    return prime

def verify_a(a,n,k,q):
    prime = False
    x = pow(a,q,n) # (a^q) mod n
    if x != 1 and x != n-1:
        j = 0
        while j<k and not prime: # (a^(q*2^j)) mod n
            x = pow(x,2,n)
            if x != n-1:
                j+=1
            else:
                prime = True
    else:
        prime = True
    return prime

def determine_k_q(n):
    k = 0
    q = n-1
    while not q&1: # find the multiple in base 2, since 2^q+k = n-1
        k,q = k+1, q>>1
    return k,q

if __name__ == "__main__":
    number = int(input("Enter number to determine primality (n): "))
    interation = int(input("Enter the number of times to execute test (k): "))
    if miller_rabin(number,interation):
        print("prime with probability %.6f to not be prime" % (1/4)**interation)
    else:
        print("compose")
