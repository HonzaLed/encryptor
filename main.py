import random

def simple_encrypt(data,seed,width=1000):
    b=""
    random.seed(seed)
    for i in data:
        b=b+chr(ord(i)*random.randint(1,width))
    return b
def simple_decrypt(data,seed,width=1000):
    b=""
    random.seed(seed)
    for i in data:
        b=b+chr(ord(i)//random.randint(1,width))
    return b

def listToInt(data):
    cache = ""
    for i in data:
        cache=cache+str(i)
    try:
        return int(cache)
    except:
        return 0

def complex_encrypt(data, seed, modifier):
    b=""
    seeds, modifier = calculateSeeds(seed, modifier)
    
    newSeeds=[seeds[0]]
    for i in range(1,len(data)):
        newSeeds.append(seeds[i]*modifier[i]*ord(data[i-1]))

    index=0
    for i in data:
        b = b + simple_encrypt(i, newSeeds[index])
        index+=1
    return b

def complex_decrypt(data, seed, modifier):
    b=""
    seeds, modifier = calculateSeeds(seed, modifier)
    
    newSeeds=[seeds[0]]
    for i in range(1,len(data)):
        newSeeds.append(seeds[i]*modifier[i]*ord(simple_decrypt(data[i-1], newSeeds[i-1])))

    index=0
    for i in data:
        b = b + simple_decrypt(i, newSeeds[index])
        index+=1
    return b

def encrypt(data, seed=None, modifier=None):
    returnSeed, returnModifier = False,False
    if seed == None:
        returnSeed = True
        seed = random.randint(int("1"*(len(data)//3)), int("9"*(len(data)//3)))
    if modifier == None:
        returnModifier = True
        modifier = random.randint(int("1"*len(data)), int("9"*len(data)))
    cache = complex_encrypt(data, seed, modifier)

    if returnSeed and returnModifier:
        return cache, seed, modifier
    elif returnSeed:
        return cache, seed
    elif returnModifier:
        return cache, modifier
    else:
        return cache

decrypt=complex_decrypt

def calculateSeeds(seed,modifier):
    seeds = list(str(seed**10))
    while len(seeds)%3!=0:
        seeds.append(0)
    seeds = [seeds[i:i+3] for i in range(0,len(seeds),3)]
    seeds = [listToInt(i) for i in seeds]
    
    modifier = list(str(modifier**10))
    while len(modifier)%3!=0:
        modifier.append(0)
    modifier = [modifier[i:i+3] for i in range(0,len(modifier),3)]
    modifier = [listToInt(i) for i in modifier]
    return seeds,modifier
