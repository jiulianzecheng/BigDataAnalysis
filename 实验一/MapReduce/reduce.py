import concurrent
import re
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from utils import merge_reduce, read, merge_combiner, graph, get_words


def reduce(file_read,file_write):
    file_r=open(file_read,'r')
    file_w=open(file_write,'a')
    result=defaultdict(int)
    titles=[]
    for line in file_r:

        line=line.strip().replace('(','').replace(')','').replace('\'','')
        title,word,num=line.split(',')
        titles.append(title)
        num=int(num)
        result[word]+=num

    result = sorted(result.items(),key=lambda x: x[1],reverse=True)

    for key,value in result:
        file_w.write("{},{}\n".format(key,value))
    return titles



if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as executor:
        future1 = executor.submit(reduce, './shuffle/shuffle1.txt', './reduce/reduce1.txt')
        future2 = executor.submit(reduce, './shuffle/shuffle2.txt', './reduce/reduce2.txt')
        future3 = executor.submit(reduce, './shuffle/shuffle3.txt', './reduce/reduce3.txt')

        title1 = future1.result()
        title2 = future2.result()
        title3 = future3.result()
    titles=[]
    titles.extend(title1)
    titles.extend(title2)
    titles.extend(title3)
    titles=set(titles)
    merge_reduce('./reduce/reduce1.txt','./reduce/reduce2.txt','./reduce/reduce3.txt','./reduce/reduce.txt')
    words=get_words('./reduce/reduce.txt')
    merge_combiner('./combiner','./combiner/combiner')
    graph(words,titles,'./combiner/combiner','./reduce/graph')