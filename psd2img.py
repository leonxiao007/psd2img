from psd_tools import PSDImage
from PIL import Image
import sys
import os
import shutil
import string
import time

# 全局变量
psd_file = None         # psd文件地址
psd_guide = False       # 读取过系统命令参数，进入引导系统
base_path = None        # 基础目录，基于文件保存的

# 没有导入PSD文件
while(psd_file == None):
    if len(sys.argv) == 1 or psd_guide == True:
        psd_file = input("\n请输入PSD文件地址：")
        psd_file = psd_file.strip("?")
    else:
        psd_file = sys.argv[1]
        psd_guide = True
    if os.path.exists(psd_file) == False:
        print("\nPSD文件不存在，请重试！", psd_file)
        psd_file = None
        continue
    if psd_file[-3:].lower() != "psd":
        print("\n错误的PSD文件，请重试！", psd_file[-3:].lower())
        psd_file = None

# 基础目录
psd_file = os.path.abspath(psd_file)
base_path = os.path.dirname(psd_file)
print("文件地址：", psd_file)
print("基础目录：", base_path)

# 根据时间创建文件夹
imgs_path = base_path + "/" + time.strftime("%Y%m%d %H_%M_%S", time.localtime())
if os.path.exists(imgs_path) == True: shutil.rmtree(imgs_path)
os.mkdir(imgs_path)

layerList = []
# 循环遍历图层
def getLayers(lists, path):
    for i in lists:
        #print('type:', type(i), i.is_group(), len(i));
        if i.is_group():
            #创建文件夹
            group_path = path + "/" + i.name
            if os.path.exists(group_path) == False: os.mkdir(group_path)
            for k in i:
                if k.is_group():
                    #创建文件夹
                    group_path = path + "/" + i.name + "/" + k.name
                    if os.path.exists(group_path) == False: os.mkdir(group_path)
                    getLayers(k, group_path)
                else :
                    layerList.append(k)
                    group_path = path + "/" + i.name + "/" + k.name
                    saveImg(k, group_path)
        else:
            print('i:', i)
            group_path = path + "/" + i.name
            saveImg(i, group_path)
            layerList.append(i)

# 存储图片
def saveImg(layer, path):
    img_type = "";
    # 保存为png
    if layer.name.find(".jpg")==-1:
        img_type = ".png"
    img_path = path + img_type;
    print('file path:', layer, layer.bbox, layer.name.find(".jpg")!=-1 and ".jpg" or ".png", img_path)
    # 保存图片
    if img_type == "":
        img = layer.topil()
        img.convert('RGB').save(img_path,'jpeg')
    else:
        # 合并图层和其蒙版(mask, vector mask, and clipping layers)(返回PIL.Image对象或没像素时返回`None`)
        layer.composite().save(img_path)

# 导出图片
def psd_to_img():
    # 解析PSD文件
    psd = PSDImage.open(psd_file)
    # 循环读取【组】
    for group in psd:
        # 判断该组是否有子层
        if (group.is_group() and group.is_visible()):
            # 创建组的目录
            group_path = imgs_path + "/" + group.name
            if os.path.exists(group_path) == False: os.mkdir(group_path)
            getLayers(group, group_path);
            print('layerList:', layerList)
        # 没有层
        elif group.is_visible():
            saveImg(group, imgs_path)
        else :
            print("*" * 22 + '该层隐藏了:', group.name + "*" * 22)


# 循环语句
choose = None
print("" + "=" * 50)
print("1. 导出PSD所有图片")
print("2. 生成HTML页面")
print("88. 退出程序！")
print("=" * 50)
choose = input("请选择：")
if choose == "1":
    psd_to_img()
    print("*" * 22 + "操作完成!" + "*" * 22 )
elif choose == "2":
    print('敬请期待...')
else:
    print("*" * 22 + "Thinks！" + "*" * 22 )
