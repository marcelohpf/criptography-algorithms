# Multiplication in GF(2^8)
def multiGF(a,b):
    d = [a,0,0,0,0,0,0,0]
    for f in range(1,8):
        d[f]= d[f-1]<<1
        # Verify the eight bit is active to apply the mod.
        if(d[f-1]&128):
            d[f]=d[f]^27
        d[f]= d[f]&255
        
    e = 0 # Accumulator off sum after multiplicate each value of polimomium
    f=1 # The verifier to see the values to sum
    for i in d:
        if(b&f):
            e = somaGF(i,e)
        f=f<<1
    return e

# Division in GF(2^8)
def division(a,b):
    r = multiGF(a,inverseMulti(b))
    return r

# Calculate the inverse multiplicative
def inverseMulti(a):
    result = a
    for i in range(1,7):
        result = multiGF(multiGF(result,result),a)
    result = multiGF(result,result)
    return result

# Perform the sum and subtraction in GF(2^8)
def somaGF(a,b):
    c = a^b
    return c


if __name__ == "__main__":
    try:

        a = int(input("A:\n"))
        operation = input("operator(+/-*)")
        b = int(input("B:\n"))
        
        if (operation == "+" or operation == "-"):
            print("A %s B = %d" %(operation,somaGF(a,b)))
        elif (operation == "*"):
            print("A * B = %d" % multiGF(a,b))
        elif (operation == "/"):
            print("A/B = %d" % division(a,b))
        else:
            print("operator invalid")
    except ValueError as error:
        print("polinomium invalid")
