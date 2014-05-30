# _*_ coding:utf8 _*_
import ImageDraw
import requests
import random
import time
import re
from random import choice
import Image,ImageEnhance,ImageFile
from pytesser import *

from PIL import Image
from StringIO import StringIO
def do(ip):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.1.0.1600 Chrome/26.0.1410.43 Safari/537.1",
        "X-Forwarded-For": ip,
        "Referer": "http://vote.dongyingnews.cn/module/vote/content/?id=15",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-Hans,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Host": "vote.dongyingnews.cn",
        "DNT": "1",
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache",
        "Cookie": "PHPSESSID=ahqsjs8b75t91c2mgv5485s4u5"
    }


    pageurl='http://vote.dongyingnews.cn/module/vote/content/?id=15'
    r = requests.get(pageurl, headers=headers)
    reg= r"<input type='hidden' .*?value='(.*?)'.*?>"
    keys=re.findall(reg, r.text)[0]

    code= r'<input type="text" size="10" .*?name="(.*?)".*?>'
    codes = re.findall(code, r.text)[0]
    #print(codes)



    id = ['356', '319', '357', '337', '329', '328', '316', '315', '322', '318', '351', '332', '312', '314', '320',
          '352', '349', '338', '358', '343', '323', '313', '359', '360', '334', '336', '327', '344', '346', '310']



    url = 'http://vote.dongyingnews.cn/module/vote/content/?mode=&fied=&sort=&action=post&id=15'

    picurl = 'http://vote.dongyingnews.cn/api.php?action=captcha'
    r = requests.get(picurl, headers=headers)
    x=getcode(r)
    #print(x)
    if len(x)==4:
        values="keys={0}&G-37%5B%5D={1}&G-37%5B%5D={2}&G-37%5B%5D={3}&G-37%5B%5D={4}&G-37%5B%5D={5}&G-37%5B%5D={6}&G-37" \
               "%5B%5D={7}&G-37%5B%5D={8}&G-37%5B%5D={9}&G-37%5B%5D={10}&{11}={12}".format(keys,337, choice(id), choice(id),choice(id), choice(id),
                                                                                 choice(id), choice(id), choice(id),

                                                                                 choice(id), choice(id),codes,x)
        values=values.replace('318','337').replace('316', '337').replace('351', '337').replace('343', '337')
        r = requests.post(url, data=values, headers=headers)
        #print( r.text)
        if '感谢' in r.content:
            print('True')
    #print('ok')


def getcode(r):


    im = Image.open(StringIO(r.content))
    im = im.convert('L')
    threshold = 100
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = im.point(table, '1')

    x = image_to_string(out)
    x = x.upper()
    x = x.replace('.', '').replace('"', '').replace('_', '').replace('‘', '') \
        .replace("'", "").replace('~', '').replace(',', '').replace('“', '') \
        .replace("/", '').replace(';', '').replace(' ', '').replace('/?', '2')
    x = x.replace('E', '8')
    x = x.replace(']', '1')
    x = x.replace('\\', '')
    x = x.replace('Z', '2')
    x = x.replace('’', '')
    x = x.replace('-', '')
    x = x.replace('$', '5')
    x = x.replace('"1', '4')
    x = x.replace('A', '4')
    x = x.replace('B', '9')
    x = x.replace('-I', '4')
    x = x.replace('S', '5')
    x = x.replace('£', '2')
    x = x.replace('T', '7')
    x = x.replace('!', '1')
    x = x.replace('H', '4')
    x = x.replace('D', '0')
    x = x.replace('V', '1')
    x = x.replace('—I', '4')
    x = x.replace('I', '1')
    x = x.replace('U', '0')
    # print(x)
    # try:
    #     out.save("pic/s/{0}.png".format(x))
    # except:
    #     pass
    return  x[0:4]


#二值数组
t2val = {}


