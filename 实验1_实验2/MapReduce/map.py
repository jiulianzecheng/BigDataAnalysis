import threading
import time
import os

from utils import read

def mapper(filepath,words_file,file_write):
    #获取目录下的所有文档路径
    file_list=os.listdir(filepath)
    for i in range(len(file_list)):
        file_list[i]=filepath+'/'+file_list[i]

    for i in range(len(file_list)):
        #读取文档中的单词
        words = read(file_list[i])
        #写入相应的文件
        with open(file_write,'a') as file_w:
            for word in words:
                file_w.write("(({}, {}), 1)\n".format(file_list[i].replace(filepath + '/', "").replace('.txt',''), word))

if __name__ == '__main__':
    t1 = threading.Thread(target=mapper('./source_data/folder_1', './source_data/words.txt','./map/map1.txt'), args=("t1",))
    t2 = threading.Thread(target=mapper('./source_data/folder_2', './source_data/words.txt','./map/map2.txt'), args=("t2",))
    t3 = threading.Thread(target=mapper('./source_data/folder_3', './source_data/words.txt','./map/map3.txt'), args=("t3",))
    t4 = threading.Thread(target=mapper('./source_data/folder_4', './source_data/words.txt','./map/map4.txt'), args=("t4",))
    t5 = threading.Thread(target=mapper('./source_data/folder_5', './source_data/words.txt','./map/map5.txt'), args=("t5",))
    t6 = threading.Thread(target=mapper('./source_data/folder_6', './source_data/words.txt','./map/map6.txt'), args=("t6",))
    t7 = threading.Thread(target=mapper('./source_data/folder_7', './source_data/words.txt','./map/map7.txt'), args=("t7",))
    t8 = threading.Thread(target=mapper('./source_data/folder_8', './source_data/words.txt','./map/map8.txt'), args=("t8",))
    t9 = threading.Thread(target=mapper('./source_data/folder_9', './source_data/words.txt','./map/map9.txt'), args=("t9",))
    start = time.perf_counter()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t1.join()

