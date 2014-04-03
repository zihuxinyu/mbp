# coding: utf-8
import os
import zipfile
def getzipfile(filepath,zipname=None):
    """
    将文件压缩
    :param filefullpath:文件完全路径
    :param zipname:压缩文件名
    """
    filename= os.path.split(filepath)[1]
    zipname=zipname if zipname else filename.split('.')[0]+'.zip'
    zipFile = zipfile.ZipFile(zipname, 'w')
    zipFile.write(filepath, filename, zipfile.ZIP_DEFLATED)
    zipFile.close()