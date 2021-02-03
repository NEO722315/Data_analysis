# coding = utf-8

import numpy as np
import pandas as pd


class Data_renew():

    def __init__(self,file_path,coding):
        self.file_path = file_path
        self.coding = coding

    # 获取数据
    def extract_data(self):
        df = pd.read_csv(self.file_path,encoding=self.coding,delimiter=",")
        return df

    def classfication_statistics(self,df):
# 统计有多少种不同电影类型
        classfication = df["电影类型"]
# 取得不重复的单一数据
        classfication_result = classfication.str.split("&").tolist()
        movie_type = list(set([i for j in classfication_result for i in j]))
# 建立长为电影类型长度，宽为500部电影的为0矩阵
        zeros_matrix = pd.DataFrame(np.zeros((df.shape[0],len(movie_type))),columns=movie_type)
        return zeros_matrix,classfication_result

    def movie_type_num_statistics(self,df,zeros_matrix,classfication_result):
# 将zeros_matrix中每一行相同电影名下赋值为1
        for i in range(df.shape[0]):
            zeros_matrix.loc[i,classfication_result[i]] = 1
        result = zeros_matrix.astype("int").sum()
        return result

    def main(self):
        df = self.extract_data()
        zeros_matrix,classfication_result=self.classfication_statistics(df)
        result = self.movie_type_num_statistics(df,zeros_matrix,classfication_result)
        return result