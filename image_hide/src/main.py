"""
基于函数的图片信息隐藏
"""
import math
import cv2
import binascii
import re
import os


class ImageSteganography():
    def __init__(self):
        self.author = 'boblee'
        self.a = 100

    def cut_text(self, text, lenth):
        """
        字符串等分，每lenth一组
        :param text: 字符串
        :param lenth: 等分数
        :return:
        """
        textArr = re.findall('.{' + str(lenth) + '}', text)
        textArr.append(text[(len(textArr) * lenth):])
        return textArr

    def heart_function(self, x, y, a):
        """
        心形函数，用于获取藏数据的位置
        :param x: 坐标x
        :param y: 坐标y
        :param a: 参数a
        :return: 数据位置
        """
        result = pow(x, 2) + pow(y, 2) + a * x - a * math.sqrt(pow(x, 2) + pow(y, 2))
        if int(result) > 10 and int(result) < 1000:
            return 0
        else:
            return 1

    def str_to_ten(self, string):
        """
        字符串转10进制
        :param string: 字符串
        :return: 10近制
        """
        return int(binascii.hexlify(bytes(string, encoding='utf-8')), 16)

    def number_encode(self, data, number):
        """
        图像像素值藏信息，更改二进制像素末三位
        :param data: 原像素值
        :param number: 需要藏得信息
        :return: 更改后得像素值
        """
        data_two = str(bin(data)).replace('0b', '')[:-4]
        number_two = str(bin(number)).replace('0b', '').rjust(4, '0')
        result_two = int('0b' + data_two + number_two, 2)
        return result_two

    def number_decode(self, number):
        """
        获取像素值中隐藏得信息
        :param number: 像素值
        :return: 隐藏得信息
        """
        data_two = str(bin(number)).replace('0b', '')[-4:]
        return int('0b' + data_two, 2)

    def ten_to_str(self, int_ten):
        """
        10进制转字符串
        :param int_ten: 10进制
        :return: 字符串
        """
        return binascii.unhexlify(hex(int_ten)[2:]).decode('utf-8')

    def image_encode(self, string,image_path, save_path):
        """
        图像隐藏信息主函数
        :param image_path: 图像路径
        :param string: 待隐藏的字符串
        :param save_path: 图像最终保存路径
        :return: 结果
        """
        image = cv2.imread(image_path)
        _, name = os.path.split(image_path)
        w, h, dim = image.shape
        string_all = str(len(str(self.str_to_ten(string)))).rjust(3, '0') + str(self.str_to_ten(string))
        string_encode = self.cut_text(string_all, 3)
        print('字符编码成功')
        data_location = []
        count = 0
        for i in range(w):
            for j in range(h):
                result = self.heart_function(i, j, self.a)
                if result == 0:
                    data_location.append([i, j])
                    count = count + 1
                if count == len(string_encode):
                    break
        print('获取图像像素位置成功')
        for i in range(len(string_encode)):
            for j in range(len(string_encode[i])):
                temp = image[data_location[i][0]][data_location[i][1]][j]
                data_new = self.number_encode(temp, int(string_encode[i][j]))
                image[data_location[i][0]][data_location[i][1]][j] = data_new
        cv2.imwrite(save_path + name, image)
        print('图片隐写成功')

    def image_decode(self, save_path):
        """
        图像隐藏信息提取主函数
        :param save_path: 含有信息的图片
        :return: 结果信息
        """
        image = cv2.imread(save_path)
        w, h, dim = image.shape
        data_location = []
        for i in range(w):
            for j in range(h):
                result = self.heart_function(i, j, self.a)
                if result == 0:
                    data_location.append([i, j])
        print('获取图像像素位置成功')
        information_ten = []
        for element in data_location:
            for j in range(3):
                information_ten.append(image[element[0]][element[1]][j])
        string_len = ''
        for i in range(3):
            string_len = string_len + str(self.number_decode(information_ten[i]))
        information_ten = information_ten[3:]
        string_all = ''
        for i in range(int(string_len)):
            string_all = string_all + str(self.number_decode(information_ten[i]))
        string = self.ten_to_str(int(string_all))
        print('获取字符串转码成功')
        return string


if __name__ == '__main__':
    data = ImageSteganography()
    data.image_encode('明晚3点老地方见', '../image/1.png', '../image_hide/')
    print('隐藏字符是：'+data.image_decode('../image_hide/1.png'))
