# Reference article: http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm

import l1e1_t as SubTables


def main():
    try:
        file = open("password.txt","r")
        password = file.read()
        file.close()
        input_name = input("Name of file with data\n")
        action = input("e - encription\nd - decription\n")
        
        file = open(input_name,"r") 
        data = file.read()
        file.close()
        output_name = ""
        action_range=[]
        if (action == 'e'):
            output_name = input_name.split(".")[0]+".des"
            action_range = range(0,16,1)
            data = data_to_bit(data) # Transform the data in bits
        elif (action == 'd'):
            output_name = input_name.split(".")[0]+".txt"
            action_range = range(15,-1,-1)
            data = [int(bit) for bit in data]
        else:
            raise NameError("Action invalid")

        data_result = des(data,password,action_range) 
        data_string = bit_to_string(data_result)
        final_data = data_string
        if( action == 'd'):
            array_chars = [chr(int(data_string[i:i+8],2)) for i in range(0,len(data_string),8)]
            final_data = ''.join(array_chars)
        file = open(output_name,"w") 
        file.write(final_data)
        file.close()
    except NameError as invalid_action:
        print("Invalid action")
    except FileNotFoundError as invalid_file:
        print(invalid_file)

def des(data,password,action_range):
    keys = generate_keys(password) # All keys of 16 rounds
    data_result = []
    # To each block of data with 64 bits, make the algorith
    for block in range(0,len(data),64):
        data_result.extend(encript(data[block:block+64],keys,action_range))
    return data_result

def encript(data,keys,action_range):
    data_first = permute(SubTables.IP,data) # Initial permutation
    left = data_first[0:32]
    right = data_first[32:64]
    for i in action_range:
        temp = left
        left = right
        # Make the expansion for right data appling function f
        expansed_data = expansion_right(right,keys[i])
        # Make the substitutions in SBox
        function_f = substitution_box(expansed_data)
        right = [bit[0]^bit[1] for bit in zip(temp,function_f)]
 #       print(left+right)
    data_result = permute(SubTables.IIP,right+left)
    return data_result

def substitution_box(expansed_data):
    final_data = []
    for block_bits in range(0,48,6):
        bits = expansed_data[block_bits:block_bits+6] # Block with 6 bits
        box_index = int(block_bits/6)
        # 16 is the number of elements of row in SBox
        row_index = ((bits[0]<<1)+bits[5])*16
        col_index = (bits[1]<<3)+(bits[2]<<2)+(bits[3]<<1)+(bits[4])
        # Obtain the number of box 0..7
        number_box = SubTables.SBox[box_index][row_index+col_index]
        # Transform the number in bits
        number_bits = []
        for i in range(3,-1,-1):
            number_bits.append( (number_box>>i)&1 )
        final_data.extend(number_bits)
    # Make the final substitution in SBox
    data_substitution = permute(SubTables.P,final_data)
    return data_substitution

def expansion_right(right,key_round):
    right_data = permute(SubTables.ET, right)
    function_data = [bit[0]^bit[1] for bit in zip(right_data,key_round)]
    return function_data


def generate_keys(key):
    # Transform password in array of bits
    k = data_to_bit(key)
    key_permuted = permute(SubTables.PC1,k) # First substitution tables
    keys = []
    left_key = key_permuted[0:28]
    right_key = key_permuted[28:56]
    new_key = []
 #   print(left_key)
    ## Create the 16 keys to each round
    for key_round in range(0,16):
        # Make the number of shifts determined
        for i in range(SubTables.left_shifts[key_round]):
            left_key.append(left_key[0])
            right_key.append(right_key[0])
            left_key.pop(0)
            right_key.pop(0)
        new_key.append(left_key+right_key)
        # Permute the key generate by shift left with PC2
        new_key[key_round] = permute(SubTables.PC2,new_key[key_round])
    return new_key

def permute(table_permutation, data):
   data_permuted = []
   for i in table_permutation:
       data_permuted.append(data[i-1]) 
   return data_permuted

def data_to_bit(data):
    data_int = [ ord(x) for x in data]
    data_bit = []
    # Tranform data in bits
    for char in data_int:
        for bit in range(7,-1,-1):
            data_bit.append( (char>>bit)&1 )

    # Fill data with bit 0
    size = len(data_bit)%64
    for bits in range(64-size):
        data_bit.append(0)
            
    return data_bit
def bit_to_string(data):
    data_string = ''.join([str(x) for x in data])
    return data_string

if __name__ == "__main__":
    main()

