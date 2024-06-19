import sys
import threading
import time

def hash(word):
    '''
    哈希函数
    :param word: 被哈希的单词
    :return: 哈希值
    '''
    hash_value=0
    #根据单词每个字母的ascall码值的和模3计算哈希值
    for char in word:
        hash_value+=ord(char)
    hash_value=hash_value%3

    return hash_value

def shuffle(filepath):
    #打开文件
    file_r=open(filepath)
    shuffle1 = open('./shuffle/shuffle1.txt','a')
    shuffle2 = open('./shuffle/shuffle2.txt', 'a')
    shuffle3 = open('./shuffle/shuffle3.txt', 'a')

    for line in file_r:
        #读取combiner中的记录
        line=line.strip().replace('(','').replace(')','')
        title,word,num=line.split(',')
        #根据每个单词的哈希值选择要shuffle到的文件
        if hash(word)==0:
            shuffle1.write("({},{}),{}\n".format(title,word,num))
        elif hash(word)==1:
            shuffle2.write("({},{}),{}\n".format(title,word,num))
        else:
            shuffle3.write("({},{}),{}\n".format(title,word,num))
if __name__ == '__main__':
    t1 = threading.Thread(target=shuffle('./combiner/combiner1.txt'),args=("t1",))
    t2 = threading.Thread(target=shuffle('./combiner/combiner2.txt'), args=("t2",))
    t3 = threading.Thread(target=shuffle('./combiner/combiner3.txt'), args=("t3",))
    t4 = threading.Thread(target=shuffle('./combiner/combiner4.txt'), args=("t4",))
    t5 = threading.Thread(target=shuffle('./combiner/combiner5.txt'), args=("t5",))
    t6 = threading.Thread(target=shuffle('./combiner/combiner6.txt'), args=("t6",))
    t7 = threading.Thread(target=shuffle('./combiner/combiner7.txt'), args=("t7",))
    t8 = threading.Thread(target=shuffle('./combiner/combiner8.txt'), args=("t8",))
    t9 = threading.Thread(target=shuffle('./combiner/combiner9.txt'), args=("t9",))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
