# coding = utf-8

from test_movie import data_process
from matplotlib import pyplot as plt
from matplotlib import font_manager

file_path = "./movie_information.csv"
coding = "gbk"

font = font_manager.FontProperties(fname="C:\Windows\Fonts\STLITI.TTF",size=20)
plt.figure(figsize=(20,8),dpi=80)

D = data_process.Data_renew(file_path,coding)
result = D.main()

movie_type = result.index
num = result.values

plt.bar(range(len(movie_type)),num)

plt.xticks(range(len(movie_type)),movie_type,fontproperties=font,rotation=45)
plt.yticks(range(0,max(num)+20,20))

plt.grid(alpha=0.5)

plt.savefig("./movie_graph.png")

plt.show()
