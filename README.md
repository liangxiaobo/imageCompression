# imageCompression 可自动压缩图片的python脚本
脚本使用Pillow处理压缩, **当前脚本只支持jpg,png格式的，后续继续完善**

脚本执行示例：
```
test.py [-i <imgs>] [-q <quality>] [-s <subsampling>] [-j <jpga>] [-d <dir>]
```
* -i，--imgs手动指定一张或多张图片压缩，以逗号分隔 a.jpg,b.jpg,c.png
* -q, --quality 默认压缩的图片质量为15，可以调整0-95
* -j, --jpga 为1时设置将图片统计转换成.jpg格式，默认为0
* -d, --dir 设置一个目录，压缩指定目录下的图片，当指定-d时，-i不生效
* -s, subsampling 设置编码器的子采样 默认-1, -1: equivalent to keep, 0: equivalent to 4:4:4, 1: equivalent to 4:2:2, 2: equivalent to 4:2:0

## Pillow
> Pillow 和 PIL 不能在同一环境中共存。在安装 Pillow 之前，请卸载PIL。
如果安装了Anaconda，Pillow就已经有了，否则就通过pip安装：

```
pip install pillow
```
操作图像
来看看最常见的图像缩放操作，只需三四行代码：
```
from PIL import Image

# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('test.jpg')
# 获得图像尺寸:
w, h = im.size
print('Original image size: %sx%s' % (w, h))
# 缩放到50%:
im.thumbnail((w//2, h//2))
print('Resize image to: %sx%s' % (w//2, h//2))
# 把缩放后的图像用jpeg格式保存:
im.save('thumbnail.jpg', 'jpeg')
```
## 命令执行

```bash
$ python imageCompression.py -h


test.py [-i <imgs>] [-q <quality>] [-s <subsampling>] [-j <jpga>] [-d <dir>]
     -i, --imgs 需要压缩的图片，多个图片以逗号分隔 "a.jpg,b.jpg
     -q, --quality 默认压缩的图片质量为15，可以调整0-95 
     -j, --jpga 为1时设置将图片统计转换成.jpg格式，默认为0 
     -d, --dir 设置一个目录，压缩指定目录下的图片 
     -s, subsampling 设置编码器的子采样 默认-1 
                     -1: equivalent to keep 
                      0: equivalent to 4:4:4 
                      1: equivalent to 4:2:2 
                      2: equivalent to 4:2:0 


命令示例：python test.py -i a.jpg,b.jpg -q 20
```

### 使用 ```-i```指定图片压缩
```bash
% python imageCompression.py -i a.jpg,image-30.png -q 30 

a.jpg 压缩前： 3.53MB 压缩后： 346KB
----------------------------------------------------------------------
image-30.png 压缩前： 2.33MB 压缩后： 326KB
----------------------------------------------------------------------
```
图片压缩完成存放在图片所在目录下的```output```目录

### 使用 ```-d```指定目录下的图片全部压缩
```bash
$ python imageCompression.py -d /Users/liangbo/Downloads/huawei_uploads/uploads/2020
image-11-1536x796.png 压缩前： 589KB 压缩后： 52KB
----------------------------------------------------------------------
image-22-1024x524.png 压缩前： 523KB 压缩后： 104KB
----------------------------------------------------------------------
image-21-1536x787.png 压缩前： 764KB 压缩后： 140KB
----------------------------------------------------------------------
image-11-2048x1062.png 压缩前： 1.05MB 压缩后： 86KB
----------------------------------------------------------------------
```
