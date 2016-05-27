import random
def miller_rabin(n,t):
    prime = True
    if n&1:
        k,q = determine_k_q(n)
 #       print(q)
  #      print(k)
        list_a = []
        if t>n-2:
            list_a = range(2,n)
        else:
            list_a = random.sample(range(2,n),t)
   #     print(list_a)
        count_t = 0
        while count_t < t and prime:
            a = list_a[count_t]
            prime = verify_a(a,n,k,q)
            count_t += 1
    else:
        prime = False
    return prime

def verify_a(a,n,k,q):
    prime = False
    x = pow(a,q,n)
    if x != 1 and x != n-1:
        j = 0
        while j<k and not prime:
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
    while not q&1:
        k,q = k+1, q>>1
    return k,q
if __name__ == "__main__":
    number = int(input("Number n"))
    interation = int(input("Number k"))
    if miller_rabin(number,interation):
        print("prime with probability %.6f to not be prime" % (1/4)**interation)
    else:
        print("compose")
