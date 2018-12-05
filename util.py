# coding:utf-8
import os


def mkdir(path):
    """判断文件夹是否存在，不存在就创建"""
    if not os.path.exists(path):
        os.mkdir(path)


def get_path():
    """获取当前文件所处的路径"""
    path = os.getcwd()
    return path

