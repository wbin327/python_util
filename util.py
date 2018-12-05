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


def load_setting_from_obj(obj: object):
    """
    读取对象中所有自定义的属性，保存在一个字典中并返回
    :param obj:对象
    :return: attrs,保存了对象所有自定义属性的字典
    """
    attrs = {key: values for key, values in obj.__dict__.items() if not key.startswith('__')}
    return attrs
