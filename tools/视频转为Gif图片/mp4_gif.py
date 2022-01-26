from moviepy.editor import *
import os


def get_filename(path=None):
    """
    获取指定目录下的所有指定后缀的文件名
    :param path: 要查找的目录路径
    :return: 符合条件的文件列表
    """
    f_list = os.listdir(path)
    if len(f_list) == 0:
        print('没有查到符合条件的文件')
    res = []
    for i in f_list:
        # os.path.splitext(): 分离文件名与扩展名
        if os.path.splitext(i)[-1] == '.mp4':
            res.append(i)
    return res


def mp4_to_gif(filename=None, in_path='.', out_path='.', t_start=0, t_end=None):
    """
    MP4 格式文件 转成 gif
    :param t_end: 截取的结束时间点
    :param t_start: 截取的开始时间点
    :param filename: 文件列表
    :param in_path: 输入文件路径
    :param out_path: 输出文件路径
    :return: 转换后的 gif 图片
    """
    try:
        for i in filename:
            clip = (VideoFileClip(in_path + '\\' + i).subclip(t_start=t_start, t_end=t_end).resize(height=None, width=300))
            clip.write_gif(out_path + '\\' + i + '.gif')
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    file_list = get_filename(r'E:\代码\ops_tool\tools\视频转为Gif图片\视频')
    mp4_to_gif(file_list, r'E:\代码\ops_tool\tools\视频转为Gif图片\视频', r'E:\代码\ops_tool\tools\视频转为Gif图片\图片', 0, 10)
