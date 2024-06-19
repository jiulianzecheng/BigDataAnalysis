import json
import sys
import threading
import time
from collections import defaultdict


def combine(file_read,file_write):
    file_r=open(file_read)
    file_w=open(file_write,'a')
    result =defaultdict(int)
    for line in file_r:
        line = line.strip()
        line=line.replace('(','').replace(')','')
        title, word, num = line.split(',')
        key=(title.strip(),word.strip())
        num = int(num)
        result[key]+=num
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    for key,value in result:
        file_w.write("{},{}\n".format(key, value))
if __name__ == '__main__':
    t1=threading.Thread(target=combine('./map/map1.txt','./combiner/combiner1.txt'),args=("t1",))
    t2 = threading.Thread(target=combine('./map/map2.txt', './combiner/combiner2.txt'), args=("t2",))
    t3 = threading.Thread(target=combine('./map/map3.txt', './combiner/combiner3.txt'), args=("t3",))
    t4 = threading.Thread(target=combine('./map/map4.txt', './combiner/combiner4.txt'), args=("t4",))
    t5 = threading.Thread(target=combine('./map/map5.txt', './combiner/combiner5.txt'), args=("t5",))
    t6 = threading.Thread(target=combine('./map/map6.txt', './combiner/combiner6.txt'), args=("t6",))
    t7 = threading.Thread(target=combine('./map/map7.txt', './combiner/combiner7.txt'), args=("t7",))
    t8 = threading.Thread(target=combine('./map/map8.txt', './combiner/combiner8.txt'), args=("t8",))
    t9 = threading.Thread(target=combine('./map/map9.txt', './combiner/combiner9.txt'), args=("t9",))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
