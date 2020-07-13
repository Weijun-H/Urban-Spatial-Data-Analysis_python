# 章节结构思考————不定性
书的章节结构符合人们的学习习惯会让学习的过程变的顺畅，但是在写作过程中，必然不能一步到位，而是一个不断调整、整合的过程，因此增加了这个部分，来思考这个问题。


### 知识点分布
```mermaid
classDiagram

单个分类POI数据爬取与地理空间点地图 --> 数据分析 : 
单个分类POI数据爬取与地理空间点地图 : 单个分类POI爬取
单个分类POI数据爬取与地理空间点地图 : 将csv格式的POI数据转换为pandas的DataFrame
单个分类POI数据爬取与地理空间点地图 : 将数据格式为DataFramed的POI数据转换为GeoPandas地理空间数据GeoDataFrame
单个分类POI数据爬取与地理空间点地图 : 使用plotly库建立地图

多个分类POI数据爬取与描述性统计 --|> 数据分析
多个分类POI数据爬取与描述性统计 --|> 描述性统计 : 拆分
多个分类POI数据爬取与描述性统计 : 多个分类POI爬取
多个分类POI数据爬取与描述性统计 : 批量转换.csv格式数据为GeoDataFrame

描述性统计 --|> 统计学知识点
描述性统计 : 数据种类
描述性统计 : 集中量数与变异量数
描述性统计 : 频数（次数）分布表和直方图
描述性统计 : 中位数
描述性统计 : 算数平均数
描述性统计 : 标准差
描述性统计 : 标准计分

正态分布与概率密度函数_异常值处理 --|> 统计学知识点
正态分布与概率密度函数_异常值处理 : 正态分布
正态分布与概率密度函数_异常值处理 : 概率密度函数
正态分布与概率密度函数_异常值处理 : 累积分布函数
正态分布与概率密度函数_异常值处理 : 偏度与峰度
正态分布与概率密度函数_异常值处理 : 检验数据集是否服从正态分布
正态分布与概率密度函数_异常值处理 : 异常值处理
正态分布与概率密度函数_异常值处理 : 给定特定值计算概率，以及找到给定概率的值

OSM数据处理 --|> 数据分析
OSM数据处理 : OSM原始数据处理
OSM数据处理 : 读取、转换.osm数据

核密度估计与地理空间点密度分布 --|> 数据分析
核密度估计与地理空间点密度分布 --|> 统计学知识点
核密度估计与地理空间点密度分布 : *核密度估计
核密度估计与地理空间点密度分布 : 核密度估计结果转换为地理栅格数据




```

### 知识关联
```mermaid
erDiagram
    USDAM-py ||--o{ geospatial-data : place 
    USDAM-py }|..|{ non : non
    data ||--|{ POI : Baidu
    POI ||--|{ geospatial-data : get-data
    POI ||--|{ single-classificaiton : crawler
    POI ||--|{ multiple-classificaiton : crawler
    single-classificaiton ||--|{ geospatial-data : geo
    USDAM-py }|..|{ descriptive-statistics : knowledge-point
    multiple-classificaiton ||--|| descriptive-statistics : knowledge-point
```