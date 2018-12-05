# coding:utf-8
import logging


def get_logger(file_path, name='default'):
    """
    创建日志
    :param name: 日志对象名
    :param file_path: 日志文件路径
    :return:
    """
    # 创建logger日志器，如果name为空则返回root
    logger = logging.getLogger(name)
    # 设置日志等级：debug->info->warning->error->critical
    logger.setLevel(logging.DEBUG)

    # 设置日期格式
    setdatefmt = '%Y-%m-%d %H:%M:%S'
    # 日志输出的格式
    setformat = '%(asctime)s => %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s - %(message)s'

    # 判断logger.handlers列表为空则添加，否则直接使用原handler处理器写日志
    if not logger.handlers:
        fh = logging.FileHandler(file_path, encoding='utf-8')  # 若已有日志，则追加写入
        # ch = logging.StreamHandler()  # 将日志发送到Steam

        # 设置handlers处理器的日志输出格式
        formatter = logging.Formatter(fmt=setformat, datefmt=setdatefmt)
        fh.setFormatter(formatter)
        # ch.setFormatter(formatter)

        # 为logger日志器添加上创建好的处理器handlers
        logger.addHandler(fh)
        # logger.addHandler(ch)

    # 移除重复的handlers处理器，避免setlogging.baseConfig()时输出重复日志
    # logger.removeHandler(fh)
    # logger.removeHandler(ch)
    return logger