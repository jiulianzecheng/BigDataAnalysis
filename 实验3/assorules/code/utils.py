from collections import defaultdict


def read_baskets(file_baskets):
    baskets = []
    with open(file_baskets, 'r') as f_baskets:
        for line in f_baskets:
            line=line.strip().replace('\'','').replace('[','').replace(']','')
            words = line.split(',')
            basket=[]
            for word in words:
                basket.append(word.strip())
            basket=set(basket)
            baskets.append(basket)
    return baskets
def write_freq_sets(frequent_sets,support_degrees,file_frequent_sets):
    with open(file_frequent_sets,'a') as f_fre_sets1:
        for i in range(len(frequent_sets)):
            f_fre_sets1.write("{}:{}\n".format(frequent_sets[i],support_degrees[i]))

def cadidate(freq_sets1,freq_sets2):
    cadidate_sets=[]
    temp=set()
    for elem1 in freq_sets1:
        for elem2 in freq_sets2:
            if not (elem1 <= elem2):
                elem3=elem1|elem2
                elem3=frozenset(elem3)
                temp.add(elem3)
    # temp=set(temp)
    # temp=list(temp)
    for elem in temp:
        cadidate_sets.append(set(elem))
    return cadidate_sets
def read_freq_sets(file_sets):
    sets = []
    with open(file_sets, 'r') as f_sets:
        for line in f_sets:
            line=line.strip()
            line=line.replace('{','').replace('}','').replace('\'','').replace('\"','')
            elem_set,num = line.split(':')
            words = elem_set.split(',')
            result=[]
            for word in words:
                result.append(word.strip())
            sets.append(set(result))
    return sets
def read_sets(file_sets):
    sets = []
    with open(file_sets, 'r') as f_sets:
        for line in f_sets:
            line=line.strip()
            line=line.replace('{','').replace('}','').replace('\'','').replace('\"','')
            words= line.split(',')
            result=[]
            for word in words:
                result.append(word.strip())
            sets.append(set(result))
    return sets

def get_baskets(file_read,file_write):
    file_w=open(file_write,'a')
    with open(file_read) as file_r:
        for line in file_r:
            line=line.strip().replace('\'','').replace('[','').replace(']','').replace('\"','')
            title,reference=line.split(':')
            words=reference.split(',')
            # words=line.split(',')
            result=[]
            for word in words:
                result.append(word.strip())
            file_w.write("{}\n".format(result))
    file_w.close()

def get_sets(file_read,file_write):
    file_w=open(file_write,'a')
    with open(file_read) as file_r:
        for line in file_r:
            line=line.strip().replace('\'','').replace('[','').replace(']','')
            key,value=line.split(',')
            file_w.write("{}\n".format(key))
    file_w.close()

def hash(set,bucket_num):
    hash_value=0
    for word in set:
        for char in word:
            hash_value += ord(char)
    hash_value=hash_value%bucket_num
    return hash_value
def get_supports(file_freq_sets):
    supports = defaultdict(float)
    with open(file_freq_sets, 'r') as f_sets:
        for line in f_sets:
            line = line.strip()
            line = line.replace('{', '').replace('}', '').replace('\'', '').replace('\"', '')
            elem_set, num = line.split(':')
            num=float(num)
            words = elem_set.split(',')
            result = []
            for word in words:
                result.append(word.strip())
            # sets.append(set(result))
            result=frozenset(result)
            supports[result] =num
    return supports
