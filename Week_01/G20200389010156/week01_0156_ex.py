import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import time


# 自定义函数：db_http
def db_http(url):
    # 伪装浏览器 header
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    header = {}
    header['user-agent'] = user_agent
    # 抓取页面
    response = requests.get(url, headers = header)
    # 使用 bs4 解析 html
    return bs(response.text, 'html.parser')


# CSV 文件路径
csv_path = './douban.csv'

# 初始化一个空 CSV 文件
csv_header = ['电影名', '评分', '评论数', '评论(Top5)']
df_init = pd.DataFrame(columns = csv_header)
df_init.to_csv(csv_path, index = False)

# 生成包含所有页面的元组
moive_pages = tuple(f'https://movie.douban.com/top250?start={page * 25}' for page in range(10))
for page_url in moive_pages:
    # 爬取电影列表页***
    page = db_http(page_url)
    moive_pic = page.find_all('div', attrs={'class': 'pic'})
    # 遍历电影缩略图区块
    for moive_item in moive_pic:
        # 初始化list
        douban_movie = []
        # 电影链接地址
        movie_page_href = moive_item.find('a')['href']
        # 电影名称
        movie_title = moive_item.find('img')['alt']
        # 输出进度
        print('正在爬取:', movie_title, '=>', movie_page_href)
        # 爬取电影详情页***
        movie = db_http(movie_page_href)
        # 豆瓣分数
        movie_average = movie.find('strong', attrs={'property': 'v:average'}).text
        # 评论数量
        movie_votes = movie.find('span', attrs={'property': 'v:votes'}).text
        # 爬取电影评论页***
        comments = db_http(movie_page_href + 'comments?sort=new_score&status=P')
        comment_span = comments.find_all('span', attrs={'class': 'short'})
        # 遍历前五条热评
        five_comments = []
        for comment in comment_span[0:5]:
            five_comments.append(comment.text.strip())
        # 评论TOP5 格式化数据=>json
        comments_json = json.dumps(five_comments, ensure_ascii = False)
        # 整理数据
        douban_movie.append([movie_title, movie_average, movie_votes, comments_json])
        # 逐条写入数据
        douban_movie_df = pd.DataFrame(data = douban_movie)
        douban_movie_df.to_csv(csv_path, mode = 'a', header = False, index = False, encoding = 'utf-8-sig')

        # 暂停 n 秒再爬取,防止屏蔽 IP
        time.sleep(8)

print('Over ~')
