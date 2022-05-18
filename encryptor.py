import random
import base64

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
    seeds, modifier = bbranchedCalculateNumbers(seed)[1], bbranchedCalculateNumbers(modifier)[1]

    newSeeds=[seeds[0]]
    for i in range(1,len(data)):
        newSeeds.append(seeds[i]*modifier[i]*ord(data[i-2]))

    index=0
    for i in data:
        b = b + simple_encrypt(i, newSeeds[index])
        index+=1
    return b

def complex_decrypt(data, seed, modifier):
    b=""
    seeds, modifier = bbranchedCalculateNumbers(seed)[1], bbranchedCalculateNumbers(modifier)[1]

    newSeeds=[seeds[0]]
    for i in range(1,len(data)):
        newSeeds.append(seeds[i]*modifier[i]*ord(simple_decrypt(data[i-2], newSeeds[i-1])))

    index=0
    for i in data:
        b = b + simple_decrypt(i, newSeeds[index])
        index+=1
    return b

def encrypt(data, seed=None, modifier=None, debug=True):
    tries=0
    a=None
    returnSeed, returnModifier = False,False
    if seed == None:
        #print("seed")
        returnSeed = True
    if modifier == None:
        #print("mod")
        returnModifier = True
    while a==None:
        try:
            if returnSeed:
                #print("seed gen")
                seed = random.randint(int("1"*round(len(data)//1.5)), int("9"*round(len(data)//1.5)))
            if returnModifier:
                #print("mod gen")
                modifier = random.randint(int("1"*round(len(data)//1.5)), int("9"*round(len(data)//1.5)))
            cache = complex_encrypt(data, seed, modifier)
            a=",#)&)"
        except BaseException as err:
            tries+=1
            if debug:
                print("[WARNING] Error while trying to encrypt data! This is try",str(tries)+", trying again!")
            print(seed, modifier)
            if tries>25:
                raise Exception("[ERROR] Error while encrypting", err)
                break
    if returnSeed and returnModifier:
        return cache, seed, modifier
    elif returnSeed:
        return cache, seed
    elif returnModifier:
        return cache, modifier
    else:
        return cache

decrypt=complex_decrypt

def bbranchedCalculateNumbers(number):
    return branchedCalculateNumbers(branchedCalculateNumbers([number])[1])

def branchedCalculateNumbers(numbers):
    result = []
    result2 = []
    for i in numbers:
        a = []
        for j in calculateNumber(i):
            a+=calculateNumber(j)
        result.append(a)
        result2 += a
    return result, result2

def calculateNumber(number):
    numbers = list(str(number**10))
    while len(numbers)%3!=0:
        numbers.append(0)
    numbers = [numbers[i:i+3] for i in range(0,len(numbers),3)]
    numbers = [listToInt(i) for i in numbers]
    return numbers

def calculateSeeds(seed,modifier):
    seeds = calculateNumber(seed)
    modifier = calculateNumber(modifier)
    return seeds,modifier