def twoValue(image, G):
    for y in xrange(0, image.size[1]):
        for x in xrange(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0


# 降噪
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败
def clearNoise(image, N, Z):
    for i in xrange(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in xrange(1, image.size[0] - 1):
            for y in xrange(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1


def saveImage(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in xrange(0, size[0]):
        for y in xrange(0, size[1]):
            draw.point((x, y), t2val[(x, y)])

    image.save('pic/er{0}.png'.format(str(filename)))
    print(image_file_to_string('pic/er{0}.png'.format(str(filename))))

def division(img,xxxx):  #图像的分割，就是验证码按字符分割出来
    global nume
    nume=0
    font = []
    for i in range(4):
        x =  i *22  #该函数中的像素值都需要自己进行微调
        y = 2
        temp = img.crop((x, y, x + 20, y + 30))

        temp.save("pic/s/{0}-{1}.png".format(xxxx,nume))
        nume = nume + 1
        font.append(temp)
    return font

# image = Image.open("d:/1.jpg").convert("L")
# twoValue(image, 100)
# clearNoise(image, 4, 1)
# saveImage("d:/5.jpg", image.size)


if __name__ == "__main__":
    while 1:

        ip1 = [27, 39, 112, 119, 182, 124, 60, 113, 123, 122, 211, 218, 59, 222, 221, 150, 153, 219, 58, 106, 61, 180,
               114, 202, 103, 203]
        ip2 = [192, 64, 224, 176, 32, 128, 208, 120, 4, 232, 168, 164, 56, 80, 132, 174, 0, 138, 118, 214, 206, 86, 218,
           162, 216, 14, 74, 235, 2, 58, 173, 156, 201, 115, 121, 122, 179, 223, 133, 3, 98, 59, 110, 136, 102, 22, 93]

        dy1=['123', '124', '182', '202', '203', '210', '211', '218', '58', '60', '61', '113', '117', '119', '121',
             '122', '221', '219', '222']
        dy2=['129', '134', '170', '131', '201', '36', '102', '110', '194', '93', '52', '90', '97', '163', '56', '57',
             '214', '133', '156', '162', '232', '122', '126', '76', '185', '186', '187', '249', '6', '2', '173', '146',
             '58', '59', '174', '206']

        ip = '{0}.{1}.{2}.{3}'.format(choice(ip1), choice(ip2), random.randint(0, 255), random.randint(0, 255))
        #print(ip)
        do(ip)

    # for xxxx in range(100):
    #     picurl = 'http://vote.dongyingnews.cn/api.php?action=captcha'
    #     r = requests.get(picurl)
    #     from PIL import Image
    #     from StringIO import StringIO
    #
    #     im = Image.open(StringIO(r.content))
    #     im = im.convert('L')
    #     threshold = 100
    #     table = []
    #     for i in range(256):
    #         if i < threshold:
    #             table.append(0)
    #         else:
    #             table.append(1)
    #     out = im.point(table, '1')
    #
    #     x= image_to_string(out)
    #     x=x.upper()
    #     x = x.replace('.', '').replace('"','').replace('_','').replace('‘','')\
    #         .replace("'","").replace('~','').replace(',','').replace('“','')\
    #         .replace("/",'').replace(';','').replace(' ','').replace('/?','2')
    #     x = x.replace('E', '8')
    #     x=x.replace(']','1')
    #     x=x.replace('\\','')
    #     x=x.replace('Z','2')
    #     x=x.replace('’','')
    #     x=x.replace('-','')
    #     x=x.replace('$','5')
    #     x=x.replace('"1','4')
    #     x=x.replace('A','4')
    #     x = x.replace('B', '9')
    #     x=x.replace('-I','4')
    #     x=x.replace('S','5')
    #     x=x.replace('£','2')
    #     x=x.replace('T','7')
    #     x=x.replace('!','1')
    #     x = x.replace('H', '4')
    #     x=x.replace('D','0')
    #     x=x.replace('V','1')
    #     x=x.replace('—I','4')
    #     x=x.replace('I','1')
    #     x=x.replace('U','0')
    #     print(x)
    #     try:
    #         out.save("pic/s/{0}.png".format(x))
    #     except:
    #         pass


        # image = im.convert("L")
        # twoValue(image, 100)
        # clearNoise(image,4, 1)
        #
        # saveImage(xxxx, image.size)

        # im=Image.open('pic/er{0}.png'.format(str(xxxx)))
        # image_to_string(im)
        # flagx = [0 for x in range(im.size[0])]
        # pix = im.load()
        #
        # #横坐标上的像素分布
        # for x in range(im.size[0]):
        #     for y in range(im.size[1]):
        #
        #
        #         if pix[x,y] < 90:
        #             flagx[x] += 1
        #         pass
        # #print flagx
        # img=im
        # result=[]
        # for i in range(img.size[0]):
        #     if flagx[i] > 0 and flagx[i - 1] <= 0:
        #         tmp = i  #记录0->n的坐标
        #     if flagx[i] > 0 and i+1 <img.size[0] and flagx[i + 1] <= 0:
        #         #完成一个字符的横坐标扫描，针对这段用同样的方法扫描纵坐标
        #         flagy = [0 for x in range(img.size[1])]
        #         for y in range(img.size[1]):
        #             for x in range(i + 1)[tmp:]:
        #                 if pix[x, y] < 90:
        #                     flagy[y] += 1
        #         #用flagy记录纵坐标像素分布
        #         for j in range(img.size[1]):
        #             if flagy[j] > 0 and flagy[j - 1] <= 0:
        #                 ttmp = j  #记录0->n的点
        #             if flagy[j] > 0 and j + 1 < img.size[1] and flagy[j + 1] <= 0:
        #                 result.append([tmp, i, ttmp + 1, j + 1])
        # if len(result)==4:
        #     for rr in result:
        #         print([(r )for r in rr])
        #         # temp = img.crop(rr)
        #         # #temp.show()
        #         out = img.point(rr, '1')
        #         img.save('pic/12' + str(xxxx) + '.png')
        #         text = image_to_string(out)
        #         print(text)

        # # #灰度
        # imgry = im.convert('L')
        #
        # #去噪
        # threshold = 1
        # table = []
        # for i in range(256):
        #     if i < threshold:
        #         table.append(0)
        #     else:
        #         table.append(1)
        # out = imgry.point(table, '1')
        # imgry.save('pic/' + str(xxxx) + '.png')
        # text = image_to_string(out)


