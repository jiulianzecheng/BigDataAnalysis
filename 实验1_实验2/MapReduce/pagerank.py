from collections import defaultdict

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


def construct(words,file_read):
    '''
    将跳转关系转换为节点，边的图形式
    :param words:
    :param file_read:
    :return:
    '''
    nodes=defaultdict(int)
    out_degree=defaultdict(int)
    edges=defaultdict(list)
    #初始化每个节点的pagerank值
    for word in words:
        nodes[word]=1/len(words)

    with open(file_read,'r') as file_r:
        for line in file_r:
            line=line.strip()
            node,edge=line.split(',',1)
            node=node.strip()
            #得到每个节点的相邻节点
            edge=edge.strip()
            edge=edge.replace('\'','').replace('[','').replace(']','')
            next_nodes=edge.split(',')
            #得到每个节点的出度
            if next_nodes == ['']:
                out_degree[node] = 0
            else:
                out_degree[node] = len(next_nodes)
                #以邻接链表的形式表示图的有向边
                for next_node in next_nodes:
                    edges[node].append(next_node.strip())
                # edges[node]=next_nodes
    return nodes,out_degree,edges
def pagerank(words,nodes,out_degree,edges,beta,theta,max_iteraters,file_write):
    '''
    迭代计算pagerank值
    :param words: 选出的1000个单词
    :param nodes: 有向图每个节点的pagerank初始值
    :param out_degree: 每个节点的出度
    :param edges: 有向图的边
    :param beta: 修正因子
    :param theta:收敛域
    :param max_iteraters:最大迭代次数
    :param file_write:计算出的pagerank要写入的文件
    :return:
    '''
    for i in range(max_iteraters):
        #nodes_next表示迭代后的pagerank值
        nodes_next=defaultdict(int)
        #根据边ij更新节点j的pagerank值
        for node in words:
            for next_node in edges[node]:
                nodes_next[next_node]+=nodes[node]*beta/out_degree[node]
        #计算泄露的pagerank值
        leak=1-(sum(nodes_next.values())+1-beta)

        for node in words:
            #计算随机跳转的pagerank值(
            nodes_next[node]+=(1-beta)/len(words)
            #归一化处理，将泄露的pagerank值补回到系统中
            nodes_next[node]+=leak/len(words)
        #判断是否已经近似收敛，近似收敛则结束迭代
        flag=0
        for node in words:
            if abs(nodes_next[node]-nodes[node]) > theta:
                flag=1
                break
        if flag==0:
            nodes = nodes_next
            break
        nodes=nodes_next
    #写入文件
    with open(file_write, 'w') as file_w:
        for key, value in nodes.items():
            file_w.write("{},{}\n".format(key, value))
    return nodes

if __name__ == '__main__':
    words=get_words('./reduce/reduce.txt')
    nodes,out_degree,edges=construct(words,'./reduce/graph')
    nodes=pagerank(words,nodes,out_degree,edges,0.85,1e-8,10000,'./pagerank')
    print("total pagerank:")
    print(sum(nodes.values()))