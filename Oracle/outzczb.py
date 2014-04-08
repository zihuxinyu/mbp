# coding: utf-8
'''
文件作用:定时将oracle dydb的组织架构跑成sql文件,包括删除原数据,插入新数据
'''
from datetime import  datetime

from Library.ziphelper import getzipfile

from Library.DB import tornoracle3
from Library.config import O_database, O_host, O_password, O_port, O_user
import os


def db():
    return tornoracle3.Connection(host=O_host,
                                  port=O_port,
                                  database=O_database,
                                  user=O_user,
                                  password=O_password)


def sendportal():
    path = os.path.abspath(os.path.dirname(__file__)) + '/'
    #目的mysql表名
    tablename = "zczb"
    #sql文件路径
    tmpsqlpath = path + '{0}.sql'.format(tablename)
    #压缩包地址
    tmpzippath = path + '{0}.zip'.format(tablename)
    #从源数据库获取语句
    selectsql = 'select * from zczb'
    opdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    head = "SET NAMES utf8;TRUNCATE {0};\r\nINSERT INTO `{0}` (`guid`, `zdmc`, `sf`, `ds`, `zcly`, `zcbqh`, `yzcbqh`, " \
           "`sblx`, `sbjb`, `yzcmc`, `swmc`, `swzt`, `swfl`, `gsbh`, `zczbbh`, `gkglzyx`, `zygkglbm`, " \
           "`zczyglzrrygbh`, `zgzyglzrrxm`, `qcbzyx`, `dlswbz`, `fzcbqh`, `yyly`, `zcml`, `zchszy`, `zcgjzms`, " \
           "`zcgjz`, `xtzylx`, `gysmc`, `sccsmc`, `yggxh`, `ggxh`, `xlh`, `zcsl`, `zcsldw`, `fzsl`, `fujldw`, `gmrq`, " \
           "`qyrq`, `syys`, `zbksrq`, `zbjzrq`, `xmbh`, `xmmc`, `xmfl`, `sfkr`, `zrbmbm`, `zrbmmc`, `zrrygbh`, " \
           "`zrrxm`, `bgryxdz`, `faddbm`, `faddms`, `bzdz`, `zcyz`, `zcjz`, `whfs`, `whbm`, `whzrrygbh`, `whzrrygxm`, " \
           "`whryxdz`, `sfxcgwb`, `zcgs`, `zypzms`, `xyxt`, `sxsj`, `xxsj`, `edgl`, `dydwgxtzdzjmc`, `sbszjfsx`, " \
           "`jjhlh`, `qsu`, `gd`, `oslxjbb`, `bdxx`, `wxmacdz`, `yxmacdz`, `sbhostname`, `sboid`, `sbdescription`, " \
           "`ipxx`, `slwlsb`, `sbcj`, `jjlx`, `zjlx`, `zjsl`, `jjdsmlx`, `swms`, `zdyt`, `zzbz`, `kzlybz`, `xdbz`, " \
           "`ygcbhjmc`, `ysr`, `fsssjfj`, `bz`, `bfbz`, `bz1`, `bz2`, `bz3`, `bz4`, `bz5`, `sbsmzj`, `sjlyfl`, " \
           "`opdate`) VALUES "

    lines = "('{guid}','{zdmc}','{sf}','{ds}','{zcly}','{zcbqh}','{yzcbqh}','{sblx}','{sbjb}','{yzcmc}','{swmc}'," \
            "'{swzt}','{swfl}','{gsbh}','{zczbbh}','{gkglzyx}','{zygkglbm}','{zczyglzrrygbh}','{zgzyglzrrxm}'," \
            "'{qcbzyx}','{dlswbz}','{fzcbqh}','{yyly}','{zcml}','{zchszy}','{zcgjzms}','{zcgjz}','{xtzylx}'," \
            "'{gysmc}','{sccsmc}','{yggxh}','{ggxh}','{xlh}','{zcsl}','{zcsldw}','{fzsl}','{fujldw}','{gmrq}'," \
            "'{qyrq}','{syys}','{zbksrq}','{zbjzrq}','{xmbh}','{xmmc}','{xmfl}','{sfkr}','{zrbmbm}','{zrbmmc}'," \
            "'{zrrygbh}','{zrrxm}','{bgryxdz}','{faddbm}','{faddms}','{bzdz}','{zcyz}','{zcjz}','{whfs}','{whbm}'," \
            "'{whzrrygbh}','{whzrrygxm}','{whryxdz}','{sfxcgwb}','{zcgs}','{zypzms}','{xyxt}','{sxsj}','{xxsj}'," \
            "'{edgl}','{dydwgxtzdzjmc}','{sbszjfsx}','{jjhlh}','{qsu}','{gd}','{oslxjbb}','{bdxx}','{wxmacdz}'," \
            "'{yxmacdz}','{sbhostname}','{sboid}','{sbdescription}','{ipxx}','{slwlsb}','{sbcj}','{jjlx}','{zjlx}'," \
            "'{zjsl}','{jjdsmlx}','{swms}','{zdyt}','{zzbz}','{kzlybz}','{xdbz}','{ygcbhjmc}','{ysr}','{fsssjfj}'," \
            "'{bz}','{bfbz}','{bz1}','{bz2}','{bz3}','{bz4}','{bz5}','{sbsmzj}','{sjlyfl}','{opdate}'), \r\n"

    man_file = open(tmpsqlpath, 'w', encoding='utf-8')
    man_file.writelines(head.format(tablename))

    list = db().query(selectsql)
    i = 1
    for x in list:
        print(i)
        #去除最后的逗号
        l = len(list)
        lines = lines.rstrip(', \r\n') if (i == l) else lines
        man_file.writelines(lines.format(
            guid=str(i), zdmc=x.X, sf=x.省分, ds=x.地市, zcly=x.资产来源, zcbqh=x.资产标签号, yzcbqh=x.原资产标签号, sblx=x.设备类型,
            sbjb=x.设备级别, yzcmc=x.原资产名称, swmc=x.实物名称, swzt=x.实物状态, swfl=x.实物分类, gsbh=x.公司编号, zczbbh=x.资产账簿编号,
            gkglzyx=x.归口管理专业线, zygkglbm=x.专业归口管理部门, zczyglzrrygbh=x.资产专业管理责任人员工编号, zgzyglzrrxm=x.资产专业管理责任人姓名,
            qcbzyx=x.全成本专业线, dlswbz=x.独立实物标识, fzcbqh=x.父资产标签号, yyly=x.应用领域, zcml=x.资产目录, zchszy=x.资产核算专业,
            zcgjzms=x.资产关键字描述, zcgjz=x.资产关键字, xtzylx=x.系统专业类型, gysmc=x.供应商名称, sccsmc=x.生产厂商名称, yggxh=x.原规格型号,
            ggxh=x.规格型号, xlh=x.序列号, zcsl=x.资产数量, zcsldw=x.资产计量单位, fzsl=x.辅助数量, fujldw=x.辅助计量单位, gmrq=x.购买日期,
            qyrq=x.启用日期, syys=x.使用月数, zbksrq=x.质保开始日期, zbjzrq=x.质保截止日期, xmbh=x.项目编号, xmmc=x.项目名称, xmfl=x.项目分类,
            sfkr=x.是否扩容, zrbmbm=x.责任部门编码, zrbmmc=x.责任部门名称, zrrygbh=x.责任人员工编号, zrrxm=x.责任人姓名, bgryxdz=x.保管人邮箱地址,
            faddbm=x.FA地点编码, faddms=x.FA地点描述, bzdz=x.标准地址, zcyz=x.资产原值, zcjz=x.资产净额, whfs=x.维护方式, whbm=x.维护部门,
            whzrrygbh=x.维护责任人员工编号, whzrrygxm=x.维护责任人员工姓名, whryxdz=x.维护人邮箱地址, sfxcgwb=x.是否需采购维保, zcgs=x.资产归属,
            zypzms=x.主要配置描述, xyxt=x.现有系统, sxsj=x.上线时间, xxsj=x.下线时间, edgl=x.额定功率, dydwgxtzdzjmc=x.对应的网管系统中的主机名称,
            sbszjfsx=x.设备所在机房属性, jjhlh=x.机架行列号, qsu=x.起始U, gd=x.高度, oslxjbb=x.OS类型及版本, bdxx=x.补丁信息, wxmacdz=x.无线MAC地址,
            yxmacdz=x.有线MAC地址, sbhostname=x.设备HOSTNAME, sboid=x.设备OID, sbdescription=x.设备DESCRIPTION, ipxx=x.IP信息,
            slwlsb=x.上联网络设备, sbcj=x.设备层级, jjlx=x.机架类型, zjlx=x.子架类型, zjsl=x.子架数量, jjdsmlx=x.机架单双面类型, swms=x.实物描述,
            zdyt=x.终端用途, zzbz=x.增资标识, kzlybz=x.可再利用标识, xdbz=x.下电标识, ygcbhjmc=x.原工程编号及名称, ysr=x.验收人, fsssjfj=x.附属设施及附件,
            bz=x.备注, bfbz=x.报废标识, bz1=x.备注1, bz2=x.备注2, bz3=x.备注3, bz4=x.备注4, bz5=x.备注5, sbsmzj=x.设备生命周期,
            sjlyfl=x.数据来源分类, opdate=opdate


        ))
        i += 1

    man_file.close()

    # #压缩文件打包
    # getzipfile(filepath=tmpsqlpath, zipname=tmpzippath)
    # #删除文件
    # os.remove(tmpsqlpath)
    #
    # from Library.mailhelper import sendMail
    #
    # subject = '{host}#{db}#{table}'.format(host='134.44.36.190', db='DLS', table=tablename)
    # #print(subject)
    # sendMail(subject, tablename, tmpzippath)
    #
    # subject = '{host}#{db}#{table}'.format(host='119.187.191.82', db='DLS', table=tablename)
    # #sendMail(subject, tablename, tmpzippath)
    # os.remove(tmpzippath)


if __name__ == "__main__":
    sendportal()



        #5小时执行一次
        #time.sleep(60*60*1)
        #time.sleep(120)