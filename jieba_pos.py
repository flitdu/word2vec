# -*- coding: utf-8 -*-
"""
Created by Dufy on 2020/1/16  16:08
IDE used: PyCharm
Description :
1)
2)
Remark:
"""

# encoding=utf-8
import time
start = time.time()
import jieba
import jieba.posseg as pseg
print('加载型号词典.....')
# jieba.load_userdict(r'.\data\fastvec_dict.txt')
# jieba.load_userdict(r'D:\dufy\code\ft_BOM\data\ft_vec\dict\测试2.txt')
jieba.load_userdict(r'D:\dufy\code\ft_BOM\data\ft_vec\dict\part_number.txt')
import re
print('结束！！！,用时:{}s'.format(time.time()-start))
# with open('测试.txt', 'r', encoding='utf-8') as fr:
#     print('加载型号词典.....')
#     f = fr.readlines()
#     for line in f:
#         # print(line.strip())
#         # # print("==================")
#         jieba.add_word(line.strip(), tag='pn')
#         pseg.re_han_internal = re.compile('(.+)', re.U)  # 修改格式
#     print('加载完毕！')


def PN_if(str1):  #词性返回
    pass
    words1 = pseg.cut(str1)
    for _, flag in words1:
        # print(flag)
        if 'pn' in flag:
            return 1
    return 0



if __name__ == "__main__":

    while True:
        bom_line = input('输入待预测BOM行：')

        if bom_line != 'end':
            line_txt_list = []
            words1 = pseg.cut(bom_line)
            # words2 = pseg.cut(bom_line.replace('-', ''))
            for word, flag in words1:
                line_txt_list.append('%s %s' % (word, flag))
            # for word, flag in words2:
            #     line_txt_list.append('%s %s' % (word, flag))
            list_new = list(set(line_txt_list))
            print('|'.join(list_new))
        else:
            break  # 结束循环

