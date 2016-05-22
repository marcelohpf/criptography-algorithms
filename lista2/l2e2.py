from l2e1 import aes,transform_text_int


start_seed = "ascderwoskdjredo"

def counter_mode(text,seed):
    data = []
    for block in range(0,len(text),16):
        data_encription = aes("aaaaeeeewwwwerti",seed,"e")
        seed = add_seed(seed)
        text_slice = text[block:block+16]
        data.extend([x[0]^ord(x[1]) for x in zip(data_encription,text_slice)])
    return data

def add_seed(seed):
    temporary_seed = [ord(x) for x in seed] 
    temporary_seed[-1]+=1
    for i in range(14,-1,-1):
        temporary_seed[i]+=(temporary_seed[i+1]&256)>>8
    new_seed = ''.join([ chr(seed&255) for seed in temporary_seed])
    return new_seed

def output_feedback_mode(text,seed):
    data = []
    for block in range(0,len(text),16):
        encription = aes("aaaaeeeewwwwerti",seed,"e")
        seed = ''.join([chr(x) for x in encription])
        text_slice = text[block:block+16]
        data.extend([x[0]^ord(x[1]) for x in zip(encription,text_slice)])
    return data
if __name__ == "__main__":
    encrypt = counter_mode("Uma mensagem de teste para criptografar",start_seed)
    print(''.join([chr(x) for x in encrypt]))
    decript = counter_mode(''.join([chr(x) for x in encrypt]),start_seed)
    print(''.join([chr(x) for x in decript]))
    
    
    encrypt = output_feedback_mode("Uma mensagem de teste para criptografar",start_seed)
    print(''.join([chr(x) for x in encrypt]))
    decript = output_feedback_mode(''.join([chr(x) for x in encrypt]),start_seed)
    print(''.join([chr(x) for x in decript]))

