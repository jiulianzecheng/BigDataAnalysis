from itertools import combinations, chain

from utils import read_baskets, write_freq_sets, read_freq_sets, get_baskets, get_sets, hash, read_sets, \
    get_supports
import numpy as np


def cadidate(freq_sets1, freq_sets2):
    """
    获取候选频繁项集
    :param freq_sets1: 1阶频繁项集
    :param freq_sets2: n-1频繁项集
    :return:
    """
    cadidate_sets = []
    temp = set()
    # 遍历两个集合
    for elem1 in freq_sets1:
        for elem2 in freq_sets2:
            # 如果elem1不是elem2的子集，合并
            if not (elem1 <= elem2):
                elem3 = elem1 | elem2
                # 采用集合的数据类型，可以避免出现重复的候选频繁项集
                elem3 = frozenset(elem3)
                temp.add(elem3)
    # temp=set(temp)
    # temp=list(temp)
    # 返回n阶候选频繁项集
    for elem in temp:
        cadidate_sets.append(set(elem))
    return cadidate_sets


def freq_sets1(file_sets, file_baskets, file_frequent_sets, min_support_degree):
    '''
    计算一阶频繁项集
    :param file_sets: 候选项集
    :param file_baskets: 购物篮
    :param file_frequent_sets:频繁项集
    :param min_support_degree: 最小支持度
    :return:
    '''
    # 读取候选项集
    sets = read_sets(file_sets)
    # 读取购物篮
    baskets = read_baskets(file_baskets)

    frequent_sets = []
    support_degrees = []
    # 遍历候选项集
    for elem in sets:
        count = 0
        # 候选项集在购物栏中出现一次，count加1
        for basket in baskets:
            if elem <= basket:
                count += 1
        # 计算支持度
        support_degree = count / len(baskets)
        # 选出频繁项集
        if support_degree >= min_support_degree:
            frequent_sets.append(elem)
            support_degrees.append(support_degree)
    # 将计算得到的频繁项集写入文件
    write_freq_sets(frequent_sets, support_degrees, file_frequent_sets)


def freq_sets2(file_frequent_sets1, file_frequent_sets2, file_baskets, file_frequent_sets, min_support_degree):
    """
    计算n阶频繁项集
    :param file_frequent_sets1: 1阶频繁项集
    :param file_frequent_sets2: n-1阶频繁项集
    :param file_baskets: 购物篮
    :param file_frequent_sets:n阶频繁项集
    :param min_support_degree: 最小支持度
    :return:
    """
    # 读取1阶频繁项集
    sets1 = read_freq_sets(file_frequent_sets1)
    # 读取n-1阶频繁项集
    sets2 = read_freq_sets(file_frequent_sets2)
    # 得到候选频繁项集
    cadidate_sets = cadidate(sets1, sets2)
    # 读取购物篮
    baskets = read_baskets(file_baskets)

    frequent_sets = []
    support_degrees = []
    # 遍历候选频繁项集
    for elem in cadidate_sets:
        count = 0
        for basket in baskets:
            # 候选项集在购物篮中出现1次，count + 1
            if elem <= basket:
                count += 1
        # 计算支持度
        support_degree = count / len(baskets)
        # 选出n阶频繁项集
        if support_degree >= min_support_degree:
            frequent_sets.append(elem)
            support_degrees.append(support_degree)
    # 写入对应文件
    write_freq_sets(frequent_sets, support_degrees, file_frequent_sets)


