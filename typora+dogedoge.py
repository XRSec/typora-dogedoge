#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import datetime, os, re, requests, sys, json, platform, tempfile, shutil, io, imghdr
requests.packages.urllib3.disable_warnings()

# 创建临时文件夹 (防止空格导致报错)
import urllib3

path_tmp = tempfile.gettempdir() + '/typora/'
# 判断结果
if not os.path.exists(path_tmp):
    os.makedirs(path_tmp)
else:
    shutil.rmtree(path_tmp)
    os.mkdir(path_tmp)


# 设置post上传接口
urls = "这里填写你的URL-API"


def upload_img():
    # 设置for 循环，防止一次性 导入 多张img 先判断有多少张图片
    for i in range(1, len(sys.argv)):
        # 先判断是否是文件会更快一点
        if os.path.isfile(sys.argv[i]):  # 判断文件是否存在，不存在则为链接
            # 老版本命名方式，根据后缀判断，容易出问题
            # new_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + os.path.splitext(sys.argv[i])[-1]  # 时间戳重命名
            new_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + "." + imghdr.what(sys.argv[i])  # 时间戳重命名
            file_path = sys.argv[int(i)]  # 设置第 i 个图片路劲
        elif "http://" or "https://" in sys.argv[i]:  # 目前不支持 ftp
            # 这里用try 是因为re.match如果匹配不到img_type 就会报错 AttributeError: 'NoneType' object has no attribute 'group'
            try:
                if re.match(r"^[\s\S]*\.(jpg|png|webp|jpeg|gif)", sys.argv[i]).group(1):
                    # 如果 文件格式匹配到了则进入下一步进行命名
                    try:
                        new_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + "." + re.match(r"^[\s\S]*\.(jpg|png|webp|jpeg|gif)", sys.argv[i]).group(1)
                        file_path = path_tmp + new_name  # 将文件保存到用户临时目录
                        with open(file_path, "wb") as temp:
                            temp.write((requests.get(sys.argv[i], timeout=5, verify=False)).content)  # 写入文件
                    # 可能上一步因为网速慢的原因导致失败，所以提示用户是否是网络问题
                    except:
                        print("network error ?")
            # 通过调用 imghdr.what 来判断在线图片是什么格式 如果报错，则提示用户是否是网络问题
            except:
                try:
                    new_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + "." + imghdr.what(None, urllib3.PoolManager().urlopen('GET', sys.argv[i]).data)
                    file_path = path_tmp + new_name  # 将文件保存到用户临时目录
                    with open(file_path, "wb") as temp:
                        temp.write((requests.get(sys.argv[i], timeout=5, verify=False)).content)  # 写入文件
                # 可能上一步因为网速慢的原因导致失败，所以提示用户是否是网络问题
                except:
                    print("network error ?")

        else:
            print("Get File/url error @ Rename and find the suffix module")
            exit()
        # print(new_name,file_path)
        # 最后输出请求结果并进行判断
        try:
            upload_result = requests.post(urls, files={'file': (new_name, open(file_path, 'rb'))}, timeout=5, verify=False)

        except:
            print('Upload img error @ Submit file module\n' + upload_result.json())

        if upload_result.json()["success"]:
            print(upload_result.json()["data"]["o_url"])
            os.remove(sys.argv[i])
            os.remove(file_path)
        else:
            print("Get upload Image/Json url error")


# 覆盖图片不支持 URL图片，只允许本地图片，尽量不要有空格 比如 C:\User\xiao ge ge\WeChat file 这种百分百报错
def cover_img():
    for i in range(1, len(sys.argv)):
        new_name = "20210905143033937071.png"
        try:
            upload_result = requests.post(urls, files={'file': (new_name, open(sys.argv[int(i)], 'rb'))}, timeout=5, verify=False)
        except:
            print('Upload img error @ Submit file module\n' + upload_result.json())

        if upload_result.json()["success"]:
            print(upload_result.json()["data"]["'o_url"])
            print(upload_result.json())
        else:
            print("Get upload Image/Json url error")


if __name__ == '__main__':
    # upload_img()
    # TODO 这里是覆盖图片的地方，如果需要则注释上面那行
    cover_img()
    exit()
