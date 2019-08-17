# scrapy_vulns
> scrapy爬虫框架爬取某漏洞信息公开网漏洞列表  

![](https://img.shields.io/badge/language-python3.7-yellowgreen.svg?style=flat-square)
![](https://img.shields.io/badge/framework-scrapy1.7-brightgreen.svg?style=flat-square)

### 0x1 简介
项目使用python3.7开发
需要的库都列在reqirements.txt中
爬虫使用随机user-agent，禁用了原有中间件，未使用ip代理，线程较低，防止被网站封锁ip。
本项目意在学习温故scrapy爬虫框架，如有侵犯隐私、公共安全的隐患请联系本人，将立即删除。

### 0x2 如何配置 
- 文件目录  

scarpy_vulns  
│  scrapy.cfg  
│  
└─scarpy_vulns  
    │  items.py   # 定义持久化的实体  
    │  middlewares.py   # 中间件  
    │  pipelines.py    # 持久化管道  
    │  settings.py  # 配置文件  
    │  start.py     # 快捷启动方式：python ./start,py  
    │  __init__.py  
    │  
    ├─spiders  
        │   src.py   # 爬虫  
        │  __init__.py  
  
- 只需要做以下配置
1. settings.py中数据库配置
2. settings.py中CONCURRENT_REQUESTS和DOWNLOAD_DELAY（保持默认也可以）
3. mysql数据库中建立一个名为scrapy_vulns数据库并在其中建立一个名为list的表，表中字段如下定义：
> CREATE TABLE `list` (
  `time` date NOT NULL,
  `title` varchar(255) NOT NULL,
  `rank` varchar(16) NOT NULL,
  `author` varchar(127) NOT NULL,
  `organization` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`time`,`title`,`author`,`rank`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;  
	# 相信懂一点sql的都能看懂  

注：如果另起库名和表名需要对应修改该settings.py和pipelines.py中的对应参数MYSQL_DB和self.cursor.execute中的list
4. 如果你的系统python环境由于缺少库环境启动爬虫失败，或者不想扰乱本地环境，可以为项目搭建虚拟环境。**具体方法请参见：本人cyblog的部署文档/另行百度**

### 0x3 如何启动
以下方法任选其一
- 克隆项目进入项目目录，再进入一层scrapy_vulns目录，能看到start.py
`python start.py`
- 或者再进入spider目录使用以下命令
`scrapy crawl src`