def pcy(file_frequent_sets1, file_frequent_sets2, file_baskets, file_frequent_sets, min_support_degree):
    """
    pcy算法计算n阶频繁项集
    :param file_frequent_sets1: 1阶频繁项集
    :param file_frequent_sets2: n - 1阶频繁项集
    :param file_baskets: 购物篮
    :param file_frequent_sets: n阶频繁项集
    :param min_support_degree: 最小支持度
    :return:
    """
    # 读取1阶频繁项集
    sets1 = read_freq_sets(file_frequent_sets1)
    # 读取n-1阶频繁项集
    sets2 = read_freq_sets(file_frequent_sets2)
    # 得到候选频繁项集
    cadidate_sets = cadidate(sets1, sets2)
    # 读取购物篮
    baskets = read_baskets(file_baskets)
    # 初始化哈希桶
    buckets = np.zeros(len(cadidate_sets))
    frequent_sets = []
    support_degrees = []
    # 遍历候选频繁项集
    for elem in cadidate_sets:
        # 计算该项的哈希值
        index = hash(elem, len(cadidate_sets))
        # 候选项集在购物篮中出现1次，对应哈希桶的计数值 + 1
        for basket in baskets:
            if elem <= basket:
                buckets[index] += 1
    # 遍历候选频繁项集
    for elem in cadidate_sets:
        index = hash(elem, len(cadidate_sets))
        # 找出哈希到频繁桶的项
        if (buckets[index] / len(baskets)) >= min_support_degree:
            # 计算该项的支持度，判断是否真的频繁
            count = 0
            for basket in baskets:
                if elem <= basket:
                    count += 1
            support_degree = count / len(baskets)
            if support_degree >= min_support_degree:
                frequent_sets.append(elem)
                support_degrees.append(support_degree)
    # 写入对应的文件
    write_freq_sets(frequent_sets, support_degrees, file_frequent_sets)


def asso_rules(file_freq_sets, min_confidence, supports, file_write):
    """
    计算关联规则
    :param file_freq_sets: 频繁项集
    :param min_confidence: 最小置信度
    :param supports: 频繁项集支持度
    :param file_write: 要写入的文件
    :return:
    """
    # 读取频繁项集
    sets = read_freq_sets(file_freq_sets)
    # assorules={}
    # confidences=[]
    with open(file_write, 'a') as file_r:
        # 遍历每个频繁项集
        for elem in sets:
            # 获取频繁项集的所有子集
            subsets = list(chain.from_iterable(combinations(elem, r) for r in range(1, len(elem))))
            # 遍历子集
            for subset in subsets:
                # 计算置信度
                confidence = supports[frozenset(elem)] / supports[frozenset(subset)]
                # 获得关联规则
                if confidence >= min_confidence:
                    file_r.write("{},{}:{}\n".format(set(subset), set(set(elem) - set(subset)), confidence))
                    # assorules[frozenset(subset)]=frozenset(set(elem)-set(subset))
                    # confidences.append(confidence)


if __name__ == '__main__':
    # 将跳转关系转化为购物篮
    get_baskets('./links.txt', './result/baskets')
    # 获取所有的项
    get_sets('./reduce.txt', './result/sets')
    # 计算1阶频繁项集
    freq_sets1('./result/sets', './result/baskets', './result/frequent_sets1', 0.15)
    # 计算2阶频繁项集
    freq_sets2('./result/frequent_sets1', './result/frequent_sets1', './result/baskets', './result/frequent_sets2',
               0.15)
    # 计算3阶频繁项集
    freq_sets2('./result/frequent_sets1', './result/frequent_sets2', './result/baskets', './result/frequent_sets3',
               0.15)
    # 计算4阶频繁项集
    freq_sets2('./result/frequent_sets1', './result/frequent_sets3', './result/baskets', './result/frequent_sets4',
               0.15)
    # 利用pcy算法计算2阶频繁项集
    pcy('./result/frequent_sets1', './result/frequent_sets1', './result/baskets', './result/pcy_sets', 0.15)
    # 获取频繁项集的支持度
    supports1 = get_supports('./result/frequent_sets1')
    supports2 = get_supports('./result/frequent_sets2')
    supports3 = get_supports('./result/frequent_sets3')
    supports4 = get_supports('./result/frequent_sets4')
    supports = (supports1) | (supports2) | (supports3) | (supports4)
    # 计算关联规则
    asso_rules('./result/frequent_sets2', 0.3, supports, './result/assorules')
    asso_rules('./result/frequent_sets3', 0.3, supports, './result/assorules')
    asso_rules('./result/frequent_sets4', 0.3, supports, './result/assorules')

