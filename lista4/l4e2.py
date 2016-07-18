import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Import extend euclids from lista 1")
from lista1.l1e2 import extend_euclids

POINT_O = (0,0)
def validate_input(a,b,p):
    """ Verify if a and b satisfy the equation
        4a^3 + 27b^2 ( mod p ) != 0
        true if satisfy
        false if not
    """   
    first_term = 4*(a**3) % p
    second_term = 27*(b**2) % p
    result = ( first_term + second_term ) % p

    return result != 0

def find_all_points(a,b,p):
    """A brute force to find all points in eclipse curve cryptografy
       over prime Zp: y^2 = x^3 + Ax + b
       iterate in every possible point x and find the relative y
    """
    value_xy=[] # contains values of y when positive, where (x,y) £ E(p)
    x = 0
    while x< p:
        y2 = (((x**3) %p) + ((a*x) %p) + b )%p
        y = 0
        while y < p and y !=-1 :
            if( (y**2)%p == y2):
 #               print("(%d,%d) (%d,%d)"% (x,y,x,(-y)%p))
                if y != (-y)%p:
                    value_xy.append((x,y))
                    value_xy.append((x,(-y)%p))
                else:
                    value_xy.append((x,y))
                y = -2
            y+=1
        x+=1
    return value_xy

def multiplication(k,pointP,a,p):
    result = POINT_O
    point = pointP
    for bit in range(k.bit_length()):
        if (k>>bit)&1:
 #           print(bit)
            result = point_sum(result,point,a,p)
        point = double_point(point,a,p)
    return result

def double_point(pointP,a,p):
    return point_sum(pointP,pointP,a,p)

def point_sum(pointP,pointQ,a,p):
    """Make the sum of a value like P+Q, for a point P=(Xp,Yp) and Q=(Xq,Yq)
        if Q==P
        lambda = (3 * Xp^2 +a)
                 -----------  mod p -> (dividend * inverse_multi(divider)) mod p
                 (    2*Yp   )
        else
        lambda = (Yq-Yp)
                 ---- mod p -> (divend * inverse_multi(divider)) mod p
                 (Xq-Xp)

       Xr = (lambda^2 - Xp -Xp) mod p
       Yr = (lambda*(Xp-Xr) -Yp) mod p
    """
    Xp,Yp = pointP
    Xq,Yq = pointQ
    pointR = None
    if pointP == POINT_O:
        pointR = pointQ
    elif pointQ == POINT_O:
        pointR = pointP
    elif Xp == Xq and (Yp == (-Yq)%p): # The P-P=O
        pointR = POINT_O
    else: 
        lambda_value = 0
        if pointP == pointQ:
            dividend = (3*(Xp**2)+a)%p
            divider = (2*Yp)%p
            lambda_value = (dividend*extend_euclids(divider,p)[1])%p
        else:
            dividend = (Yq-Yp)%p
            divider = (Xq-Xp)%p
            lambda_value = (dividend*extend_euclids(divider,p)[1])%p
        x_sum = ((lambda_value**2) - Xp - Xq)%p
        y_sum = (lambda_value*(Xp-x_sum) - Yp)%p
        pointR=(x_sum,y_sum)
    return pointR

def define_order(point,a,p):
    """ Define order based in definition of O point witch is  of P-P=O
        so, order = n, where n is the number of sums nP = P+P+...+P into 
        P-P=O
    """
    order = 1
    x,y = point
    while point != POINT_O:
        point = point_sum(point,(x,y),a,p)
 #       print(point,order)
        order+=1
    return order

def input_abp():
    a = int(input("A value\n"))
    b = int(input("B value\n"))
    p = int(input("P value\n"))
    while not validate_input(a,b,p): 
        print("invalid A and B") 
        a = int(input("A value\n"))
        b = int(input("B value\n"))
        p = int(input("P value\n"))
    return (a,b,p)

if __name__ == "__main__":
    
    a,b,p = input_abp()
    print("The inputs are valid ok")

    points = find_all_points(a,b,p)
    orders = [ define_order(point,a,p) for point in points]
    order_points = [ value for value in zip(orders,points)]
    order_points.sort()
    print("order, (X,Y)")
    for point in order_points:
        print(point)
    print("Point sugest: {}".format(order_points[-1]))
    print("Count of poins%d"%(len(points)))
        
