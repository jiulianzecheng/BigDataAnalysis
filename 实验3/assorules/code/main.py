from itertools import combinations, chain

from utils import read_baskets, write_freq_sets, read_freq_sets, cadidate, get_baskets, get_sets, hash, read_sets, \
    get_supports
import numpy as np

def freq_sets1(file_sets,file_baskets,file_frequent_sets,min_support_degree):
    #读取候选项集
    sets=read_sets(file_sets)
    #读取购物篮
    baskets=read_baskets(file_baskets)
    frequent_sets=[]
    support_degrees=[]
    for elem in sets:
        count=0
        #候选项集在购物栏中出现一次，count加1
        for basket in baskets:
            if elem<=basket:
                count+=1
        #计算支持度
        support_degree=count/len(baskets)
        if support_degree>=min_support_degree:
            frequent_sets.append(elem)
            support_degrees.append(support_degree)
    write_freq_sets(frequent_sets,support_degrees,file_frequent_sets)
def freq_sets2(file_frequent_sets1,file_frequent_sets2,file_baskets,file_frequent_sets,min_support_degree):
    sets1=read_freq_sets(file_frequent_sets1)
    sets2=read_freq_sets(file_frequent_sets2)
    cadidate_sets=cadidate(sets1,sets2)
    baskets=read_baskets(file_baskets)
    frequent_sets = []
    support_degrees = []
    for elem in cadidate_sets:
        count=0
        for basket in baskets:
            if elem<=basket:
                count+=1
        support_degree=count/len(baskets)
        if support_degree >= min_support_degree:
            frequent_sets.append(elem)
            support_degrees.append(support_degree)
    write_freq_sets(frequent_sets,support_degrees, file_frequent_sets)

def pcy(file_frequent_sets1,file_frequent_sets2,file_baskets,file_frequent_sets,min_support_degree):
    sets1=read_freq_sets(file_frequent_sets1)
    sets2=read_freq_sets(file_frequent_sets2)
    cadidate_sets=cadidate(sets1,sets2)
    baskets=read_baskets(file_baskets)
    buckets=np.zeros(len(cadidate_sets))
    frequent_sets=[]
    support_degrees=[]
    for elem in cadidate_sets:
        index=hash(elem,len(cadidate_sets))
        for basket in baskets:
            if elem <= basket:
                buckets[index]+=1
    for elem in cadidate_sets:
        index=hash(elem,len(cadidate_sets))
        if (buckets[index]/len(baskets)) >= min_support_degree:
            count=0
            for basket in baskets:
                if elem <= basket:
                    count+=1
            support_degree=count/len(baskets)
            if support_degree >= min_support_degree:
                frequent_sets.append(elem)
                support_degrees.append(support_degree)
    write_freq_sets(frequent_sets,support_degrees, file_frequent_sets)

def asso_rules(file_freq_sets,min_confidence,supports,file_write):
    sets=read_freq_sets(file_freq_sets)
    # assorules={}
    # confidences=[]
    with open(file_write, 'a') as file_r:
        for elem in sets:
            subsets=list(chain.from_iterable(combinations(elem,r) for r in range(1,len(elem))))
            for subset in subsets:
                confidence=supports[frozenset(elem)]/supports[frozenset(subset)]
                if confidence>=min_confidence:
                    file_r.write("{},{}:{}\n".format(set(subset),set(set(elem)-set(subset)),confidence))
                    # assorules[frozenset(subset)]=frozenset(set(elem)-set(subset))
                    # confidences.append(confidence)





if __name__ == '__main__':
    get_baskets('./links.txt','./result/baskets')
    get_sets('./reduce.txt','./result/sets')
    freq_sets1('./result/sets','./result/baskets','./result/frequent_sets1',0.15)
    freq_sets2('./result/frequent_sets1','./result/frequent_sets1','./result/baskets','./result/frequent_sets2',0.15)
    freq_sets2('./result/frequent_sets1', './result/frequent_sets2', './result/baskets', './result/frequent_sets3', 0.15)
    freq_sets2('./result/frequent_sets1', './result/frequent_sets3', './result/baskets', './result/frequent_sets4', 0.15)
    pcy('./result/frequent_sets1', './result/frequent_sets1', './result/baskets', './result/pcy_sets', 0.15)
    supports1 = get_supports('./result/frequent_sets1')
    supports2 = get_supports('./result/frequent_sets2')
    supports3 = get_supports('./result/frequent_sets3')
    supports4 = get_supports('./result/frequent_sets4')
    supports=(supports1)|(supports2)|(supports3)|(supports4)
    assorules2=asso_rules('./result/frequent_sets2',0.3,supports,'./result/assorules')
    assorules3 = asso_rules('./result/frequent_sets3', 0.3, supports,'./result/assorules')
    assorules4 = asso_rules('./result/frequent_sets4', 0.3, supports,'./result/assorules')
    # assorules=assorules2|assorules3|assorules4


