#!python 
#coding=utf-8

import os,sys
from xml.etree import ElementTree
from PIL import Image
 
def tree_to_dict(tree) -> dict:
    '''
    将xml文件读取的Tree格式转换成Dict字典\n
    Args:
        tree:xml文件的tree
    Returns:
        dict
    '''

    d = {}
    for index, item in enumerate(tree):
        if item.tag == 'key':
            if tree[index+1].tag == 'string':
                d[item.text] = tree[index + 1].text
            elif tree[index + 1].tag == 'true':
                d[item.text] = True
            elif tree[index + 1].tag == 'false':
                d[item.text] = False
            elif tree[index+1].tag == 'dict':
                d[item.text] = tree_to_dict(tree[index+1])
    return d
 
def gen_png_from_plist(plist_filename, png_filename):
    '''
    将plist文件转换为png小图\n
    Args:
        plist_filename:XX.plist文件
        png_filename:XX.png文件
    '''

    file_path = plist_filename.replace('.plist', '')
    big_image = Image.open(png_filename)
    root = ElementTree.fromstring(open(plist_filename, 'r').read())

    plist_dict = tree_to_dict(root[0])
    to_list = lambda x: x.replace('{','').replace('}','').split(',')
    for k,v in plist_dict['frames'].items():
        rectlist = to_list(v['frame'])
        width = int( rectlist[3] if v['rotated'] else rectlist[2] )
        height = int( rectlist[2] if v['rotated'] else rectlist[3] )
        box=( 
            int(rectlist[0]),
            int(rectlist[1]),
            int(rectlist[0]) + width,
            int(rectlist[1]) + height,
        )
        sizelist = [ int(x) for x in to_list(v['sourceSize']) ]
        rect_on_big = big_image.crop(box)
 
        if v['rotated']:
            rect_on_big = rect_on_big.transpose(Image.ROTATE_90)

        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        outfile = (file_path+'/' + k).replace('gift_', '')
        print ("输出文件：",outfile)
        rect_on_big.save(outfile)
    print("图集转换完成！")
    input("输入回车退出……")


if __name__ == '__main__':

    info=r'''
        Name:    Plist图集转换小图工具
        use:     用于将cocos使用的plist图集逆转换成小图
        Author:  Liushun
        Time:    2021-4-27
        input:   输入需要转换的图集名（也可以是绝对路径），不包含后缀名
    '''
    print(info)
    filename=input("filename：")
    plist_filename = filename + '.plist'
    png_filename = filename + '.png'
    if (os.path.exists(plist_filename) and os.path.exists(png_filename)):
        gen_png_from_plist( plist_filename, png_filename )
    else:
        print("确保输入的文件拥有plist和png文件")
        input("输入回车退出……")

