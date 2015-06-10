#!/usr/bin/env python3

import jieba.posseg as pseg
import zlib

ignore = ['x', 'uj', 'ul', 'y', 'p', 'c', 'd']
#ignore = []

def getWords(data):
    words = pseg.cut(data) 
    res = {}
    for word, flag in words:
#        print(word, flag)
        if flag in ignore:
            continue
        if word in res:
            res[word] = res[word] + 1
        else:
            res[word] = 1
    return res

def simHash(words):
    s = [0 for i in range(0, 32)]
    for i in words:
        v = words[i]
        cksum = zlib.adler32(i.encode('utf8')) 
        for k in range(0, 32):
            if (cksum >> k) & 1 == 0:
                s[k] = s[k] - v
            else:
                s[k] = s[k] + v
    res = 0
    for i in s:
        if i > 0:
            res = res | 1
        else:
            res = res | 0
        res = res << 1
    return res

def getSimHash(data):
    return simHash(getWords(data))

def getDis(hash1, hash2):
    dis = 0
    for i in range(0, 32):
        if ((hash1>>i)&1) ^ ((hash2>>i)&1) == 1:
            dis = dis + 1; 
    return dis


#demo

data1 = "理解分治法的算法思想，阅读实现书上已有的部分程序代码并完善程序，加深对分治法 的算法原理及实现过程的理解。用分治法实现一组无序序列的两路合并排序和快速排序。要求清楚合并排序及快速排序 的基本原理，编程实现分别用这两种方法将输入的一组无序序列排序为有序序列后输出。"
data2 = "弄清楚分治法的算法思想，实现书上已有的部分程序代码并且完善之，加深对分治法的算法原理及实现过程的理解。用分治法实现一组无序序列的两路合并排序和快速排序。要求搞懂合并排序及快速排序的原理，分别实现这两种方法将输入的一组无序序列排序为有序序列后输出。"


hash1 = getSimHash(data1)
print("simhash for data1: ", hash1)
hash2 = getSimHash(data2)
print("simhash for data2: ", hash2)

print("distance: ", getDis(hash1, hash2))
