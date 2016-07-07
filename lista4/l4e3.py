import os,sys
print("import l4e2 for processing points operations in ecc")
sys.path.append(os.path.abspath(__file__))
from l4e2 import *
import random

def validate_points(point,points):
    valid_point = point in points 
    format_point = isinstance(point,tuple)
    return valid_point and format_point
def input_point():
    point = eval(input("Input point, the format should be: (Px,Py)"))
    points = find_all_points(a,b,p)
    while not validate_points(point,points):
        print("invalid point")
        point = eval(input("Input point, the format should be: (Px,Py)"))
    return point

def cipher(pointG,pointP,public_key,a,p):
    """Cipher a point P, based in pointG
       C = { k*G, P+k*PKb }
    """
    k = random.randint(1,order-1)#386
    print("generate random k = %d"%k)
    first_point = multiplication(k,pointG,a,p)
    second_point = point_sum(
                    pointP,
                    multiplication(k,public_key,a,p),
                    a,p)
    return (first_point,second_point)

def decipher(pointsC,private_key,a,p):
    first_point = multiplication(private_key,pointsC[0],a,p)
    plain = point_sum(pointsC[1],(first_point[0],(-first_point[1])%p),a,p)
    return plain

if __name__ == '__main__':
    a,b,p = input_abp() #-1,188,751
    print('#'*20+"\npoint base G")
    pointG = input_point() #0,376
    print("#"*20+"point P")
    pointP = input_point() #562,201
    order = define_order(pointG,a,p)
    private_key = int(input("Input private key b")) # 58
    public_key_b = multiplication(private_key,pointG,a,p)# (201,5)
    pointsC = cipher(pointG,pointP,public_key_b,a,p)
    print(pointsC)
    pointP = decipher(pointsC,58,a,p)
    print(pointP)
