
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from utils import read, merge_combiner, graph, get_words


def reduce(file_read,file_write):
    #打开文件
    file_r=open(file_read,'r')
    file_w=open(file_write,'a')

    result=defaultdict(int)
    titles=[]
    for line in file_r:
        #从shuffle文件中读取记录
        line=line.strip().replace('(','').replace(')','').replace('\'','')
        title,word,num=line.split(',')
        #记录所有的title，以便于生成跳转关系
        titles.append(title)
        #统计每个单词的出现次数
        num=int(num)
        result[word]+=num
    #根据出现次数对单词进行逆序排序
    result = sorted(result.items(),key=lambda x: x[1],reverse=True)
    #将单词的统计结果写入对应的reduce文件中
    for key,value in result:
        file_w.write("{},{}\n".format(key,value))
    return titles
def merge_reduce(file1,file2,file3,file_write):
    '''
    合并3个reduce文件的结果
    :param file1: reduce1.txt
    :param file2: reduce2.txt
    :param file3: reduce2.txt
    :param file_write: reduce.txt
    :return: 无返回值
    '''
    #打开文件
    f1=open(file1,'r')
    f2=open(file2,'r')
    f3=open(file3,'r')
    #合并3个reduce文件中相同的单词
    result=defaultdict(int)
    for line in f1:
        line=line.strip()
        word,num=line.split(',')
        num=int(num)
        result[word]+=num
    for line in f2:
        line = line.strip()
        word,num=line.split(',')
        num=int(num)
        result[word]+=num
    for line in f3:
        line = line.strip()
        word,num=line.split(',')
        num=int(num)
        result[word]+=num
    #将单词按出现次数逆序排序
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    #将前1000个满足在words.txt中的单词写入相应的文件
    words_list = read('./source_data/words.txt')
    with open(file_write,'a') as file_w:
        i = 0
        for key,value in result:
            if key in words_list:
                file_w.write("{},{}\n".format(key, value))
                i += 1
            if(i>=1000):
                break


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as executor:
        future1 = executor.submit(reduce, './shuffle/shuffle1.txt', './reduce/reduce1.txt')
        future2 = executor.submit(reduce, './shuffle/shuffle2.txt', './reduce/reduce2.txt')
        future3 = executor.submit(reduce, './shuffle/shuffle3.txt', './reduce/reduce3.txt')

        title1 = future1.result()
        title2 = future2.result()
        title3 = future3.result()
    #记录所有title中出现的单词，以便于生成跳转关系
    titles=[]
    titles.extend(title1)
    titles.extend(title2)
    titles.extend(title3)
    titles=set(titles)
    #合并3个reduce节点的结果
    merge_reduce('./reduce/reduce1.txt','./reduce/reduce2.txt','./reduce/reduce3.txt','./reduce/reduce.txt')
    #读取最终reduce出的1000个单词
    words=get_words('./reduce/reduce.txt')
    #合并9个combiner文件为1个
    merge_combiner('./combiner','./combiner/combiner')
    #生成跳转关系
    graph(words,titles,'./combiner/combiner','./reduce/graph')