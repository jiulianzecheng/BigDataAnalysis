from collections import defaultdict

from utils import get_words


def construct(words,file_read):
    '''
    将跳转关系转换为
    :param words:
    :param file_read:
    :return:
    '''
    nodes=defaultdict(int)
    out_degree=defaultdict(int)
    edges=defaultdict(list)
    for word in words:
        nodes[word]=1/len(words)
    with open(file_read,'r') as file_r:
        for line in file_r:
            line=line.strip()
            node,edge=line.split(',',1)
            node=node.strip()
            edge=edge.strip()
            edge=edge.replace('\'','').replace('[','').replace(']','')
            next_nodes=edge.split(',')
            if next_nodes == ['']:
                out_degree[node] = 0
            else:
                out_degree[node] = len(next_nodes)
                for next_node in next_nodes:
                    edges[node].append(next_node.strip())
                # edges[node]=next_nodes
    return nodes,out_degree,edges
def pagerank(words,nodes,out_degree,edges,beta,theta,max_iteraters,file_write):
    for i in range(max_iteraters):
        nodes_next=defaultdict(int)
        for node in words:
            for next_node in edges[node]:
                nodes_next[next_node]+=nodes[node]*beta/out_degree[node]
        leak=1-(sum(nodes_next.values())+1-beta)
        for node in words:
            nodes_next[node]+=(1-beta)/len(words)
            nodes_next[node]+=leak/len(words)
        flag=0
        for node in words:
            if abs(nodes_next[node]-nodes[node])>theta:
                flag=1
                break
        if flag==0:
            nodes = nodes_next
            break
        nodes=nodes_next
    return nodes
    with open(file_write,'w') as file_w:
        for key,value in nodes.items():
            file_w.write("{},{}\n".format(key,value))
if __name__ == '__main__':
    words=get_words('./reduce/reduce.txt')
    nodes,out_degree,edges=construct(words,'./reduce/graph')
    nodes=pagerank(words,nodes,out_degree,edges,0.85,1e-8,10000,'./pagerank')
    print(sum(nodes.values()))