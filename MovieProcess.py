# coding = utf-8

import requests
import re

class MovieProcess():

    def __init__(self):
        self.url = 'http://58921.com/alltime/wangpiao'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.file_path = "movie_information.csv"

    # 获取网页
    def get_page(self,url):
        response = requests.get(url=url,headers=self.headers)
        response.encoding = 'UTF-8'
        return response.text

    # 获取电影名称
    def get_movie_inforamtion(self,resp):
        name = re.findall(r'<td><a href=.*? title="(.*?)">.*?</a></td>',resp)
        movie_code = re.findall(r'><td><a href="(.*?)" title=.*?>.*?</a></td>', resp)
        return name,movie_code

    # 处理信息，生成字典
    def process_movie_information(self,name,movie_code):
        info_dict = {}
        # 除去其中name获取到的空字段
        for i in name:
            if i == '':
                name.remove(i)
        for i in range(len(name)):
            info_dict[name[i]] = movie_code[i]
        return info_dict

    # 循环获得各个页面的电影名称
    def get_all_pages_info(self):
        name_code = {}
        for i in range(11):
            url_update = self.url + "?page={}".format(i)
            resp_update = self.get_page(url_update)
            name,code = self.get_movie_inforamtion(resp_update)
            name_code.update(self.process_movie_information(name,code))
        return name_code

    # 获取票房,生成字典
    def get_revenue_all(self,name_code):
        url = 'http://58921.com/'
        name_revenue = {}
        for name,code in name_code.items():
            url_update = url + "{}/boxoffice".format(code)
            resp = self.get_page(url_update)
            # 按照电影名长度加上公共字段长度，从前往后截取，除去末尾的右括号
            revenue = re.findall(r'<h3 class="panel-title">(.*?)</h3>',resp)[0][len(name)+10:-1]
            # 生成电影名与票房的字典
            name_revenue[name] = revenue
        return name_revenue

    # 获取电影类型,生成字典并输出
    def get_movie_classfication(self,name_code):
        url = 'http://58921.com/'
        name_classfication = {}
        for name,code in name_code.items():
            url_update = url + code
            resp = self.get_page(url_update)
            movie_classification = re.findall(r'<li><strong>类型：</strong>(.*?)</li>',resp)
            if movie_classification:
                result = re.findall(r'<a href=.*? title=.*?>(.*?)</a>',movie_classification[0])
                string = ""
                for i in result:
                    string += i
                    if i==result[-1]:
                        continue
                    else:
                        string += "&"
                name_classfication[name] = string
            else:
                name_classfication[name] = "无分类"

        return name_classfication

    # 生成文件
    def generate_file(self,name_revenue,name_classfication):
        with open(self.file_path, 'w+') as f:
            f.write("电影名,")
            f.write("票房,")
            f.write("电影类型")
            f.write("\n")
            for name,revenue in name_revenue.items():
                f.write(name+",")
                f.write(revenue+",")
                f.write(name_classfication[name])
                f.write("\n")


    def main_method(self):
        name_code = self.get_all_pages_info()
        name_revenue = self.get_revenue_all(name_code)
        name_classfication = self.get_movie_classfication(name_code)
        self.generate_file(name_revenue,name_classfication)



if __name__ == "__main__":
    m = MovieProcess()
    m.main_method()
