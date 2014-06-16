import tablib
from autodb.Logic.Oracledb import db
from pony.orm import *
from time import clock

@db_session
def main():
    start = clock()


    import xlsxwriter

    workbook = xlsxwriter.Workbook('hello.xlsx', {'constant_memory': True})
    worksheet = workbook.add_worksheet()





    #data = db.execute("select * from GBY_QIANFEI_GUWANG_ALL t"    EXT_DPT_USR)
    sqlcount="select count(*) from EXT_DPT_USR t"
    data = db.execute("select * from EXT_DPT_USR t")
    count=db.execute(sqlcount)
    for x in count:
        row=int(x[0])
        break
    print(row)

    for d in data:

        col=len(d)

        break
    print(col)


    i = 0
    for d in data:
        for x in xrange(col):
            #print(i,x,d[x])
            worksheet.write(i, x, d[x])
        i=i+1

    workbook.close()
    finish = clock()
    print (finish - start) / 1000000
if __name__=="__main__":
    main()