from django.shortcuts import render, redirect, HttpResponse, render_to_response
import os
from django.conf import settings


def index(request):
    return render(request, './index.html')


def savefile(request):
    if request.method == "POST":  # 文件一定是要POST方法
        f = request.FILES['image']  # 在FILES中接收文件
        # 文件在服务器端的路径
        filepath = os.path.join(settings.MEDIA_ROOT, f.name)
        filepath2 = os.path.join(settings.BASE_DIR, f.name)
        with open(filepath, 'wb') as fp:
            for info in f.chunks():
                fp.write(info)  # chunks是以文件流的方式来接受文件，分段写入

        with open(filepath2, 'wb') as fp:
            for info in f.chunks():
                fp.write(info)  # chunks是以文件流的方式来接受文件，分段写入

        command = 'python3 ' + settings.BASE_DIR + '/sample.py --image=' + f.name  # 可以直接在命令行中执行的命令
        print(command)
        r = os.popen(command)  # 执行该命令
        info = r.readlines()  # 读取命令行的输出到一个list
        line = info[0]
        result = line.split(">")[1]
        result = result.split("<")[0]
        print(result)
        results = [""]
        image = [""]
        image[0] = f.name
        results[0] = result
        return render_to_response('./save.html', {'results': results, 'image': image})

