import hashlib
import math
import numpy as np
import random
import matplotlib.pyplot as plt

def get_hash(mode, value, a, b, out_bits): 
    if (mode == "md5"):
        return int(hashlib.md5(np.uint64(value)).hexdigest(), 16) % 2**out_bits
    if (mode == "linear"):
        return ((a * value + b) % 2**out_bits)
    if (mode == "squared"):
        return ((((value+a) **2) + b*value + value%2) % 2**out_bits)

def hash_attack(x, hash_type, in_bits, out_bits, mode):
    num_trials = 0
    collision_no = []
    a = 10001759
    b = 9004901
    while (num_trials < x):
        num_at_collision=0
        hash_list=[]
        orig_num = random.getrandbits(in_bits)
        rand_hash = get_hash(hash_type, orig_num, a, b, out_bits)
        prev_hash = rand_hash
        multiple = 2
        value = orig_num
        while (rand_hash not in hash_list):
            hash_list.append(rand_hash)
            if (mode == "multiple"):
                value = orig_num * multiple
                if (value > 2**64):
                    orig_num = random.getrandbits(64)
                    value = orig_num
                    multiple = 1
            elif (mode == "square"):
                value = prev_hash**2
            elif (mode == "evens"):
                value = random.getrandbits(in_bits)
                value = value + value % 2
            else:
                value = random.getrandbits(in_bits)
            rand_hash = get_hash(hash_type, value, a, b, out_bits)
            prev_hash = rand_hash
            multiple *= 2
            num_at_collision = num_at_collision + 1
        num_trials+=1
        collision_no.append(num_at_collision)
        print(str(num_trials) +":" + str(num_at_collision))
        #print (str(rand_hash) + " is in " + str (hash_list))
    colls = np.zeros(100)
    coll_range = np.linspace(0,15000,100)
    for i in range(100):
        for z in collision_no:
            if (z < (coll_range[i])):
                colls[i] += 1
    colls = colls/x
    return colls

md5_colls = hash_attack(1000, "md5", 64, 24, "multiple")
lin_colls = hash_attack(1000, "linear", 64, 24, "multiple")
sq_colls = hash_attack(1000, "squared", 64, 24, "multiple")
x = np.linspace(0,15000,100) 
y = 1-np.exp(-1*x**2/2**25) #Random oracle model
plt.plot(x,y, 'b', alpha=0.5, label = 'Random Oracle') 
plt.plot(x,md5_colls, 'r', alpha=0.7, label = 'MD5')
plt.plot(x,lin_colls, 'k', alpha=0.7, label = 'Linear')
plt.plot(x,sq_colls, 'g', alpha=0.7, label = 'Quadratic')
plt.xlabel('Number of Hashes')
plt.ylabel('Probability of Collision')
plt.title('Repeated Multiplication by 2 Attack')
plt.legend()
plt.show()