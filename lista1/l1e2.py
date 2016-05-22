# Extend algorithm of euclids interative
def euclids(a,b):

    r = [a,b] 
    s = [1,0] # alpha value
    t = [0,1] # beta value
    
    while(r[0]%r[1] != 0):
        rt = r[0]%r[1] 
        q = int(r[0]/r[1])
        
        st =  s[0] - s[1]*q # calculate the new value of alpha
        tt = t[0] - t[1]*q # calculate the new value of beta
        
        r[0]=r[1]
        r[1]=rt
        s[0]=s[1]
        s[1]=st # update the value of alpha
        t[0]=t[1]
        t[1]=tt # update the value of beta
    
    if(r[1] == 1):
        print("alpha: %d beta: %d" % ( s[1],t[1]))
    else:
        print("a,b are not relative prime")



if __name__ == "__main__":
    try:
        a = int(input("Enter with value a"\n))
        b  = int(input("Enter with value b\n"))
        euclids(a,b)
    except ValueError as e:
        print("Invalid value")
