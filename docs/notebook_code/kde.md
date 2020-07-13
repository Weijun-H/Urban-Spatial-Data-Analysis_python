> Created on Thu Jul  9 22/10/09 2020  @author: Richie Bao-caDesign设计(cadesign.cn)

## 1 核密度估计与地理空间点密度分布
### 1.1 核密度估计
#### 1.1.1 单变量（一维数组）的核密度估计
当直方图的组距无限缩小至极限后，能够拟合出一条曲线，计算这个分布曲线的公式即为概率密度函数（Probability Density Function,PDF），这是在[正态分布](https://richiebao.github.io/Urban-Spatial-Data-Analysis_python/#/./notebook_code/normalDis_PDF_outliers)一节中所阐述的内容，而用于估计概率密度函数的非参数方法就是核密度估计。核密度估计（Kernel density estimation, KDE）是一个基本的数据平滑问题（a fundamental data smoothing problem），例如对不平滑的直方图平滑，给定一个核K, 并指定带宽（bandwidth），其值为正数，核密度估计定义为： $\hat{f} _{n} (x)= \frac{1}{nh}  \sum_{i=1}^n {K( \frac{x- x_{i} }{h} )} $，其中K为核函数，$h$为带宽，核函数有多个，例举其中高斯核为：$\frac{1}{ \sqrt{2 \pi } }  e^{- \frac{1}{2}  x^{2} } $，将其带入核密度估计公式结果为：$\hat{f} _{n} (x)= \frac{1}{ \sqrt{2 \pi } nh}  \sum_{i=1}^n { e^{ -\frac{ (x- x_{i} )^{2} }{2 h^{2} } } } $。

在下述代码中绘制了三条曲线，红色粗线为概率密度函数；两条细线均为核密度估计（高斯核），只是蓝色线是依据核密度公式直接编写代码，并设置带宽h=0.4；绿色线则是使用scipy库下的`stats.gaussian_kde()`方法计算高斯核密度估计。

> 非参数统计（Nonparametric Statistics）是统计的一个分支，但不是完全基于参数化的概率分布，例如通过参数均值和方差（或标准差）定义一个正态分布，非参数统计基于自由分布（distribution-free）或指定的分布但未给分布参数，例如当处理PDF的一般情况时，不能像正态分布那样给定参数进行分类。其基本思想是在尽可能少的假定时，利用数据对一个未知量做出推断，通常意味着利用具有无穷维的统计模型。 

> 对于核密度估计名词中密度一词可以形象理解为下图中橄榄绿小竖线的分布密度。

参考：Wikipedia以及 Larry Wasserman.All of nonparametric statistics.Springer (October 21, 2005),中文版为：[美]Larry Wasserman.吴喜之译.现代非参数统计[M].科学出版社,北京.2008.5；Urmila Diwekar,Amy David.Bonus algorithm for large scale stochastic nonlinear programming problems.Springer; 2015 edition (March 5, 2015)

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import math
x=np.linspace(stats.norm.ppf(0.001,loc=0,scale=1),stats.norm.ppf(0.999,loc=0,scale=1), 100) #等分概率为0.1%到99.9%之间的数值。如果不给参数loc和scale,则默认为标准正态分布，即loc=0, scale=1
pdf=stats.norm.pdf(x)

plt.figure(figsize=(25,5))
plt.plot(x,pdf,'r-', lw=5, alpha=0.6, label='norm_pdf')

random_variates=stats.norm.rvs(loc=0,scale=1,size=500)
count, bins, ignored =plt.hist(random_variates,bins=100,density=True,histtype='stepfilled',alpha=0.2)
plt.eventplot(random_variates,color='y',linelengths=0.03,lineoffsets=0.025) #给定位置画出对应的短线

rVar_sort=np.sort(random_variates)
h=0.4 #带宽（bandwidth,bw）
n=len(rVar_sort)
kde_Gaussian=[sum(math.exp(-1*math.pow(vi-vj,2)/(2*math.pow(h,2))) for vj in rVar_sort)/(h*n*math.sqrt(2*math.pi)) for vi in rVar_sort] #将上述高斯核密度估计公式转换为代码
plt.plot(rVar_sort,kde_Gaussian,'b-', lw=2, alpha=0.6, label='kde_formula,h=%s'%h)

scipyStatsGaussian_kde=stats.gaussian_kde(random_variates)
plt.plot(bins,scipyStatsGaussian_kde(bins),'g-', lw=2, alpha=0.6, label='scipyStatsGaussian_kde')
plt.legend()
plt.show()
```

<a href=""><img src="./imgs/5_1.png" height="auto" width="auto" title="caDesign"></a>

带宽（bandwidth）影响光滑的程度，下述实验设置不同的值，观察核密度曲线的变化情况。关于最适宜的带宽推断，<em>Bonus algorithm for large scale stochastic nonlinear programming problems</em>第3章，<em>Probability Density Function and Kernel Density Estimation</em>一节中提到一种方法，可以参考。

```python
bws=np.arange(0.1,1,0.2)
colors_kde=['C{}'.format(i) for i in range(len(bws))] #maplotlib，指定颜色
i=0
plt.figure(figsize=(25,5))
for h in bws:
    kde_Gaussian=[sum(math.exp(-1*math.pow(vi-vj,2)/(2*math.pow(h,2))) for vj in rVar_sort)/(h*n*math.sqrt(2*math.pi)) for vi in rVar_sort] #将上述高斯核密度估计公式转换为代码
    plt.plot(rVar_sort,kde_Gaussian,color=colors_kde[i], lw=2, alpha=0.6, label='kde_formula,h=%.2f'%h)
    i+=1
plt.legend()
plt.show()
```

<a href=""><img src="./imgs/5_2.png" height="auto" width="auto" title="caDesign"></a>

#### 1.1.2 多变量（多维数组）的核密度估计
核密度估计可以平滑多维数据，例如热力图的制作是基于核密度估计的二维平滑，以爬取的百度POI和OSM数据为例，直接使用`scipy.stats.gaussian_kde()`计算其核密度，一是计算所有点的核密度估计；二是提取一级分类为'美食'（delicacy）的行，计算美食的核密度估计。

```python
import pandas as pd
poi_gpd=pd.read_pickle('./data/poiAll_gpd.pkl') #读取已经存储为.pkl格式的POI数据，其中包括geometry字段，为GeoDataFrame地理信息数据，可以通过poi_gpd.plot()迅速查看数据。
poi_gpd.plot(marker=".",markersize=5) #查看POI数据是否读取正常
```

<a href=""><img src="./imgs/5_3.png" height="auto" width="auto" title="caDesign"></a>

* 所有POI点数据的核密度估计，并建立地图

```python
from scipy import stats
poi_coordinates=poi_gpd[['location_lng','location_lat']].to_numpy().T  #根据stats.gaussian_kde()输入参数要求确定数组结构
poi_coordi_kernel=stats.gaussian_kde(poi_coordinates) #核密度估计
poi_gpd['poi_kde']=poi_coordi_kernel(poi_coordinates)

import plotly.express as px
poi_gpd.detail_info_price=poi_gpd.detail_info_price.fillna(0) 
mapbox_token='pk.eyJ1IjoicmljaGllYmFvIiwiYSI6ImNrYjB3N2NyMzBlMG8yc254dTRzNnMyeHMifQ.QT7MdjQKs9Y6OtaJaJAn0A'
px.set_mapbox_access_token(mapbox_token)
fig=px.scatter_mapbox(poi_gpd,lat=poi_gpd.location_lat, lon=poi_gpd.location_lng,color='poi_kde',color_continuous_scale=px.colors.sequential.PuBuGn, size_max=15, zoom=10) #亦可以选择列，通过size=""配置增加显示信息
fig.show()

poi_gpd.head()
```

<a href=""><img src="./imgs/5_4.png" height="auto" width="auto" title="caDesign"></a>

|index|name|	location_lat|	location_lng|	detail_info_tag|	detail_info_overall_rating	|detail_info_price|	geometry|	poi_kde|
|---|---|---|---|---|---|---|---|---|
|0|	御荷苑饭店|	34.182148|	108.823310|	美食;中餐厅|	4.0	|0|	POINT (108.82331 34.18215)	|2.917734|
|2|	一品轩餐厅|	34.183155|	108.823328|	美食;中餐厅	|5.0|	0	|POINT (108.82333 34.18316)	|3.131301|
|4|	老米家泡馍|	34.183547|	108.823851|	美食;中餐厅	|5.0|	0	|POINT (108.82385 34.18355)	|3.264152|
|6|	关中印象咥长安(创汇店)|	34.183542|	108.823498|	美食;中餐厅|	4.5|	8	|POINT (108.82350 34.18354)|	3.227471|
|8|	惠记葫芦头梆梆肉|	34.183534|	108.823589|	美食;中餐厅|	4.6|	0|	POINT (108.82359 34.18353)	|3.234969|

* '美食'位置点分布的核密度估计

```python
pd.options.mode.chained_assignment = None
poi_gpd['tag_primary']=poi_gpd['detail_info_tag'].apply(lambda row:str(row).split(";")[0])
poi_classificationName={
        "美食":"delicacy",
        "酒店":"hotel",
        "购物":"shopping",
        "生活服务":"lifeService",
        "丽人":"beauty",
        "旅游景点":"spot",
        "休闲娱乐":"entertainment",
        "运动健身":"sports",
        "教育培训":"education",
        "文化传媒":"media",
        "医疗":"medicalTreatment",
        "汽车服务":"carService",
        "交通设施":"trafficFacilities",
        "金融":"finance",
        "房地产":"realEstate",
        "公司企业":"corporation",
        "政府机构":"government",
        'nan':'nan'
        }
poi_gpd.loc[:,["tag_primary"]]=poi_gpd["tag_primary"].replace(poi_classificationName)
delicacy_df=poi_gpd.loc[poi_gpd.tag_primary=='delicacy']
delicacy_coordi=delicacy_df[['location_lng','location_lat']].to_numpy().T 
delicacy_kernel=stats.gaussian_kde(delicacy_coordi) #核密度估计
delicacy_df['delicacy_kde']=delicacy_kernel(delicacy_coordi)

import plotly.express as px
poi_gpd.detail_info_price=poi_gpd.detail_info_price.fillna(0) 
mapbox_token='pk.eyJ1IjoicmljaGllYmFvIiwiYSI6ImNrYjB3N2NyMzBlMG8yc254dTRzNnMyeHMifQ.QT7MdjQKs9Y6OtaJaJAn0A'
px.set_mapbox_access_token(mapbox_token)
fig=px.scatter_mapbox(delicacy_df,lat=delicacy_df.location_lat, lon=delicacy_df.location_lng,color='delicacy_kde',color_continuous_scale=px.colors.sequential.PuBuGn, size_max=15, zoom=10) #亦可以选择列，通过size=""配置增加显示信息
fig.show()
```

<a href=""><img src="./imgs/5_5.png" height="auto" width="auto" title="caDesign"></a>

### 1.2 核密度估计结果转换为地理栅格数据
上述二维地理空间点的核密度估计最终的计算值在地图表达上落在了点位置本身，如果希望能够以栅格的形式显示估计值，可以将其转换为栅格数据，本质上就是地理空间点数据转栅格数据。在下述的方法中，提供了两种转换方式，一种方式是将存储有核密度估计值的GeoDataFrame格式数据先直接使用`gdf.to_file()`存储为.shp格式的点数据，然后定义.shp转栅格的函数；第二种方式是直接定义一个函数，能够直接计算核密度估计并同时直接存储为栅格数据。在这两种方式中均需要定义GeoDataFrame格式数据的坐标投影，并提取其信息用于使用GDAL库提取或定义坐标投影，因此必须在geopandas库和GDAL库之间有可以互相转换的共同的坐标体系，EPSG编号体系是比较好的选择。EPSG（European Petroleum Survey Group）最早建立了该编码体系，其中最为重要的编码包括：

EPSG:4326 - 即WGS84，广泛应用于地图和导航系统，在地理空间数据分析中，这个地理坐标系统是最为基础表征位置数据的坐标系统，通常各类地理空间的数据信息都以WGS84为基本的坐标系统，而后可以在不同数据类型或者平台，以及根据分析目的的不同，尤其实际地理位置的变化来配置投影。

EPSG:3857 - 伪墨卡托投影，也被称为球体墨卡托，用于显示许多基于网页的地图工具，包括Google地图和OpenStreetMap等。

关于EPSG编码可以查看：[spatialreference](https://spatialreference.org/)，和[epsg.io](https://epsg.io/)

本次实验输出栅格的坐标投影系统为EPSG:32649，即WGS 84 / UTM zone 49N，对应西安区域Landsat遥感影像所使用的坐标投影系统。通常在分析某一城市空间问题时，可能用到很多类型的，不同来源的数据，尽量以最基本的WGS84作为数据存储坐标系统之外，数据的显示往往需要对应区域的坐标系统，从而优化显示结果，使其更适宜阅读。

```python
import geopandas as gpd
from pyproj import CRS
import os
import pandas as pd

poi_gpd=pd.read_pickle('./data/poiAll_gpd.pkl') #读取已经存储为.pkl格式的POI数据，其中包括geometry字段，为GeoDataFrame地理信息数据，可以通过poi_gpd.plot()迅速查看数据。
poi_gpd.plot(marker=".",markersize=5) #查看POI数据是否读取正常

print("original projection:",poi_gpd.crs)
poi_gpd_copy=poi_gpd.copy(deep=True)
poi_gpd_copy=poi_gpd_copy.to_crs(CRS("EPSG:32649"))
print("re-projecting:",poi_gpd_copy.crs)

save_path=r'./data/geoData'
poi_epsg32649_fn='poi_epsg32649.shp'
poi_gpd_copy.to_file(os.path.join(save_path,poi_epsg32649_fn))
```

```
original projection: epsg:4326
re-projecting: EPSG:32649
```

<a href=""><img src="./imgs/5_6.png" height="auto" width="auto" title="caDesign"></a>

#### 1.2.1 .shp格式地理空间点数据转栅格数据
该函数定义的核心是GDAL库提供的`gdal.RasterizeLayer()`方法，可以将读取的.shp点层属性字段的值写入对应位置的栅格，从而避免编写对位栅格单元位置和字段值数组的代码。在栅格投影定义上直接提取.shp点数据的坐标投影系统，代码位置于向栅格单元写入数据之后，如果位于之前，则会出现坐标投影错误。在栅格定义时，空值通常设置为-9999。GDAL提供栅格定义的方式为先获取栅格驱动`gdal.GetDriverByName('GTiff')`，再建立`.Create(raster_path, x_res, y_res, 1, gdal.GDT_Float64)`。并配置地理变换`target_ds.SetGeoTransform((x_min, cellSize, 0, y_max, 0, -cellSize))`，通过读取栅格波段`band=target_ds.GetRasterBand(1)`，向其写入值`band.WriteArray()`完成栅格的定义。地理变换中，因为地图通常向上为北向，因此第3和第5个参数通常配置为0。

```python
#convert points .shp to raster 将点数据写入为raster数据。使用raster.SetGeoTransform,栅格化数据。参考GDAL官方代码
def pts2raster(pts_shp,raster_path,cellSize,field_name=False):
    from osgeo import gdal, ogr,osr
    '''
    function - 将.shp格式的点数据转换为.tif栅格(raster)
    
    Paras:
    pts_shp - .shp格式点数据文件路径
    raster_path - 保存的栅格文件路径
    cellSize - 栅格单元大小
    field_name - 写入栅格的.shp点数据属性字段
    '''
    #定义空值（没有数据）的栅格数值 Define NoData value of new raster
    NoData_value=-9999
    
    #打开.shp点数据，并返回地理区域范围 Open the data source and read in the extent
    source_ds=ogr.Open(pts_shp)
    source_layer=source_ds.GetLayer()
    x_min, x_max, y_min, y_max=source_layer.GetExtent()
    
    #使用GDAL库建立栅格 Create the destination data source
    x_res=int((x_max - x_min) / cellSize)
    y_res=int((y_max - y_min) / cellSize)
    target_ds=gdal.GetDriverByName('GTiff').Create(raster_path, x_res, y_res, 1, gdal.GDT_Float64) #create(filename,x_size,y_size,band_count,data_type,creation_options)。gdal的数据类型 gdal.GDT_Float64,gdal.GDT_Int32...
    target_ds.SetGeoTransform((x_min, cellSize, 0, y_max, 0, -cellSize))
    outband=target_ds.GetRasterBand(1)
    outband.SetNoDataValue(NoData_value)

    #向栅格层中写入数据
    if field_name:
        gdal.RasterizeLayer(target_ds,[1], source_layer,options=["ATTRIBUTE={0}".format(field_name)])
    else:
        gdal.RasterizeLayer(target_ds,[1], source_layer,burn_values=[-1])   
        
    #配置投影坐标系统
    spatialRef=source_layer.GetSpatialRef()
    target_ds.SetProjection(spatialRef.ExportToWkt())       
        
    outband.FlushCache()
    return gdal.Open(raster_path).ReadAsArray()

pts_shp=os.path.join(save_path,poi_epsg32649_fn)
raster_path=os.path.join(save_path,r'poi_epsg32649.tif')
cellSize=100
field_name='poi_kde'
poiRaster_array=pts2raster(pts_shp,raster_path,cellSize,field_name)
print("conversion complete!")
```

```
conversion complete!
```

python中处理栅格数据的库可以使用[rasterio](https://rasterio.readthedocs.io/en/latest/quickstart.html#reading-raster-data)，相比GDAL能够大幅度减少代码的数量，其方法也更便捷。用该库读取栅格数据的相关信息，并读取数据为数组（array）,及打印栅格查看数据。

```python
raster_path=os.path.join(save_path,r'poi_epsg32649.tif')
import rasterio
dataset=rasterio.open(raster_path)
print(
    "band count:",dataset.count,'\n', #查看栅格波段数量
    "columns wide:",dataset.width,'\n', #查看栅格宽度
    "rows hight:",dataset.height,'\n', #查看栅格高度
    "dataset's index and data type:",{i: dtype for i, dtype in zip(dataset.indexes, dataset.dtypes)},'\n',#查看波段及其数据类型
    "bounds:",dataset.bounds,'\n', #查看外接矩形边界左下角与右上角坐标
    "geospatial transform:",dataset.transform,'\n', #数据集的地理空间变换
    "lower right corner:",dataset.transform*(dataset.width,dataset.height),'\n', #计算外接矩形边界右下角坐标
    "crs:",dataset.crs,'\n', #地理坐标投影系统
    "band's index number:",dataset.indexes,'\n' #栅格层（波段）索引
    )
band1=dataset.read(1) #读取栅格波段数据为数组
print(band1)
```

```
band count: 1 
 columns wide: 653 
 rows hight: 446 
 dataset's index and data type: {1: 'float64'} 
 bounds: BoundingBox(left=294142.8129965692, bottom=3783958.0837052986, right=326792.8129965692, top=3806258.0837052986) 
 geospatial transform: | 50.00, 0.00, 294142.81|
| 0.00,-50.00, 3806258.08|
| 0.00, 0.00, 1.00| 
 lower right corner: (326792.8129965692, 3783958.0837052986) 
 crs: EPSG:32649 
 band's index number: (1,) 

[[-9999. -9999. -9999. ... -9999. -9999. -9999.]
 [-9999. -9999. -9999. ... -9999. -9999. -9999.]
 [-9999. -9999. -9999. ... -9999. -9999. -9999.]
 ...
 [-9999. -9999. -9999. ... -9999. -9999. -9999.]
 [-9999. -9999. -9999. ... -9999. -9999. -9999.]
 [-9999. -9999. -9999. ... -9999. -9999. -9999.]]
 ```

```python
from rasterio.plot import show
import matplotlib.pyplot as plt
plt.figure(figsize=(15,10))
show((dataset,1),cmap='Greens') 
plt.show()
```

<a href=""><img src="./imgs/5_7.png" height="auto" width="auto" title="caDesign"></a>

rasterio库支持的颜色(基本同matplotlib库，可以在该库查看具体名称对应的颜色带)： 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'

在QGIS或者ArcGIS中打开查看结果。该部分的栅格化过程，开始配置了空值为，`outband.SetNoDataValue(-9999)`，后续向栅格写入数据时，仅含有值的位置替换原空值，因此，所看到的栅格空值部分透明。

<a href=""><img src="./imgs/5_8.jpg" height="auto" width="auto" title="caDesign"></a>

#### 1.2.2 给定GeoDataFrame格式的地理空间点数据，计算核密度估计存储为栅格数据
下述函数的定义将核密度估计置于函数之内，可以传入GeoDataFrame格式地理空间点数据（pts_geoDF），给定保存位置（raster_path），栅格单元大小（cellSize），以及调整核密度估计值比例缩放因子（scale）直接获取最后的核密度估计值栅格图（热力图）。这种计算方法能够减少中间步骤，尤其不用先转换为.shp格式的点数据后再存储为栅格数据。但是这种将多个步骤放置于一个函数中的计算方式，会将“单步”的计算时长拉长，因此最好在函数内通过print()函数打印相关完成信息，避免大批量数据计算时，不知道完成进度，无法确定程序是否仍在正常运行，或者已经完成，甚至已经中断。

GDAL库提供建立栅格，向栅格单元写入数值的方法是`outband.WriteArray() `，传入的参数为数组，这个数组对应着栅格的位置，因此计算完核密度估计之后，定义提取估计值的位置坐标需要重新进行定义，而不能直接用点坐标。在位置（positions）定义上借助`np.meshgrid()`实现，同时需要注意上述定义的positions位置提取估计值，其顺序是逆反的，即由下往上逐行读取，这个通常符合对图片像素的定义顺序，在地理栅格数据中，通常是由上往下写入，因此用`np.flip(Z,0)`翻转数组，将最后一行提为正数第一行，倒数第二行为正数第二行，以此类推。

```python
def pts_geoDF2raster(pts_geoDF,raster_path,cellSize,scale):
    from osgeo import gdal,ogr,osr
    import numpy as np
    from scipy import stats
    '''
    function - 将GeoDaraFrame格式的点数据转换为栅格数据
    
    Paras:
    pts_geoDF - GeoDaraFrame格式的点数据
    raster_path - 保存的栅格文件路径
    cellSize - 栅格单元大小
    scale - 缩放核密度估计值
    '''
    #定义空值（没有数据）的栅格数值 Define NoData value of new raster
    NoData_value=-9999
    x_min, y_min,x_max, y_max=pts_geoDF.geometry.total_bounds

    #使用GDAL库建立栅格 Create the destination data source
    x_res=int((x_max - x_min) / cellSize)
    y_res=int((y_max - y_min) / cellSize)
    target_ds=gdal.GetDriverByName('GTiff').Create(raster_path, x_res, y_res, 1, gdal.GDT_Float64 )
    target_ds.SetGeoTransform((x_min, cellSize, 0, y_max, 0, -cellSize))
    outband=target_ds.GetRasterBand(1)
    outband.SetNoDataValue(NoData_value)   
    
    #配置投影坐标系统
    spatialRef = osr.SpatialReference()
    epsg=int(pts_geoDF.crs.srs.split(":")[-1])
    spatialRef.ImportFromEPSG(epsg)  
    target_ds.SetProjection(spatialRef.ExportToWkt())
    
    #向栅格层中写入数据
    #print(x_res,y_res)
    X, Y = np.meshgrid(np.linspace(x_min,x_max,x_res), np.linspace(y_min,y_max,y_res)) #用于定义提取核密度估计值的栅格单元坐标数组
    positions=np.vstack([X.ravel(), Y.ravel()])
    values=np.vstack([pts_geoDF.geometry.x, pts_geoDF.geometry.y])    
    print("Start calculating kde...")
    kernel=stats.gaussian_kde(values)
    Z=np.reshape(kernel(positions).T, X.shape)
    print("Finish calculating kde!")
    #print(values)
        
    outband.WriteArray(np.flip(Z,0)*scale) #需要翻转数组，写栅格单元        
    outband.FlushCache()
    print("conversion complete!")
    return gdal.Open(raster_path).ReadAsArray()
    
save_path=r'./data/geoData'
raster_path_gpd=os.path.join(save_path,r'poi_gpd.tif')
cellSize=500 #cellSize值越小，需要计算的时间越长，开始调试时，可以尝试将其调大以节约计算时间，例如值为50，100等
scale=10**10 #相当于math.pow(10,10)
poiRasterGeoDF_array=pts_geoDF2raster(poi_gpd_copy,raster_path_gpd,cellSize,scale)    
```

```
Start calculating kde...
Finish calculating kde!
conversion complete!
```

```python
save_path=r'./data/geoData'
raster_path_gpd=os.path.join(save_path,r'poi_gpd.tif')
import rasterio
dataset_gpd=rasterio.open(raster_path_gpd)

from rasterio.plot import show
import matplotlib.pyplot as plt
plt.figure(figsize=(15,10))
show((dataset_gpd,1),contour=True,cmap='Greens') #开启等高线模式
plt.show()
```

<a href=""><img src="./imgs/5_9.png" height="auto" width="auto" title="caDesign"></a>

```python
plt.figure(figsize=(15,10))
show((dataset_gpd,1),cmap='Greens') #开启等高线模式
plt.show()
```

<a href=""><img src="./imgs/5_10.png" height="auto" width="auto" title="caDesign"></a>

#### 1.2.3 芝加哥城及其区域OSM地理空间点数据的核密度估计

将上述.shp点转栅格,以及地理空间点核密度计算并直接存储为栅格的两个函数放置于util.py工具文件中,方便调用。 在[OSM数据处理](https://richiebao.github.io/Urban-Spatial-Data-Analysis_python/#/./notebook_code/OSM_dataProcessing)章节已经叙述了OSM数据处理的方法，并简要的概述了OSM地理空间数据集的结构。OSM的Node标签分类丰富，针对不同的问题可以提取不同标签用于分析。因为标签中的便利设施（amenity）与人们的日常生活栖息相关，包括生计、教育、交通、金融、医疗、娱乐、艺术和文化等等，而更进一步的分类多达100多。因此提取标签（tags）为amenity的多有空间点数据，计算核密度估计，查看其分布情况。

```python
import util 
start_time=util.start_time()
read_node_gdf=gpd.read_file("./data/osm_node.gpkg")
util.duration(start_time)
```

```
start time: 2020-07-12 14:53:32.200039
end time: 2020-07-12 15:29:14.515908
Total time spend:35.70 minutes
```

```python
read_node_gdf.head()
```

|index|type|	id|	version|	visible|	ts|	uid|	user|	changeet|	tagLen|	tags|	geometry|
|---|---|---|---|---|---|---|---|---|---|---|---|
|0|	node|	219850|	55|	True|	2018-02-20T05/50/28	|0|	|	0|	2|	{"highway": "motorway_junction", "ref": "276C"}|	POINT (-87.91012 41.75859)|
|1|	node|	219851|	48|	True|	2018-02-20T05/50/29	|0|	|	0|	2|	{"highway": "motorway_junction", "ref": "277A"}	|POINT (-87.90764 41.75931)|
|2|	node|	219966|	5|	True|	2009-04-04T22/47/50	|0|	|	0|	0|	{}|	POINT (-87.91596 43.01149)|
|3|	node|	219968|	12|	True|	2015-08-04T05/38/49	|0|	|	0|	2|	{"ref": "73B", "highway": "motorway_junction"}|	POINT (-87.92464 43.05606)|
|4|	node|	219969|	6|	True|	2009-04-14T00/13/37	|0|	|	0|	0|	{}|	POINT (-87.92441 43.05684)|

```python
amenity_poi=read_node_gdf[read_node_gdf.tags.apply(lambda row: "amenity" in eval(row).keys())] #提取标tags列，含标签"amenity"的所有行
print("Finished amenity extraction!")
```

```
Finished amenity extraction!
```

因为原始的OSM数据读取的时间大概需要35分钟，而提取仅含"amenity"的行后，数据大幅度减少，后续的分析均只针对提取后的数据，因此将该数据单独保存，方便后续读取分析，避免读取大文件带来的时间成本。

```python
print(
    "the overal data number:",read_node_gdf.shape,'\n',
    "the amenity data number:",amenity_poi.shape,'\n',     
     )
amenity_poi.to_file("./data/geoData/amenity_poi.gpkg",driver='GPKG')
print("Finished saving!")
```

```
the overal data number: (23859111, 11) 
 the amenity data number: (38421, 11) 

Finished saving!
```

```python
import geopandas as gpd
amenity_poi=gpd.read_file("./data/geoData/amenity_poi.gpkg")
amenity_poi.plot(marker=".",markersize=5,figsize=(15, 8))
```

<a href=""><img src="./imgs/5_11.png" height="auto" width="auto" title="caDesign"></a>

* 使用第一种方式计算核密度估计，并存储为栅格数据

注意在定义字段名时，如果写入.shp格式数据后，字段名有可能被裁切，例如如果定义字段名为“amenity_kde”，那么用geopandas存储为.shp后，字段名可能被裁切为"amenity_kd"，如果读取该数据，不注意字段名的变化，可能带来不易察觉的错误。

```python
import pandas as pd
import numpy as np
from scipy import stats
pd.options.mode.chained_assignment = None

start_time=util.start_time()
poi_coordinates=np.array([amenity_poi.geometry.x,amenity_poi.geometry.y])
amenity_kernel=stats.gaussian_kde(poi_coordinates) #核密度估计
amenity_poi['amenityKDE']=amenity_kernel(poi_coordinates) 
util.duration(start_time)
```

```
start time: 2020-07-12 15:45:02.394814
end time: 2020-07-12 15:45:25.106516
Total time spend:0.37 minutes
```

```python
import geopandas as gpd
from pyproj import CRS
import os
print("original projection:",amenity_poi.crs)
amenity_poi_copy=amenity_poi.copy(deep=True)
amenity_poi_copy=amenity_poi.to_crs(CRS("EPSG:32616"))  #EPSG:32616 - WGS 84 / UTM zone 16N - Projected
print("re-projecting:",amenity_poi_copy.crs)

amenity_kde_fn='./data/geoData/amenity_kde.shp'
amenity_poi_copy.to_file(amenity_kde_fn)

raster_path=r'./data/geoData/amenity_kde.tif'
cellSize=300
field_name='amenityKDE' 
amenityKDE_array=util.pts2raster(amenity_kde_fn,raster_path,cellSize,field_name)
print("finished kde computing.")
```

```
original projection: epsg:4326
re-projecting: EPSG:32616
finished kde computing.
```

<a href=""><img src="./imgs/5_12.jpg" height="auto" width="auto" title="caDesign"></a>

* 使用第二种方法计算核密度估计并存储为连续的栅格值

```python
import util 
import rasterio
start_time=util.start_time()
raster_path=r'./data/geoData/amenity_G_kde.tif'
cellSize=500
scale=10**10 
amenity_G_kde=util.pts_geoDF2raster(amenity_poi_copy,raster_path,cellSize,scale)
util.duration(start_time)
```

```
start time: 2020-07-12 16:36:33.980935
Start calculating kde...
Finish calculating kde!
conversion complete!
end time: 2020-07-12 16:41:04.800500
Total time spend:4.50 minutes
```

```python
from rasterio.plot import show
import matplotlib.pyplot as plt
amenity_kde=rasterio.open(raster_path)
plt.figure(figsize=(10,15))
show((amenity_kde,1),cmap='Greens') 
plt.show()
```

<a href=""><img src="./imgs/5_13.png" height="auto" width="auto" title="caDesign"></a>

### 1.3 要点
#### 1.3.1 数据处理技术

* numpy处理技术汇总

1. 数据的建立

-创建等差数列，
`x=np.linspace(stats.norm.ppf(0.001,loc=0,scale=1),stats.norm.ppf(0.999,loc=0,scale=1), 100)` # numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0)

2. 数据组织

-排序数组 
`rVar_sort=np.sort(random_variates)` #numpy.sort(a, axis=-1, kind=None, order=None)

-垂直按顺序堆叠数组
`values=np.vstack([pts_geoDF.geometry.x, pts_geoDF.geometry.y]) `

-更新数组结构（shape）
`Z=np.reshape(kernel(positions).T, X.shape)` #numpy.flip(m, axis=None)

-翻转数组
`np.flip(Z,0)`

* GDAL库，处理地理空间数据，包括栅格raster、栅格vector以及坐标投影系统等

* raster库，简便的栅格数据处理库

#### 1.3.2 新建立的函数
* function - 将.shp格式的点数据转换为.tif栅格(raster)，`pts2raster(pts_shp,raster_path,cellSize,field_name=False)`

* function - 将GeoDaraFrame格式的点数据转换为栅格数据， `pts_geoDF2raster(pts_geoDF,raster_path,cellSize,scale)`

#### 1.3.3 所调用的库

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import math
import pandas as pd
import plotly.express as px
import geopandas as gpd
from pyproj import CRS
import os
from osgeo import gdal, ogr,osr
import rasterio
from rasterio.plot import show
```