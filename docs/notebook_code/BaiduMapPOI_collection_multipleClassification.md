> Created on Thu Nov 16 12/12/38 2017  @author: Richie Bao-caDesign设计(cadesign.cn)
> __+updated on Fri Jun 26 11/02/19 2020 by Richie Bao
## 1. 多个分类POI数据爬取与描述性统计
[JupterLab .ipynb文件下载位置](https://github.com/richieBao/Urban-Spatial-Data-Analysis_python/tree/master/notebook/BaiduMapPOIcollection_ipynb)

### 1.1 多个分类POI爬取
在上一章节新建立有两个函数工具，分别是‘百度地图开放平台POI数据爬取’和‘转换.csv格式的POI数据为pandas的DataFrame’。为了能够方便应用所建立的函数工具，使用Anaconda的Spyder创建一个新的文件为util_poi.py，将上述两个函数置于其中，同时包括函数所使用的库。对于所包括的库，为方便日后函数迁移，以及明确每个函数所调用的库，将对应调用库的语句分别置于各个函数内部。util_poi.py与待调用该文件的文件于同一文件夹下。util_poi.py文件可从本书GitHub仓库中下载。调入语句如下：

```python
import util_poi
```

根据百度地图一级行业分类，建立映射字典，用于多个分类POI的数据爬取。注意，可以根据数据的需求选择行业分类，在进一步分析中不需要的分类包括出入口、自然地物、行政地标和门址，因此在映射字典中未包含上述分类。

```python
poi_classificationName={
        "美食 ":"delicacy",
        "酒店 ":"hotel",
        "购物 ":"shopping",
        "生活服务":"lifeService",
        "丽人 ":"beauty",
        "旅游景点":"spot",
        "休闲娱乐":"entertainment",
        "运动健身":"sports",
        "教育培训":"education",
        "文化传媒":"media",
        "医疗 ":"medicalTreatment",
        "汽车服务":"carService",
        "交通设施":"trafficFacilities",
        "金融":"finance",
        "房地产":"realEstate",
        "公司企业":"corporation",
        "政府机构":"government"
        }
```

配置基本参数。注意在配置上一章节时用到`query_dic`，此次批量下载将所有参数在循环函数外字典形式单独给出，方便调用。而`query_dic`字典参数在批量下载函数内配置。

该部分代码仅是用于说明上一章节参数配置形式，本次无需敲入。
query_dic={
    'query':'旅游景点',
    'page_size':'20',
    'scope':2,
    'ak':'uqRcWhrQ6h0pAaSdxYn73GMWgd5uNrRX',
}


```python
poi_config_para={
    'data_path':'./data/poi_batchCrawler/', #配置数据存储位置
    'bound_coordinate':{'leftBottom':[108.776852,34.186027],'rightTop':[109.129275,34.382171]}, #百度地图坐标拾取系统 http://api.map.baidu.com/lbsapi/getpoint/index.html
    'page_num_range':range(20),
    'partition':3, #3
    'page_size':'20', #20
    'scope':2,
    'ak':'uqRcWhrQ6h0pAaSdxYn73GMWgd5uNrRX',
}
```

建立批量下载的循环函数，依据给出的`poi_classificationName`字典键值逐次调用单个分类POI爬取函数下载POI数据。在爬取的过程中，可以将每一次小批量下载数据存储在同一变量下，待全部下载完后一次性存储。但是这种一次性存储的方式并不推荐，其一，网络有时并不稳定，可能造成下载中断，那么已下载的数据未得以存储，造成数据丢失和不必要的重复下载；其二，有时数据量很大，如果都存储在一个变量下，可能造成内存溢出。

```python
def baiduPOI_batchCrawler(poi_config_para):
    import os
    import util_poi
    '''function-百度地图开放平台POI数据批量爬取，需要调用单个分类POI爬取函数baiduPOI_dataCrawler(query_dic,bound_coordinate,partition,page_num_range,poi_fn_list=False)'''
    for idx,(poi_ClassiName,poi_classMapping) in enumerate(poi_classificationName.items()):
        print(str(idx)+"_"+poi_ClassiName)
        poi_subFileName="poi_"+str(idx)+"_"+poi_classMapping
        data_path=poi_config_para['data_path']
        poi_fn_csv=os.path.join(data_path,poi_subFileName+'.csv')
        poi_fn_json=os.path.join(data_path,poi_subFileName+'.json')
        
        query_dic={
            'query':poi_ClassiName,
            'page_size':poi_config_para['page_size'],
            'scope':poi_config_para['scope'],
            'ak':poi_config_para['ak']                        
        }
        bound_coordinate=poi_config_para['bound_coordinate']
        partition=poi_config_para['partition']
        page_num_range=poi_config_para['page_num_range']
        #调用单个分类POI爬取函数
        util_poi.baiduPOI_dataCrawler(query_dic,bound_coordinate,partition,page_num_range,poi_fn_list=[poi_fn_csv,poi_fn_json])  
        
baiduPOI_batchCrawler(poi_config_para)
```

```
Start downloading data...
No.1 was written to the .csv file.
No.2 was written to the .csv file.
No.3 was written to the .csv file.
No.4 was written to the .csv file.
No.5 was written to the .csv file.
No.6 was written to the .csv file.
No.7 was written to the .csv file.
No.8 was written to the .csv file.
No.9 was written to the .csv file.
The download is complete.
0_美食 
Start downloading data...
No.1 was written to the .csv file.
No.2 was written to the .csv file.
No.3 was written to the .csv file.
No.4 was written to the .csv file.
No.5 was written to the .csv file.
No.6 was written to the .csv file.
No.7 was written to the .csv file.
No.8 was written to the .csv file.
No.9 was written to the .csv file.
The download is complete.
1_酒店 
Start downloading data...
No.1 was written to the .csv file.
No.2 was written to the .csv file.
No.3 was written to the .csv file.
No.4 was written to the .csv file.
No.5 was written to the .csv file.
No.6 was written to the .csv file.
No.7 was written to the .csv file.
No.8 was written to the .csv file.
No.9 was written to the .csv file.
The download is complete.
2_购物 
Start downloading data...
No.1 was written to the .csv file.
No.2 was written to the .csv file.
No.3 was written to the .csv file.
```

### 1.2 批量转换.csv格式数据为GeoDataFrame
在单个分类实现部分我们是逐步实现.csv格式数据到GeoDataFrame数据的转换，基于已有代码，在该部分将实现两个目的，一个是定义单独函数实现.csv批量转换为GeoDataFame格式数据并存储为.pkl文件；二是批量读取存储为.pkl文件的GeoDataFrame格式数据，并根据需要提取信息存储在单一变量下并再存储为.pkl文件。需要注意，当读取所有数据于单一变量时，内存需要满足要求，如果有内存溢出，则需要考虑是否根据内存情况调整每次读取的数据数量。
#### 1.2.1 定义提取文件夹下所有文件路径的函数
因为批量下载POI数据为多个.csv文件及.json文件，因此在批量处理这些数据时，第一件事情是要提取所有文件的路径。定义返回所有指定后缀名的文件路径的函数是最为常用的函数之一，在之后的很多实验中，都需要调用该函数，因此可以将其同样保存在util_poi.py文件中，方便日后调用。同时需要注意，文件夹下通常包括子文件夹，需要`os.walk()`遍历目录,并给出条件语句判断是否存在子文件夹，如果存在则需要返回该文件夹下的文件路径。

```python
def filePath_extraction(dirpath,fileType):
    import os
    '''funciton-以所在文件夹路径为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
    filePath_Info={}
    i=0
    for dirpath,dirNames,fileNames in os.walk(dirpath): #os.walk()遍历目录，使用help(os.walk)查看返回值解释
       i+=1
       if fileNames: #仅当文件夹中有文件时才提取
           tempList=[f for f in fileNames if f.split('.')[-1] in fileType]
           if tempList: #剔除文件名列表为空的情况,即文件夹下存在不为指定文件类型的文件时，上一步列表会返回空列表[]
               filePath_Info.setdefault(dirpath,tempList)
    return filePath_Info

dirpath='./data/poi_batchCrawler/'
fileType=["csv"]
poi_paths=filePath_extraction(dirpath,fileType)
print(poi_paths)
```

```
{'./data/poi_batchCrawler/': ['poi_0_delicacy.csv', 'poi_10_medicalTreatment.csv', 'poi_11_carService.csv', 'poi_12_trafficFacilities.csv', 'poi_13_finance.csv', 'poi_14_realEstate.csv', 'poi_15_corporation.csv', 'poi_16_government.csv', 'poi_1_hotel.csv', 'poi_2_shopping.csv', 'poi_3_lifeService.csv', 'poi_4_beauty.csv', 'poi_5_spot.csv', 'poi_6_entertainment.csv', 'poi_7_sports.csv', 'poi_8_education.csv', 'poi_9_media.csv']}
```

#### 1.2.2 .csv格式POI数据批量转换为GeoDataFrame
```
Index(['address', 'area', 'city', 'detail', 'detail_info_checkin_num','detail_info_children', 'detail_info_comment_num',
       'detail_info_detail_url', 'detail_info_facility_rating','detail_info_favorite_num', 'detail_info_hygiene_rating',
       'detail_info_image_num', 'detail_info_indoor_floor','detail_info_navi_location_lat', 'detail_info_navi_location_lng',
       'detail_info_overall_rating', 'detail_info_price','detail_info_service_rating', 'detail_info_tag', 'detail_info_type',
       'location_lat', 'location_lng', 'name', 'province', 'street_id','telephone', 'uid'],dtype='object')
```
上述为POI数据字段，可以根据其来确定提取的字段名。除了增加循环语句循环POI的.csv文件逐一转换为pandas的DataFrame格式，再进一步转换为geopandas的GeoDataFrame格式之外，其它的条件同上一章节。直接GeoDataFrame.plot()方式初步查看地理空间信息数据。在文件保存部分，可以有多种保存格式，GeoPandas提供了Shapefile、GeoJSON和GeoPackage三种方式，以及pickle。GeoPandas提供的保存格式再读取后不再包含多重索引，而pickle格式则保持。转换为.shp格式文件时，在QGIS等桌面GIS平台下打开时会出现两个问题，一个是如果列名称过长，转化为属性表的字段名会被字段压缩修改，往往不能反映字段的意义，因此需要置换列名称；二是用POI的一级行业分类名作为index时，列中并不包含该字段，转化为Shapefile文件时也不包含该字段，因此需要将index转换为列，再存储为.shp文件。


```python
fields_extraction=['name','location_lat', 'location_lng','detail_info_tag','detail_info_overall_rating', 'detail_info_price'] #配置需要提取的字段，即列（columns）
save_path={'geojson':'./data/poiAll_gpd.geojson','shp':'./data/poiAll_gpd.shp','pkl':'./data/poiAll_gpd.pkl'} #分别存储为GeoJSON、Shapefile和pickle三种数据格式
def poi_csv2GeoDF_batch(poi_paths,fields_extraction,save_path):
    import os,pathlib
    import util_poi
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point
    '''funciton-.csv格式POI数据批量转换为GeoDataFrame，需要调用转换.csv格式的POI数据为pandas的DataFrame函数csv2df(poi_fn_csv)'''
    #循环读取与转换poi的.csv文件为pandas的DataFrame数据格式
    poi_df_dic={}
    i=0
    for key in poi_paths:
        for val in poi_paths[key]:
            poi_csvPath=os.path.join(key,val)
            poi_df=util_poi.csv2df(poi_csvPath) #注释掉了了csv2df()函数内部的print("%s data type is not converted..."%(col))语句，以pass替代，减少提示内容，避免干扰
            print(val)
            poi_df_path=pathlib.Path(val)
            poi_df_dic[poi_df_path.stem]=poi_df
            
            #if i==2:break
            i+=1
    poi_df_concat=pd.concat(poi_df_dic.values(),keys=poi_df_dic.keys(),sort=True)
    #print(poi_df_concat.loc[['poi_0_delicacy'],:]) #提取index为 'poi_0_delicacy'的行，验证结果
    poi_fieldsExtraction=poi_df_concat.loc[:,fields_extraction]
    poi_geoDF=poi_fieldsExtraction.copy(deep=True)
    poi_geoDF['geometry']=poi_geoDF.apply(lambda row:Point(row.location_lng,row.location_lat),axis=1) 
    crs={'init': 'epsg:4326'} #配置坐标系统，参考：https://spatialreference.org/        
    poiAll_gpd=gpd.GeoDataFrame(poi_geoDF,crs=crs)
    
    poiAll_gpd.to_pickle(save_path['pkl'])
    poiAll_gpd.to_file(save_path['geojson'],driver='GeoJSON')
    
    poiAll_gpd2shp=poiAll_gpd.reset_index() #不指定level参数，例如Level=0，会把多重索引中的所有索引转换为列
    poiAll_gpd2shp.rename(columns={
        'location_lat':'lat', 'location_lng':'lng',
        'detail_info_tag':'tag','detail_info_overall_rating':'rating', 'detail_info_price':'price'},inplace=True)
    poiAll_gpd2shp.to_file(save_path['shp'],encoding='utf-8')
        
    return poiAll_gpd
            
poi_gpd=poi_csv2GeoDF_batch(poi_paths,fields_extraction,save_path)
poi_gpd.loc[['poi_0_delicacy'],:].plot(column='detail_info_overall_rating') #提取index为'poi_0_delicacy'的行查看结果
```

```
__________________________________________________
.csv to DataFrame is completed!
poi_0_delicacy.csv
__________________________________________________
.csv to DataFrame is completed!
poi_10_medicalTreatment.csv
__________________________________________________
.csv to DataFrame is completed!
poi_11_carService.csv
__________________________________________________
.csv to DataFrame is completed!
poi_12_trafficFacilities.csv
__________________________________________________
.csv to DataFrame is completed!
poi_13_finance.csv
__________________________________________________
.csv to DataFrame is completed!
poi_14_realEstate.csv
__________________________________________________
.csv to DataFrame is completed!
poi_15_corporation.csv
__________________________________________________
.csv to DataFrame is completed!
poi_16_government.csv
__________________________________________________
```

<a href="https://jupyter.org/"><img src="./imgs/2_1.png" height="auto" width="auto" title="caDesign"/></a>

> 在[QGIS开源桌面GIS平台](https://www.qgis.org/en/site/index.html)下打开保存的.shp数据。虽然我们的所有工作基本都是在python中完成，但是有些工作与其它平台相互联系，需要以这些平台为辅助。在辅助平台选择上，我们尽可能使用具有广泛应用的开源软件。在地理信息系统（GIS，Geographic Information Systems）中主要使用的集成式平台有QGIS和ArcGIS。

<a href=""><img src="./imgs/2_2.jpg" height="auto" width="auto" title="caDesign"/>

### 1.3 使用plotly库建立地图
用颜色表示POI一级分类，用大小表示rating字段。

```python
import geopandas as gpd
poi_gpd=gpd.read_file('./data/poiAll_gpd.shp') #读取存储的.shp格式文件

import plotly.express as px
poi_gpd.rating=poi_gpd.rating.fillna(0) #pandas库的方法同样适用于geopandas库，例如对`nan`位置填充指定数值
mapbox_token='pk.eyJ1IjoicmljaGllYmFvIiwiYSI6ImNrYjB3N2NyMzBlMG8yc254dTRzNnMyeHMifQ.QT7MdjQKs9Y6OtaJaJAn0A'
px.set_mapbox_access_token(mapbox_token)
fig=px.scatter_mapbox(poi_gpd,lat=poi_gpd.lat, lon=poi_gpd.lng,color="level_0",size='rating',color_continuous_scale=px.colors.cyclical.IceFire, size_max=10, zoom=10) #亦可以选择列，通过size=""配置增加显示信息
fig.show()
```

<a href=""><img src="./imgs/2_3.jpg" height="auto" width="auto" title="caDesign"/></a>

### 1.4 描述性统计图表
#### 1.4.1 读取数据与查看
* 读取已经保存的.pkl数据。通过.plot()确认读取的数据是否正常，或者直接`poi_gpd.head()`查看数据。

```python
import pandas as pd
poi_gpd=pd.read_pickle('./data/poiAll_gpd.pkl')
poi_gpd.plot(marker=".",markersize=5,column='detail_info_overall_rating') #只有不设置columns参数时，可以使用color='green'参数
print(poi_gpd.columns) #查看列名称
```

```
Index(['name', 'location_lat', 'location_lng', 'detail_info_tag',
       'detail_info_overall_rating', 'detail_info_price', 'geometry'],
      dtype='object')
```

<a href=""><img src="./imgs/2_4.png" height="auto" width="auto" title="caDesign"/></a>

#### 1.4.2 用plotly表格显示DataFrame数据

print()是查看数据最为主要的方式，主要用于代码调试。当需要展示数据时，对于DataFrame格式的数据可以直接使用plotly转换为表格形式，因为POI数据有万行之多，仅显示每一一级行业分类(含17类)的前两行的内容，总共$2\times17=34$行。为方便调用，将其功能定义为一个函数。提取数据时，因为数据格式是多重索引DataFrame，因此使用pandas.IndexSlice()函数辅助执行多重索引切分。同时用plotly显示表格时，如果时多重索引则会显示错误，因此需要df.reset_index()重置索引。plotly也不能够显示'geometry'几何对象，在列提取时需要移除该列。

```python
df=poi_gpd.loc[pd.IndexSlice[:,:2],:]
df=df.reset_index()
column_extraction=['level_0','name', 'location_lat', 'location_lng', 'detail_info_tag','detail_info_overall_rating', 'detail_info_price']

def ployly_table(df,column_extraction):
    import plotly.graph_objects as go
    import pandas as pd
    '''funciton-使用plotly以表格形式显示DataFrame格式数据'''
    fig = go.Figure(data=[go.Table(
        header=dict(values=column_extraction,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=df[column_extraction].values.T.tolist(), #values参数的值为按列的嵌套列表，因此需要使用参数.T反转数组
                   fill_color='lavender',
                   align='left'))
    ])
    fig.show()    
ployly_table(df,column_extraction)
```

<a href=""><img src="./imgs/2_5.jpg" height="auto" width="auto" title="caDesign"/></a>

#### 1.4.3 描述性统计

> 参考 (日)高桥 信著,株式会社TREND-PRO漫画制作，陈刚译.漫画统计学[M].科学出版社.北京.  以及维基百科（Wikipedia）。枯燥的知识以漫画的方式讲出来，并结合实际的案例由简入繁使枯燥的学习变得有趣起来，欧姆社学习漫画系列和众多以漫画和图示的方式讲解知识的优秀图书都值得推荐。但是有利有弊，大部分的漫画图书往往以基础知识为主，深入的研究还是要搜索科学文献和相关论著。同时漫画形式可以引起读者的兴趣，但是因为穿插故事情节，知识点不易定位，核心的知识内容相对分散，阅读上也要花费更多的时间。因此想学习一门知识，想以哪种形式入手，需要根据个人的情况确定。

描述性统计分析是对调查总体所有变量的有关数据做统计性描述，了解各变量内的观察值集中与分散的情况。

-表示集中趋势（集中量数）的有平均数、中位数、众数、几何平均数、调和平均数等；表示离散程度（变异量数）的有极差（全距）、平均差、标准差、相对差、四分差等。数据的次数分配情况，往往会呈现正态分布。

-数据的频数（次数）分配情况，往往会呈现正态分布。为了表示测量数据与正态分布偏离的情况，会使用偏度、峰度这两种统计数据。

-为了解个别观察值在整体中所占的位置，会需要将观察值转换为相对量数，如百分等级、标准分数、四分位数等。

通常在描述性统计中将数据图表化，以直观的方式了解整体资料分布的情况，包括直方图、散点图、饼图、折现图、箱型图等。


##### 1. 数据种类
通常数据可以分为两类，不可测量的数据称为分类数据；可测量的数据称为数值数据。上述图表中'level_0', 'detail_info_tag'字段均为分类数据，'location_lat', 'location_lng','detail_info_overall_rating', 'detail_info_price'均为数值数据。而'name'字段则是数据的索引名称。

##### 2. 数值数据的描述性统计

###### 频数（次数）分布表和直方图

🍅 建立简单数据示例，数据来源于《漫画统计学》'美味拉面畅销前50'上刊载的拉面馆的拉面价格。虽然一组数据通常使用pandas.Series()建立Series格式数据，但是后续分析会加入新的数据，因此仍旧建立DataFrame格式数据。使用df.describe()可以粗略查看主要统计值。

```python
ranmen_price=pd.DataFrame([700,850,600,650,980,750,500,890,880,700,890,720,680,650,790,670,680,900,880,720,850,700,780,850,750,
                           780,590,650,580,750,800,550,750,700,600,800,800,880,790,790,780,600,690,680,650,890,930,650,777,700],columns=["price"])
print(ranmen_price.describe())
```

```

            price
count   50.000000
mean   743.340000
std    108.261891
min    500.000000
25%    672.500000
50%    750.000000
75%    800.000000
max    980.000000
```

因为有些价格是相同的，一般可以直接使用上述ranmen_price数据直接计算频数，但是很多时候相同的数据并不多，而且希望分析内容为数值区段间的比较，分析才更具有意义，因此转换为相对量数，以100间隔为一级。范围根据数据的最大和最小值来确定。

```python
bins=range(500,1000+100,100) #配置分割区间（组距）
ranmen_price['price_bins']=pd.cut(x=ranmen_price.price,bins=bins,right=False) #参数right=False指定为包含左边值，不包括右边值。
ranmenPrice_bins=ranmen_price.sort_values(by=['price']) #按照分割区间排序
ranmenPrice_bins.set_index(['price_bins',ranmenPrice_bins.index],drop=False,inplace=True) #以price_bins和原索引值设置多重索引，同时配置drop=False参数保留原列。
print(ranmen_price.head(10))
```

```
   price   price_bins
0    700   [700, 800)
1    850   [800, 900)
2    600   [600, 700)
3    650   [600, 700)
4    980  [900, 1000)
5    750   [700, 800)
6    500   [500, 600)
7    890   [800, 900)
8    880   [800, 900)
9    700   [700, 800)
```

频数计算

```python
ranmenPriceBins_frequency=ranmenPrice_bins.price_bins.value_counts() #dropna=False  
ranmenPriceBins_relativeFrequency=ranmenPrice_bins.price_bins.value_counts(normalize=True) #参数normalize=True将计算相对频数(次数) dividing all values by the sum of values
ranmenPriceBins_freqANDrelFreq=pd.DataFrame({'fre':ranmenPriceBins_frequency,'relFre':ranmenPriceBins_relativeFrequency})
print(ranmenPriceBins_freqANDrelFreq)
```

```
             fre  relFre
[700, 800)    18    0.36
[600, 700)    13    0.26
[800, 900)    12    0.24
[500, 600)     4    0.08
[900, 1000)    3    0.06
```

组中值计算

```python
ranmenPriceBins_median=ranmenPrice_bins.median(level=0)
ranmenPriceBins_median.rename(columns={'price':'median'},inplace=True)
print(ranmenPriceBins_median)
```

```
             median
price_bins         
[500, 600)      565
[600, 700)      650
[700, 800)      750
[800, 900)      865
[900, 1000)     930
```


合并分割区间、频数计算和组中值的DataFrame格式数据。

```python
ranmen_fre=ranmenPriceBins_freqANDrelFreq.join(ranmenPriceBins_median).sort_index().reset_index() #在合并时会自动匹配index
print(ranmen_fre)
```

```
         index  fre  relFre  median
0   [500, 600)    4    0.08     565
1   [600, 700)   13    0.26     650
2   [700, 800)   18    0.36     750
3   [800, 900)   12    0.24     865
4  [900, 1000)    3    0.06     930
```

计算频数比例，即各个区间频数占总数的百分比，能够更清晰比较之间的差异大小。配合使用df.apply()和lambda匿名函数，这两个方法经常被用到，能够巧妙的以一种简洁的方式解决相关问题。

```python
ranmen_fre['fre_percent%']=ranmen_fre.apply(lambda row:row['fre']/ranmen_fre.fre.sum()*100,axis=1)
print(ranmen_fre)
```

```
         index  fre  relFre  median  fre_percent  fre_percent%
0   [500, 600)    4    0.08     565          8.0           8.0
1   [600, 700)   13    0.26     650         26.0          26.0
2   [700, 800)   18    0.36     750         36.0          36.0
3   [800, 900)   12    0.24     865         24.0          24.0
4  [900, 1000)    3    0.06     930          6.0           6.0
```


直方图（pandas） pandas自身就带有不少图表打印的功能（基于Matplotlib库），可以迅速的预览，而不必要过多的调整数据结构。但是不像plotly具有交互功能。

```python
ranmen_fre.loc[:,['fre','index']].plot.bar(x='index',rot=0,figsize=(5,5))
```

<a href=""><img src="./imgs/2_6.png" height="auto" width="auto" title="caDesign"/></a>

🐨有了上述简单数据的示例，再返回到POI实验数据，就可以直接迁移上述代码，略作调整后分析POI一级分类美食'poi_0_delicacy'的价格总体分布情况。将上述的所有分析代码放置于一个函数中，函数的主要功能就是计算DataFrame数据格式下，指定组距，一列数据的频数分布。将上述零散的代码纳入到一个函数中，需要注意几点事宜，一个是尽可能让变量名具有普适性，例如原变量名ranmenPrice_bins在函数中更改为df_bins，因为该函数同样可以计算'detail_info_overall_rating'字段的频数分布情况；二是公用的常用变量尽量开始配置，例如column_name和column_bins_name，这样避免不断的用原始的语句，例如重复使用`df.columns[0]+'_bins'`，从而导致代码可读性较差；再者，基本不可能直接迁移上述代码于函数中使用，需要逐句或者逐段的迁移测试，例如原代码`ranmenPrice_bins.price_bins`，在函数中改为df_bins[column_bins_name]，因为列名是以变量名形式存储，无法直接用`.`的方式读取数据。最后是需要注意函数返回值的灵活性，例如并未在函数内部定义图表打印，而是返回DataFrame格式的数据，因为打印的方式比较多样化，可以仅打印一列数据的柱状图，或者多列，以及图表的形式也会多样化，因此这部分工作放置于函数外处理，增加灵活性。

```python
delicacy_price=poi_gpd.xs('poi_0_delicacy',level=0).detail_info_price #由多重索引提取美食一级分类，并进而提取价格列数据
delicacy_price_df=delicacy_price.to_frame(name='price')
print(delicacy_price_df.describe())
```

```
            price
count  785.000000
mean    53.584076
std     44.123529
min      5.000000
25%     23.000000
50%     43.000000
75%     72.000000
max    571.000000
```

```python
def frequency_bins(df,bins):
    import pandas as pd
    '''function-频数分布计算'''
    
    #A-组织数据
    column_name=df.columns[0]
    column_bins_name=df.columns[0]+'_bins'
    df[column_bins_name]=pd.cut(x=df[column_name],bins=bins,right=False) #参数right=False指定为包含左边值，不包括右边值。
    df_bins=df.sort_values(by=[column_name]) #按照分割区间排序
    df_bins.set_index([column_bins_name,df_bins.index],drop=False,inplace=True) #以price_bins和原索引值设置多重索引，同时配置drop=False参数保留原列。
    #print(df_bins.head(10))
    
    #B-频数计算
    dfBins_frequency=df_bins[column_bins_name].value_counts() #dropna=False  
    dfBins_relativeFrequency=df_bins[column_bins_name].value_counts(normalize=True) #参数normalize=True将计算相对频数(次数) dividing all values by the sum of values
    dfBins_freqANDrelFreq=pd.DataFrame({'fre':dfBins_frequency,'relFre':dfBins_relativeFrequency})
    #print(dfBins_freqANDrelFreq)
    
    #C-组中值计算
    dfBins_median=df_bins.median(level=0)
    dfBins_median.rename(columns={column_name:'median'},inplace=True)
    #print(dfBins_median)
    
    #D-合并分割区间、频数计算和组中值的DataFrame格式数据。
    df_fre=dfBins_freqANDrelFreq.join(dfBins_median).sort_index().reset_index() #在合并时会自动匹配index
    #print(ranmen_fre)
    
    #E-计算频数比例
    df_fre['fre_percent%']=df_fre.apply(lambda row:row['fre']/ranmen_fre.fre.sum()*100,axis=1)
    
    return df_fre
bins=range(0,600+50,50) #配置分割区间（组距）    
poiPrice_fre_50=frequency_bins(delicacy_price_df,bins)    
print(poiPrice_fre_50)
```

```
         index  fre    relFre  median  fre_percent%
0      [0, 50)  445  0.566879    26.0         890.0
1    [50, 100)  257  0.327389    70.0         514.0
2   [100, 150)   63  0.080255   110.0         126.0
3   [150, 200)   12  0.015287   165.5          24.0
4   [200, 250)    4  0.005096   214.5           8.0
5   [250, 300)    1  0.001274   285.0           2.0
6   [300, 350)    0  0.000000     NaN           0.0
7   [350, 400)    2  0.002548     NaN           4.0
8   [400, 450)    0  0.000000   571.0           0.0
9   [450, 500)    0  0.000000     NaN           0.0
10  [500, 550)    0  0.000000     NaN           0.0
11  [550, 600)    1  0.001274   381.0           2.0
```

```python
poiPrice_fre_50.loc[:,['fre','index']].plot.bar(x='index',rot=0,figsize=(15,5))
```

<a href=""><img src="./imgs/2_7.png" height="auto" width="auto" title="caDesign"/></a>

调整组距，查看总体频数分布情况

```python
bins=list(range(0,300+5,5))+[600] #通过df.describe()查看数据后，发现72%的价格位于72元之下，结合上图柱状图，重新配置组距，尽可能的显示数据变化的趋势。
poiPrice_fre_5=frequency_bins(delicacy_price_df,bins)    
import matplotlib.pyplot as plt
poiPrice_fre_5.loc[:,['fre','index']].plot.bar(x='index',rot=0,figsize=(30,5))
plt.xticks(rotation=90)
```

<a href=""><img src="./imgs/2_8.png" height="auto" width="auto" title="caDesign"/></a>

一般的事物都会呈现正态分布的形式，当组距配置约为5时，这种数据结构或者事物的规律就会显现出来，也能够从中发现价格变化的趋势。

###### 集中量数与变异量数

🍅建立简单数据示例，数据来源于《漫画统计学》保龄球大赛的结果。首先建立嵌套字典，然后将其转换为多重索引的DataFrame数据。

```python
bowlingContest_scores_dic={'A_team':{'Barney':86,'Harold':73,'Chris':124,'Neil':111,'Tony':90,'Simon':38},
                            "B_team":{'Jo':84,'Dina':71,'Graham':103,'Joe':85,'Alan':90,'Billy':89},
                            'C_team':{'Gordon':229,'Wade':77,'Cliff':59,'Arthur':95,'David':70,'Charles':88}
                          }
bowlingContest_scores=pd.DataFrame.from_dict(bowlingContest_scores_dic, orient='index').stack().to_frame(name='score') #可以逐步拆解来查看每一步的数据结构，结合搜索相关方法解释，可以理解每一步的作用。例如df.stack()是由列返回多重索引的DataFrame,具体可以查看官方案例，更直观的理解其作用
bowlingContest_scores #使用print()或者直接在每一JupyterLab的Cell最后给出要查看的变量名，都可以查看数据，只是可能显示的模式略有差异。但是建议使用print()查看，因为涉及到代码迁移时，单独变量的出现可能会造成代码运行错误。
```

<a href=""><img src="./imgs/2_9.jpg" height="500" width="auto" title="caDesign"/></a>

求每一队的均值（算数平均数）

```python
bowlingContest_mean=bowlingContest_scores.mean(level=0)
print(bowlingContest_mean)
```

```
        score
A_team   87.0
B_team   87.0
C_team  103.0
```

求每一队的中位数。C队的均值最高，其原因不是每一个队员的成绩都高，而是Gordon获得了229远超其他队员的得分。因此求中位数更为适合。

```python
bowlingContest_median=bowlingContest_scores.median(level=0)
print(bowlingContest_median)
```

```
        score
A_team   88.0
B_team   87.0
C_team   82.5
```

箱型图（Box plot），又称盒须图，盒式（状）图或箱线图，一种用作显示一组数据分散情况的统计图。显示的一组数据包括最大值，最小值，中位数和上下四分位数，因此使用箱型图较之单一的数值而言可以更清晰的观察数据分布情况。如图（引自Wikipedia）：

```
                            +-----+-+       
  *           o     |-------|   + | |---|
                            +-----+-+    
                                         
+---+---+---+---+---+---+---+---+---+---+   分数
0   1   2   3   4   5   6   7   8   9  10
```

这组数据显示：最小值（minimum）=5；下四分位数（Q1）=7；中位数（Med,即Q2）=8.5；上四分位数（Q3）=9；最大值（maximum）=10；平均值=8；四分位间距(interquartile range)=(Q3-Q2)=2(即ΔQ)。使用pandas自带的plot功能打印箱型图，查看各队分数的分布情况。

```python
bowlingContest_scores_transpose=bowlingContest_scores.stack().unstack(level=0)
boxplot=bowlingContest_scores_transpose.boxplot(column=['A_team', 'B_team', 'C_team'])
```

<a href=""><img src="./imgs/2_10.png" height="auto" width="auto" title="caDesign"/></a>

plotly库所提供的箱型图可以互动显示具体的数值，具有更强的图示能力。

```python
import plotly.express as px
fig = px.box(bowlingContest_scores.xs('C_team',level=0), y="score")
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    title='C_team'
    )
fig.show()
```

<a href=""><img src="./imgs/2_11.jpg" height="500" width="auto" title="caDesign"/></a>

求标准差，又称准偏差或均方差（Standard Deviation，缩写SD），数学符号通常用σ（sigma）。用于测量一组数值的离散程度，公式：$SD= \sqrt{1/N \sum_{i=1}^N { x_{i}- \mu  } } $ 其中$\mu$ 为平均值。虽然A_team和B_team具有相同的均值，但是数值的分布情况迥然不同，通过计算标准差比较离散程度，标准差越小，代表数据的离散程度越小；反之，标准差越大，离散程度越大。

```python
bowlingContest_std=bowlingContest_scores.std(level=0)
print(bowlingContest_std)
```

```
            score
A_team  30.172835
B_team  10.373042
C_team  63.033325
```

🐨返回到实验数据，因为一级行业分类分类中美食部分的'detial_info_tag'包含餐厅的子分类，使用箱型图显示子分类评分'detail_info_overall_rating'的数值分布情况，以及计算标准差。

```python
delicacy=poi_gpd.xs('poi_0_delicacy',level=0)
delicacy_rating=delicacy[['detail_info_tag','detail_info_overall_rating']] 
print(delicacy_rating.head())
```

```
  detail_info_tag  detail_info_overall_rating
0          美食;中餐厅                         4.4
2          美食;中餐厅                         4.1
4          美食;中餐厅                         4.5
6          美食;中餐厅                         4.4
8          美食;中餐厅                         4.2
```

查看餐厅类型。并移除错误的分类数据，例如`'教育培训;其他'`。同时可以调整子分类的名称，例如由'美食;中餐厅' 修改为'中餐厅'，其中使用了df.applay()方法。最后将其映射为英文字符，在打印时也可以避免显示错误，如果显示中文字符错误，需要增加相应处理语句。

```python
print(delicacy_rating.detail_info_tag.unique())
delicacy_rating_clean=delicacy_rating[delicacy_rating.detail_info_tag!='教育培训;其他']
print(delicacy_rating_clean.detail_info_tag.unique())
#定义一个函数，用于df.apply()函数处理字符串
def str_row(row):
    if type(row)==str:
        row_=row.split(';')[-1]
    else:
        #print(type(row))
        row_='nan' #原数据类型为nan，通过type(row)查看后为float数据类型，此时将其转换为字符串
    return row_
delicacy_rating_clean.loc[:,["detail_info_tag"]]=delicacy_rating_clean["detail_info_tag"].apply(str_row)  
print(delicacy_rating_clean.detail_info_tag.unique())

tag_mapping={'中餐厅':'Chinese_restaurant','小吃快餐店':'Snake_bar','nan':'nan','其他':'others','外国餐厅':'Foreign_restaurant','蛋糕甜品店':'CakeANDdessert_shop','咖啡厅':'cafe','茶座':'teahouse','酒吧':'bar'}
delicacy_rating_clean.loc[:,["detail_info_tag"]]=delicacy_rating_clean["detail_info_tag"].replace(tag_mapping)
print(delicacy_rating_clean.detail_info_tag.unique())
```

```
['美食;中餐厅' nan '美食;小吃快餐店' '美食;其他' '美食;外国餐厅' '美食;蛋糕甜品店' '美食;咖啡厅' '美食;茶座'
 '美食;酒吧' '教育培训;其他']
['美食;中餐厅' nan '美食;小吃快餐店' '美食;其他' '美食;外国餐厅' '美食;蛋糕甜品店' '美食;咖啡厅' '美食;茶座'
 '美食;酒吧']
['中餐厅' 'nan' '小吃快餐店' '其他' '外国餐厅' '蛋糕甜品店' '咖啡厅' '茶座' '酒吧']
['Chinese_restaurant' 'nan' 'Snake_bar' 'others' 'Foreign_restaurant'
 'CakeANDdessert_shop' 'cafe' 'teahouse' 'bar']
```

```python
delicacy_rating_clean.boxplot(column=['detail_info_overall_rating'],by=['detail_info_tag'],figsize=(25,8))
delicacy_rating_clean_std=delicacy_rating_clean.set_index(['detail_info_tag']).std(level=0)
print(delicacy_rating_clean_std)
```

```
                     detail_info_overall_rating
detail_info_tag                                
Chinese_restaurant                     0.488348
nan                                         NaN
Snake_bar                              0.490777
others                                 0.367939
Foreign_restaurant                     0.159960
CakeANDdessert_shop                    0.257505
cafe                                   0.243386
teahouse                               0.629374
bar                                    0.189297
```

<a href=""><img src="./imgs/2_12.png" height="auto" width="auto" title="caDesign"/></a>

###### 标准计分（分数）
🍅建立简单数据示例，数据来源于《漫画统计学》考试成绩。在这个案例中，虽然Mason和Reece分别在English和Chinese科目中，以及history和biology科目中具有相同的分数，但是因为标准差，即离散程度不同，所表示的重要程度亦不一样。标准差越小，离散程度越小，则数值每一单位的变化都会影响最终排名，即每一分都很重要。也可以理解为标准差小时，其他同学很容易追上你的成绩，但是标准差大时，其他同学不容易追上你的成绩。

```python
test_score_dic={"English":{"Mason":90,"Reece":81,'A':73,'B':97,'C':85,'D':60,'E':74,'F':64,'G':72,'H':67,'I':87,'J':78,'K':85,'L':96,'M':77,'N':100,'O':92,'P':86},
                "Chinese":{"Mason":71,"Reece":90,'A':79,'B':70,'C':67,'D':66,'E':60,'F':83,'G':57,'H':85,'I':93,'J':89,'K':78,'L':74,'M':65,'N':78,'O':53,'P':80},
                "history":{"Mason":73,"Reece":61,'A':74,'B':47,'C':49,'D':87,'E':69,'F':65,'G':36,'H':7,'I':53,'J':100,'K':57,'L':45,'M':56,'N':34,'O':37,'P':70},
                "biology":{"Mason":59,"Reece":73,'A':47,'B':38,'C':63,'D':56,'E':75,'F':53,'G':80,'H':50,'I':41,'J':62,'K':44,'L':26,'M':91,'N':35,'O':53,'P':68},
               }

test_score=pd.DataFrame.from_dict(test_score_dic)
print(test_score.tail())
```

```
       English  Chinese  history  biology
Mason       90       71       73       59
N          100       78       34       35
O           92       53       37       53
P           86       80       70       68
Reece       81       90       61       73
```

求标准计分（Standard Score），又称z-score即Z-分数，或标准化值。z-score代表原始数值和平均值之间的距离，并以标准差为单位计算，即z-score是从感兴趣的点到均值之间有多少个标准差，这样就可以在不同组数据间比较某一数值的重要程度。公式为：$z=(x- \mu )/ \sigma $其中，$\sigma  \neq 0$  并$x$是需要被标准化的原始分数，$\mu$是平均值，$\sigma$是标准差。

标准计分的特征：

1. 无论作为变量的满分为几分，其标准计分的平均数势必为0， 而其标准差势必为1；
2. 无论作为变量的单位是什么，其标准计分的平均数势必为0， 而其标准差势必为1. 

```python
from scipy.stats import zscore
test_Zscore=test_score.apply(zscore)
print(test_Zscore.tail())
```

```
        English   Chinese   history   biology
Mason  0.770054 -0.296174  0.780635  0.162355
N      1.658577  0.325792 -1.083330 -1.298840
O      0.947758 -1.895516 -0.939948 -0.202944
P      0.414644  0.503497  0.637253  0.710303
Reece -0.029617  1.392020  0.207107  1.014719
```

其中Mason在English科目中的标准计分为0.77，在整体分布中位于平均分之上0.71个标准差的地位；而Reece在Chinese中的标准计分为1.39，在整体分布中位于平均分之上1.39个标准差的地位，即Reece获得的每一分值价值高于Mason的所获取的每一分值，但是Mason的成绩不容易被人超越，也不容易超越他人。

🐨返回到实验数据，分别计算美食部分总体评分'detail_info_overall_rating'和价格 'detail_info_price'的标准计分。

```python
delicacy=poi_gpd.xs('poi_0_delicacy',level=0)
delicacy_dropna=delicacy.dropna(subset=['detail_info_overall_rating', 'detail_info_price'])
delicacy_Zscore=delicacy_dropna[['detail_info_overall_rating', 'detail_info_price']].apply(zscore).join(delicacy["name"])
print(delicacy_Zscore.head())
```

```
   detail_info_overall_rating  detail_info_price             name
0                    0.180589           1.389133       西安饭庄(锦业路店)
2                   -0.773606           0.505657        范家大院(华为店)
4                    0.498655          -0.015368       苏福记(紫薇臻品店)
6                    0.180589          -0.060674        大厨小馆(绿地店)
8                   -0.455541           0.800149  上下九广州菜馆(锦业路旗舰店)
```

在实验数据里可以计算z_score比较某一饭店的价格和评分的重要性，其意义是，是否价格越接近均值，对应的评分越高于（低于）均值。但是单独看单一饭店的数据很难判断是否存在这样的一种关系，因此可以打印曲线，观察曲线的变化规律。因为原始数据量较大，需要使用df.rolling()方法平滑数据后再绘制曲线观察数据。

```python
cdelicacy_Zscore.rolling(20, win_type='triang').sum().plot.line(figsize=(25,8))
```

<a href=""><img src="./imgs/2_13.png" height="auto" width="auto" title="caDesign"/></a>

从上图可以观察到，当价格标准计分（橘色线）高时，对应的评价分数标准计分通常趋低，反之亦然。即如果饭店在定制饭菜销售价格时，如果定制的价格趋近于均值，相对而言，所获取的评价越高于平均值。

### 1.5 要点
#### 1.5.1 数据处理技术
* pandas处理技术汇总-A

pandas的DataFrame和Series数据格式是最为常用的数据格式，尤其在地理空间数据处理中更具有重要的作用。pandas提供的处理工具数不胜数，想以通读pandas手册来掌握pandas是不现实，也是不可取的。通常来讲，可以学习入门手册，对其有个初步了解，再在处理数据过程中遇到相关问题时搜索获取。虽然不用系统的查看pandas功用，但是有些常用的功能会经常用到，又或者有些功能是自己多费周章才搜索查到，或者自己又进一步完善编写，如果不记录，下次遇到时即使搜索也不宜查到，那么可以尝试根据自己的情况建立自己的代码仓库，当用到时方便查询。

[pandas](https://pandas.pydata.org/)库官方文档一般给出了详细的解释，包括功用、参数、属性以及实际案例，因此在汇总pandas处理技术时，只是简单罗列说明函数及其功用，备以查询，具体内容则可以借助这个简要说明进一步利用搜索引擎检索。
1. 数据合并类

-合并列表， `poi_df_concat=pd.concat(poi_df_dic.values(),keys=poi_df_dic.keys(),sort=True)`

-直接建立， `ranmenPriceBins_freqANDrelFreq=pd.DataFrame({'fre':ranmenPriceBins_frequency,'relFre':ranmenPriceBins_relativeFrequency})`

-Seire格式转换为DataFrame， `delicacy_price_df=delicacy_price.to_frame(name='price')`

-追加df， `ranmen_fre=ranmenPriceBins_freqANDrelFreq.join(ranmenPriceBins_median).sort_index().reset_index()`

-从嵌套字典建立， `bowlingContest_scores=pd.DataFrame.from_dict(bowlingContest_scores_dic, orient='index').stack().to_frame(name='score')`


2. 数值检索类

-.loc()方式,同时配置index和colomn

```python
poi_fieldsExtraction=poi_df_concat.loc[:,fields_extraction]
poi_gpd.loc[['poi_0_delicacy'],:].plot(column='detail_info_overall_rating') 
df=poi_gpd.loc[pd.IndexSlice[:,:2],:]
```

-.xs方式，多重索引提取

`delicacy_price=poi_gpd.xs('poi_0_delicacy',level=0).detail_info_price`


3. 数据操作类

-应用函数逐行操作数据，

使用lambda匿名函数

`poi_geoDF['geometry']=poi_geoDF.apply(lambda row:Point(row.location_lng,row.location_lat),axis=1)`

使用自定义函数

```python
def str_row(row):
    if type(row)==str:
        row_=row.split(';')[-1]
    else:
        #print(type(row))
        row_='nan' #原数据类型为nan，通过type(row)查看后为float数据类型，此时将其转换为字符串
    return row_
    
delicacy_rating_clean.loc[:,["detail_info_tag"]]=delicacy_rating_clean["detail_info_tag"].apply(str_row)
```

-根据组距切分数据，`ranmen_price['price_bins']=pd.cut(x=ranmen_price.price,bins=bins,right=False)`

-排序行， `ranmenPrice_bins=ranmen_price.sort_values(by=['price'])` 

-频数计算， `ranmenPriceBins_frequency=ranmenPrice_bins.price_bins.value_counts(normalize=True)`

-计算中值， `ranmenPriceBins_median=ranmenPrice_bins.median(level=0)`

-求均值， `bowlingContest_mean=bowlingContest_scores.mean(level=0)`

-求标准差， `bowlingContest_std=bowlingContest_scores.std(level=0)`

-求标准计分， 

```python
from scipy.stats import zscore
test_Zscore=test_score.apply(zscore)
```

-移除空值， `delicacy_dropna=delicacy.dropna(subset=['detail_info_overall_rating', 'detail_info_price'])`

-平滑数据， `delicacy_Zscore.rolling(20, win_type='triang').sum().plot.line(figsize=(25,8))`

4. 索引操作类（(multi)index 和 columns）

-重置索引， `df=df.reset_index()`

-设置（多重）索引， `ranmenPrice_bins.set_index(['price_bins',ranmenPrice_bins.index],drop=False,inplace=True)`

-多重索引切分， `df=poi_gpd.loc[pd.IndexSlice[:,:2],:]`

-重命名， `ranmenPriceBins_median.rename(columns={'price':'median'},inplace=True)`

-组织结构， `bowlingContest_scores_transpose=bowlingContest_scores.stack().unstack(level=0)`

5. 图表打印类

-柱状图，`ranmen_fre.loc[:,['fre','index']].plot.bar(x='index',rot=0,figsize=(5,5))`

-箱型图，`boxplot=bowlingContest_scores_transpose.boxplot(column=['A_team', 'B_team', 'C_team'])`

6. 其它

-复制与深度复制 `poi_geoDF=poi_fieldsExtraction.copy(deep=True)`

* geopandas数据保存类型包括： Shapefile(.shp)，GeoJSON(.geojson)，GeoPackage(.gpkg)以及PostGIS，示例如下（引自geopandas官网手册）：

```python
countries_gdf.to_file("countries.shp")
countries_gdf.to_file("countries.geojson", driver='GeoJSON')

countries_gdf.to_file("package.gpkg", layer='countries', driver="GPKG")
cities_gdf.to_file("package.gpkg", layer='cities', driver="GPKG")

from sqlalchemy import create_engine
db_connection_url = "postgres://myusername:mypassword@myhost:5432/mydatabase";
engine = create_engine(db_connection_url)
countries_gdf.to_postgis(name="countries_table", con=engine)
```

#### 1.5.2 新建立的函数工具
* function-百度地图开放平台POI数据批量爬取，baiduPOI_batchCrawler(poi_config_para)。需要调用单个分类POI爬取函数baiduPOI_dataCrawler(query_dic,bound_coordinate,partition,page_num_range,poi_fn_list=False)'
* funciton-以所在文件夹路径为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 filePath_extraction(dirpath,fileType)
* funciton-.csv格式POI数据批量转换为GeoDataFrame，poi_csv2GeoDF_batch(poi_paths,fields_extraction,save_path)。需要调用转换.csv格式的POI数据为pandas的DataFrame函数csv2df(poi_fn_csv)
* funciton-使用plotly以表格形式显示DataFrame格式数据,ployly_table(df,column_extraction)
* function-频数分布计算，frequency_bins(df,bins)

#### 1.5.3 所调用的python库

```python
import util_poi
import os, pathlib
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import zscore
```