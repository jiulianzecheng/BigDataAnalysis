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

def get_words(file):
    '''
    从文件中读取所有的单词的集合
    :param file: 文件路径
    :return: 单词集合
    '''
    words=[]
    with open(file,'r') as file:
        for line in file:
            word,num=line.split(',')
            words.append(word.strip())
    return words

def merge_combiner(filepath,file_write):
    '''
    合并9个combiner文件到1个combiner
    :param filepath: 目录路径
    :param file_write: 要合并到的combiner文件路径
    :return:
    '''
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
    '''
    生成跳转关系
    :param words: reduce出的单词
    :param titles: 在title中出现过的单词的集合
    :param combiner_file: combiner合并后的结果
    :param file_write: 最后跳转关系写入的文件
    :return:
    '''
    graph={}
    dict={}

    with open(combiner_file,'r') as file:
        for line in file:
            line=line.strip()
            title,word,num=line.split(',')
            #通过combiner生成每个title对应的跳转关系
            if title in dict.keys():
                dict[title].append(word)
            else:
                dict[title]=[]
                dict[title].append(word)

    for word in words:
        graph[word]=[]
        #reduce出的单词在title中出现过
        if word in titles:
            #找出其所有的跳转单词
            for reference_word in dict[word]:
                if reference_word in words:
                    graph[word].append(reference_word)
    #写入文件
    with open(file_write,'a') as file_w:
        for node,list in graph.items():
            file_w.write("{},{}\n".format(node,list))