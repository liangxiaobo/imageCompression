import sys, getopt
from PIL import Image
from pathlib import Path
import os

g_compress_data = []

def main(argv):
    '''
    命令执行示例：python test.py -i a.jpg,b.jpg -q 20
    imgs：接收需要压缩的图片路径，a.jpg,b.jpg
    quality：默认压缩的图片质量为15，可以调整
    subsampling 子采样值 默认-1
    '''
    imgs = ''
    quality = 15
    subsampling = -1
    jpga = 0 #判断是否全部转换成jpg格式保存
    output = 'output'
    dir_files = '' # 要执行的目录，也就是图片文件存在的目标目录

    try:
        opts, args = getopt.getopt(argv, "hi:q:s:j:d:", ["imgs=", "quality=", "subsampling=", "jpga=", "dir"])
    except getopt.GetoptError:
        print('test.py -i <imgs> -q <quality> -s <subsampling> -j <jpga>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <imgs> -q <quality>  -s <subsampling>  -j <jpga> \n命令执行示例：python test.py -i a.jpg,b.jpg -q 20\nimgs：接收需要压缩的图片路径，a.jpg,b.jpg\nquality：默认压缩的图片质量为15，可以调整\nsubsampling 子采样值 默认-1')
            sys.exit()
        elif opt in ("-i", "--imgs"):
            imgs = arg
        elif opt in ("-q", "--quality"):
            quality = int(arg)
        elif opt in ("-s", "--subsampling"):
            subsampling = int(arg)
        elif opt in ("-j", "--jpga"):
            jpga = int(arg)
            print("opt_jpga: ", jpga)
        elif opt in ("-d", "--dir"):
            dir_files = arg
        
    # print('imgs:', imgs)
    # print('quality:', quality)

    
    notfound_imgs = []

    if dir_files:
        dirOfImageCompress(dir_files, quality, subsampling, notfound_imgs, jpga, output)
        return
    
    if len(imgs) > 0:
        # 创建output目录
        output_dir = Path(output)
        if output_dir.exists() == False:
            os.mkdir(output)
        for img_item in imgs.split(','):
            imageCompress(quality, subsampling, img_item, notfound_imgs, jpga, output)
    
    # TODO 向屏幕输出压缩结果信息
    # print(g_compress_data)
    if notfound_imgs:
        print('找不到的文件：', notfound_imgs)

def dirOfImageCompress(dir, quality, subsampling, notfound_imgs, jpga, output):
    '''
    当命令行中-d不为空时，表示要在指定目录里搜索图片文件进行压缩
    '''
    for dirpath, dirname, filenames in os.walk(dir):
        print('目录：', dirpath)

        if dirpath.endswith('/output') == False:
            # print('目录名：', dirname)
           
            output_dir = Path('{}/{}'.format(dirpath, output))
            if output_dir.exists() == False:
                output_dir.mkdir()

            for filename in filenames:
                # print('文件：', filename)
                if filename.endswith('.jpg') or filename.endswith('.png'):
                    imageCompress(quality, subsampling, '{}/{}'.format(dirpath, filename), notfound_imgs, jpga, output_dir)

def imageCompress(quality, subsampling, img_item, notfound_imgs, jpga, output):
    '''
    把单个文件传入此方法进行压缩
    '''
    img_item_path= ''
    img_item_path = Path(os.path.abspath(img_item))
    img_item_endswith = img_item.endswith('.png') or img_item.endswith('.jpg')

    if img_item_path.is_file() and img_item_endswith:
        # 文件存在就开始压缩
        # 压缩前的文件名
        img_file_name = img_item_path.name

        img_item_data = {'fileNameBefore': img_file_name}

        img: Image.Image = Image.open(img_item_path)
        w,h = img.size
        print('Origin image size: %sx%s' % (w, h))
        shotname = ''
        extension = ''
        (shotname, extension) = os.path.splitext(img_file_name)
        # 获取压缩前的文件byte
        byteSizeBefore = len(img.fp.read())
        img_item_data['byteSizeBefore'] = byteSizeBefore

        if byteSizeBefore < 307200:
            return

        # 区别jpg、png
        if img_item.endswith('.png'):
            if jpga > 0:
                img = img.convert('RGB')
                extension = ".jpg"
            else:
                img = img.quantize(colors=256)


        save_file = "{}/{}{}".format(output, shotname, extension)
        img_item_data['fileNameAfter'] = save_file
        img.save(save_file, quality=quality, optimize=True, subsampling=subsampling)
        img_item_data['byteSizeAfter'] = os.path.getsize(save_file)
        g_compress_data.append(img_item_data)
    else:
        # 标记不存在的文件
        notfound_imgs.append(img_item)
    
if __name__ == "__main__":
    main(sys.argv[1:])
