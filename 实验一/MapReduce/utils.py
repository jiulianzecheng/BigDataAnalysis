import os
import re
from collections import defaultdict


def read(filepath):
    '''
    从文档中读取英文单词并转换为小写
    :param filepath: 文档路径
    :return: 单词列表
    '''
    file=open(filepath,encoding='utf-8')
    content=file.read()
    file.close()
    #正则表达式
    pattern = '[a-zA-Z]+'
    words = re.findall(pattern, content)
    #转换成小写
    words=list(word.lower() for word in words)
    return words
def merge_reduce(file1,file2,file3,file_write):
    f1=open(file1,'r')
    f2=open(file2,'r')
    f3=open(file3,'r')
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

    words_list = read('./source_data/words.txt')
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    with open(file_write,'a') as file_w:
        i = 0
        for key,value in result:
            if key in words_list:
                file_w.write("{},{}\n".format(key, value))
                i += 1
            if(i>=1000):
                break
def get_words(file):
    words=[]
    with open(file,'r') as file:
        for line in file:
            word,num=line.split(',')
            words.append(word.strip())
    return words

def merge_combiner(filepath,file_write):
    file_list=os.listdir(filepath)
    file_w=open(file_write,'a')
    for i in range(len(file_list)):
        file_list[i]=filepath+'/'+file_list[i]
        with open(file_list[i],'r') as file:
            for line in file:
                line = line.strip().replace('(','').replace(')','').replace('\'','')
                title,word,num=line.split(',')
                file_w.write("{},{},{}\n".format(title.strip(), word.strip(),num.strip()))
def graph(words,titles,combiner_file,file_write):
    graph={}
    dict={}
    with open(combiner_file,'r') as file:
        for line in file:
            line=line.strip()
            title,word,num=line.split(',')
            if title in dict.keys():
                dict[title].append(word)
            else:
                dict[title]=[]
                dict[title].append(word)
    for word in words:
        graph[word]=[]
        # if word in titles:
        for reference_word in dict[word]:
            if reference_word in words:
                graph[word].append(reference_word)
    with open(file_write,'a') as file_w:
        for node,list in graph.items():
            file_w.write("{},{}\n".format(node,list))