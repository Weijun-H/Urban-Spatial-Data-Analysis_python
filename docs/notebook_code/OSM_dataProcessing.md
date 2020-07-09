> Created on Fri Dec 27 14/28/05 2019 @author: Richie Bao-caDesign设计(cadesign.cn) __+updated on Mon Jul  6 19/29/41 2020

## 1.OpenStreetMap（OSM）数据处理
[OpenStreetMap(OSM)](https://www.openstreetmap.org/#map=13/41.8679/-87.6569),"欢迎访问OpenStreetMap,这是个为全世界创建和分发免费地理数据的项目。我们之所以这么做，是因为人们认为作为免费的地图，在使用方面实际上有法律或者技术上的限制，阻碍了人们以创作性的、多产的、或意想不到的方式使用它们"。OSM提供了世界各地的道路、小径、咖啡馆、火车站等诸多地理信息数据，是我们在城市空间方面研究的宝贵数据财富。OSM数据的下载查看其官网信息，一般来讲有两个途径，一个是直接下载显示窗口范围的数据，或输入坐标自定义范围，但是这种方式下载的数据量有限制，如果范围过大则无法下载；另一种方式是直接从资源库下载，不同的资源下载的方式也有所不同，根据自己的需要来确定。同时OSM提供了多年历史数据，这为城市空间变化的研究提供了数据支持。本次所下载的数据从[Geofabrik](https://download.geofabrik.de/north-america/us.html)库中下载，因为分析的目标区域为芝加哥城，下载了[llinois-latest-free.shp.zip](https://download.geofabrik.de/north-america/us/illinois.html)压缩文件340MB，解压后3.73GB，根据下载后点数据的分布情况，为了保持点连续的区域，增加下载[wisconsin-latest.osm.bz2](https://download.geofabrik.de/north-america/us/wisconsin.html)数据文件324MB，解压后3.73GB。可以使用QGIS初步查看数据。其包含的数据层有：lines，multilinestrings，multipolygons，other_relations 和points。

> 下图同时打开了了Ilinois和wisconsin的点数据，内部红色半透明区域为[芝加哥城行政范围](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-City/ewy2-6yfk)，数据来源于[Chicago Data Portal](https://data.cityofchicago.org/). 外部红色虚线为实验数据提取的实际边界。最小的黑色矩形是用于代码调试提取小规模数据。

<a href=""><img src="./imgs/4_6.jpg" height="auto" width="500" title="caDesign"></a>

### 1.1 OSM原始数据处理
.osm数据处理包括合并两个区域数据，以及裁切，或者先分别裁切再合并，可以根据电脑内存需求和处理速度确定前后顺序。裁切.osm数据。这里选用的裁切方法是使用[osmosis](https://wiki.openstreetmap.org/wiki/Osmosis)命令行工具，非常适合处理大数据文件，裁切和更新数据。同时可以参考[Manipulating Data with Osmosis](https://learnosm.org/en/osm-data/osmosis/)。查询osmosis给出的案例，寻找应用polygon提取数据的代码为：`osmosis --read-xml file="planet-latest.osm" --bounding-polygon file="country2pts.txt" --write-xml file="germany.osm"`，共涉及到三个参数，原始.osm数据；裁切边界polygon（.txt数据格式），需要注意该处的polygon为osmosis格式的polygon格式数据，需要编写转换代码；以及输出路径。

目视粗略判断点集聚的范围，在QGIS中绘制常规的polygon边界，如上图外红色虚线。首先编写polygon到osmosis格式的polygon代码，查询其数据格式为：
```
australia_v
first_area
     0.1446693E+03    -0.3826255E+02
     0.1446627E+03    -0.3825661E+02
     0.1446763E+03    -0.3824465E+02
     0.1446813E+03    -0.3824343E+02
     0.1446824E+03    -0.3824484E+02
     0.1446826E+03    -0.3825356E+02
     0.1446876E+03    -0.3825210E+02
     0.1446919E+03    -0.3824719E+02
     0.1447006E+03    -0.3824723E+02
     0.1447042E+03    -0.3825078E+02
     0.1446758E+03    -0.3826229E+02
     0.1446693E+03    -0.3826255E+02
END
second_area
     0.1422436E+03    -0.3839315E+02
     0.1422496E+03    -0.3839070E+02
     0.1422543E+03    -0.3839025E+02
     0.1422574E+03    -0.3839155E+02
     0.1422467E+03    -0.3840065E+02
     0.1422433E+03    -0.3840048E+02
     0.1422420E+03    -0.3839857E+02
     0.1422436E+03    -0.3839315E+02
END
END
```

定义转换格式函数时，调用了osgeo类，该类包含于[GDAL](https://pypi.org/project/GDAL/)库中,GDAL是一个用于栅格（raster）和矢量（vector）地理空间数据格式的开源转换库，包含大量格式驱动，大多数python的地理空间数据处理库通常基于GDAL为底层编写，是最为基础的库。geopandas库基于fiona库，方便用户对地理空间数据的处理，而fiona包含链接到GDAL的扩展模块。通常在使用python地理空间数据库时，并没有使用哪个库的限制，目前最快处理地理空间数据的库是geopandas，但是有时这些库满足不了所有要求，因此需要调用GDAL来处理。查看GDAL帮助信息，可以浏览[GDAL/OGR Cookbook!](http://pcjericks.github.io/py-gdalogr-cookbook/index.html)，以及[GDAL documentation](https://gdal.org/)


```python
def shpPolygon2OsmosisTxt(shape_polygon_fp,osmosis_txt_fp): 
    from osgeo import ogr #osgeo包含在GDAL库中
    '''
    function-转换shape的polygon为osmium的polygon数据格式（.txt），用于.osm地图数据的裁切
    
    Params:
    shape_polygon_fp - 输入shape地理数据格式的polygon
    osmosis_txt_fp - 输出为osmosis格式的polygon数据格式.txt
    '''
    driver=ogr.GetDriverByName('ESRI Shapefile') #GDAL能够处理众多地理数据格式，此时调入了ESRI Shapefile数据格式驱动
    infile=driver.Open(shape_polygon_fp) #打开.shp文件
    layer=infile.GetLayer() #读取层
    f=open(osmosis_txt_fp,"w") 
    f.write("osmosis polygon\nfirst_area\n")
    
    for feature in layer: 
        feature_shape_polygon=feature.GetGeometryRef() 
        print(feature_shape_polygon) #为polygon
        firsts_area_linearring=feature_shape_polygon.GetGeometryRef(0) #polygon不包含嵌套，为单独的形状
        print(firsts_area_linearring) #为linearRing
        area_vertices=firsts_area_linearring.GetPointCount() #提取linearRing对象的点数量
        for vertex in range(area_vertices): #循环点，并向文件中写入点坐标
            lon, lat, z=firsts_area_linearring.GetPoint(vertex)  
            f.write("%s  %s\n"%(lon,lat))
    f.write("END\nEND")  
    f.close()   
#转换实际实验边界
shape_polygon_fp=r'.\data\geoData\OSMBoundary.shp'
osmosis_txt_fp=r'.\data\geoData\OSMBoundary.txt'
shpPolygon2OsmosisTxt(shape_polygon_fp,osmosis_txt_fp)

#转换代码调试小批量数据边界
shape_polygon_small_fp=r'.\data\geoData\OSMBoundary_small.shp'
osmosis_txt_small_fp=r'.\data\geoData\OSMBoundary_small.txt'
shpPolygon2OsmosisTxt(shape_polygon_small_fp,osmosis_txt_small_fp)
```

    POLYGON ((-90.0850881031402 40.9968994947319,-90.0850881031402 43.6657936592248,-87.383039973871 43.6657936592248,-87.383039973871 40.9968994947319,-90.0850881031402 40.9968994947319))
    LINEARRING (-90.0850881031402 40.9968994947319,-90.0850881031402 43.6657936592248,-87.383039973871 43.6657936592248,-87.383039973871 40.9968994947319,-90.0850881031402 40.9968994947319)
    POLYGON ((-87.6807286451907 41.8373927809521,-87.6807286451907 41.9214101975252,-87.5941157249019 41.9214101975252,-87.5941157249019 41.8373927809521,-87.6807286451907 41.8373927809521))
    LINEARRING (-87.6807286451907 41.8373927809521,-87.6807286451907 41.9214101975252,-87.5941157249019 41.9214101975252,-87.5941157249019 41.8373927809521,-87.6807286451907 41.8373927809521)
    

执行转换后，写入.txt格式文件的实际实验边界polygon如下：
```
osmosis polygon
first_area
-90.08508810314017  40.99689949473193
-90.08508810314017  43.66579365922478
-87.38303997387102  43.66579365922478
-87.38303997387102  40.99689949473193
-90.08508810314017  40.99689949473193
END
END
```

用于调试小批量数据提取的.txt边界：
```
osmosis polygon
first_area
-87.68072864519071  41.83739278095207
-87.68072864519071  41.92141019752525
-87.59411572490187  41.92141019752525
-87.59411572490187  41.83739278095207
-87.68072864519071  41.83739278095207
END
END
```

osmosis也提供多个.osm地理空间数据的合并，其合并示例代码为`osmosis --rx 1.osm --rx 2.osm --rx 3.osm --merge --wx merged.osm`. 首先执行合并操作，针对该实验的osmosis合并代码`osmosis --rx "F:/GitHubBigData/illinois-latest.osm" --rx "F:/GitHubBigData/wisconsin-latest.osm"--merge --wx "F:/GitHubBigData/illinois-wisconsin.osm"`，合并后的文件大小为7.57GB。再执行裁切命令`osmosis --read-xml file="F:\GitHubBigData\illinois-wisconsin.osm" --bounding-polygon file="C:\Users\richi\omen-richiebao\omen_github\Urban-Spatial-Data-Analysis_python\notebook\BaiduMapPOIcollection_ipynb\data\geoData\OSMBoundary.txt" --write-xml file="F:\GitHubBigData\osm_clip.osm"`，裁切后的文件大小为3.80GB。可以再通过QGIS查看数据是否已经按照预期合并裁切完毕。用于代码调试的小规模数据提取直接裁切`osmosis --read-xml file="F:\GitHubBigData\illinois-wisconsin.osm" --bounding-polygon file="C:\Users\richi\omen-richiebao\omen_github\Urban-Spatial-Data-Analysis_python\notebook\BaiduMapPOIcollection_ipynb\data\geoData\OSMBoundary_small.txt" --write-xml file="F:\GitHubBigData\osm_small_clip.osm"`。

> osmosis命令行，于windows系统的命令行终端中执行，建议在[Windows PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-7)终端中执行代码。

<a href=""><img src="./imgs/4_5.jpg" height="auto" width="auto" title="caDesign"></a>

OSM使用附加在基本数据结构上的标签（tag）来表示地面上的物理特征（feature），例如道路或者建筑物等。在QGIS中打开属性表，可以查看各要素所属于的标签。对于具体标签的内容可以查看[Map Features](https://wiki.openstreetmap.org/wiki/Map_Features)，下面仅列出主要标签的分类：

| 序号   |      一级标签      |  二级标签 |
|----------|:-------------|------:|
| 1 |   Aerialway |  |
| 2 |     Aeroway   |   |
| 3 |  Amenity |     Sustenance,Education,  Transportation, Financial, Healthcare, Entertainment, Arts & Culture, Others|
|4| Barrier| Linear barriers, Access control on highways|
| 5 |  Boundary |Attributes   |
| 6| Building |  Accommodation, Commercial, Religious,Civic/Amenity, Agricultural/Plant production, Sports,Storage,Cars, Power/Technical buildings,Other Buildings, Additional Attributes|
| 7 | Craft |   |
| 8 | Emergency | Medical Rescue,Firefighters, Lifeguards,  Assembly point,Other Structure |
| 9 |  Geological |   |
| 10 | Highway |  Roads, Link roads, Special road types, Paths,Lifecycle, Attributes,Other highway features|
| 11 | Historic |   |
| 12 | Landuse | Common Landuse Key Values - Developed land, Common Landuse Key Values - Rural and agricultural land, Other Landuse Key Values |
| 13 | Leisure |   |
| 14 |  Man_made |   |
| 15 | Military |   |
| 16 | Natural |  Vegetation or surface related, Water related, Landform related |
| 17 |Office  |   |
| 18 | Place | Administratively declared places,   Populated settlements, urban,Populated settlements, urban and rural, Other places|
| 19 |  Power |  Public Transport |
| 20 | Public Transport |  |
| 21 | Railway |  Tracks, Additional features, Stations and Stops, Other railways|
| 22 | Route |   |
| 23 | Shop | Food, beverages,  General store, department store, mall,  Clothing, shoes, accessories, Discount store, charity, Health and beauty, Do-it-yourself, household, building materials, gardening, Furniture and interior, Electronics, Outdoors and sport, vehicles, Art, music, hobbies,Stationery, gifts, books, newspapers, Others|
| 24 | Sport  |   |
| 25 |  Telecom |   |
| 26 |Tourism  |   |
| 27 |  Waterway | Natural watercourses, Man-made waterways, Facilities,Barriers on waterways,Other features on waterways|
| Additional properties |  |   |
| 1 | Addresses | Tags for individual houses, For countries using hamlet, subdistrict, district, province, state, Tags for interpolation ways |
| 2 | Annotation  |   |
| 3 | Name |   |
| 4 | Properties  |   |
| 5 | References  |   |
| 6 | Restrictions  |   |


> osmosis 工具是由OSM及其开源社区成员所建立的[osmcode.org](https://osmcode.org/)开发的工具。

### 1.2 读取、转换.osm数据
用python读取.osm数据仍然使用[osmcode.org](https://osmcode.org/)提供的工具[pyosmium](https://docs.osmcode.org/pyosmium/latest/), pyosmium是处理不同格式的OSM文件，内核为c++的osmium库，能够有效快速的处理OSM数据。上述处理后的.osm数据文件osm_clip.osm为3.80GB，如果一开始就使用较大的数据来编写程序，花费的时间成本可能较高，可以给更少的数据编写、调试，达到预期效果后再使用待要分析的大文件数据。

编写读取.osm数据，需要对OSM的数据结构有所了解，从而能够清晰的提取所需要的值。[元素（elements）](https://wiki.openstreetmap.org/wiki/Elements)是OSM物理世界概念数据模型的基本组成部分，包括节点nodes、路径或区域ways、关系relations，以及其标签tag。

| 元素（elements）   |      图标     |  解释 |对位shape地理空间数据（vector矢量）|
|----------|:-------------|------:|------:|
| node |   <a href=""><img src="./imgs/30px-Osm_element_node.svg.png" height="auto" width="auto" title="caDesign"></a> |由经纬度坐标定义的地理空间点  |point|
| way |    <a href=""><img src="./imgs/30px-Osm_element_way.svg.png" height="auto" width="auto" title="caDesign"></a><a href=""><img src="./imgs/30px-Osm_element_closedway.svg.png" height="auto" width="auto" title="caDesign"></a><a href=""><img src="./imgs/30px-Osm_element_area.svg.png" height="auto" width="auto" title="caDesign"></a>   | 由点(20-2000个)构成的路径以及闭合的区域，包含open way, closed way和area  |polyline,polygon|
| relation |     <a href=""><img src="./imgs/30px-Osm_element_relation.svg.png" height="auto" width="auto" title="caDesign"></a>   | 记录两个或多个元素之间关系的多用途数据结构，关系可以有不同的含义，其意义由对应的标签定义  ||
| tag|  <a href=""><img src="./imgs/30px-Osm_element_tag.svg.png" height="auto" width="auto" title="caDesign"></a>   | nodes、ways和relations都可以由描述其意义的标签，一个标签由键key:值value组成，Key必须是唯一的  |字段 field|

* 示例

**node**
```html
<node id="25496583" lat="51.5173639" lon="-0.140043" version="1" changeset="203496" user="80n" uid="1238" visible="true" timestamp="2007-01-28T11:40:26Z">
    <tag k="highway" v="traffic_signals"/>
</node>
```

**way**

简单的路径或区域 simple way
```html
  <way id="5090250" visible="true" timestamp="2009-01-19T19:07:25Z" version="8" changeset="816806" user="Blumpsy" uid="64226">
    <nd ref="822403"/>
    <nd ref="21533912"/>
    <nd ref="821601"/>
    <nd ref="21533910"/>
    <nd ref="135791608"/>
    <nd ref="333725784"/>
    <nd ref="333725781"/>
    <nd ref="333725774"/>
    <nd ref="333725776"/>
    <nd ref="823771"/>
    <tag k="highway" v="residential"/>
    <tag k="name" v="Clipstone Street"/>
    <tag k="oneway" v="yes"/>
  </way>
```

多边形区域集合 multipolygon area

<img src="./imgs/300px-Multipolygon_Illustration_2.svg.png" height="auto" width="auto" title="caDesign"><img src="./imgs/300px-Multipolygon_Illustration_1b.svg.png" height="auto" width="auto" title="caDesign">

```html
  <relation id="12" timestamp="2008-12-21T19:31:43Z" user="kevjs1982" uid="84075">
    <member type="way" ref="2878061" role="outer"/> <!-- picture ref="1" -->
    <member type="way" ref="8125153" role="inner"/> <!-- picture ref="2" -->
    <member type="way" ref="8125154" role="inner"/> <!-- picture ref="3" -->

    <member type="way" ref="3811966" role=""/> <!-- empty role produces
        a warning; avoid this; most software works around it by computing
        a role, which is more expensive than having one set explicitly;
        not shown in the sample pictures to the right -->

    <tag k="type" v="multipolygon"/>
  </relation>
```




* 元素的属性

| 名称   | 值类型          |  解释 |
|----------|:-------------|------:|
| id |integer (64-bit)   | 用于表示元素 |
| user |character string   | 最后修改对象的用户名 |
| uid | integer | 最后修改对象的用户ID |
| timestamp | W3C standard date and time  | 最后修改时间 |
|visible  | "true" or "false"  | 数据库中的对象是否被删除 |
|version  | integer  | 版本控制 |
|changeset  | integer  |创建或更新对象时使用的变更集编号  |

了解了OSM基本的数据类型、结构和属性，通过继承osmium的类.SimpleHandler，用.apply_file方法传入.osm文件，并定义所要提取的元素类型，并给出该元素类型的属性提取对应的属性值。在地理空间数据分析中，通常比较关键的属性包括：,元素修改的最后时间（.timestamp），标签（tags,<tag.k,tag.v>）,生成的几何对象（geometry<point,linestring,multipolygon>）。下述函数分别提取了node, way(area)对象的属性和几何对象，同时将其转换为GeoDataFrame的数据格式，并存储为`GPKG`的格式数据，方便日后调用，尤其大批量数据。因为涉及到大批量数据，因此调入datatime时间模块，观察所用时间，帮助调试代码。


```python
import osmium as osm
import pandas as pd
import datetime
import shapely.wkb as wkblib
wkbfab=osm.geom.WKBFactory()

class osmHandler(osm.SimpleHandler):    
    '''
    class-通过继承osmium类 class osmium.SimpleHandler读取.osm数据. 
    '''
    
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_node=[]
        self.osm_way=[]
        self.osm_area=[]
        
    def node(self,n):
        wkb=wkbfab.create_point(n)
        point=wkblib.loads(wkb,hex=True)
        self.osm_node.append([
            'node',
            point,
            n.id,
            n.version,
            n.visible,
            pd.Timestamp(n.timestamp),
            n.uid,
            n.user,
            n.changeset,
            len(n.tags),
            {tag.k:tag.v for tag in n.tags},
            ])

    def way(self,w):     
        try:
            wkb=wkbfab.create_linestring(w)
            linestring=wkblib.loads(wkb, hex=True)
            self.osm_way.append([
                'way',
                linestring,
                w.id,
                w.version,
                w.visible,
                pd.Timestamp(w.timestamp),
                w.uid,
                w.user,
                w.changeset,
                len(w.tags),
                {tag.k:tag.v for tag in w.tags}, 
                ])
        except:
            pass
        
    def area(self,a):     
        try:
            wkb=wkbfab.create_multipolygon(a)
            multipolygon=wkblib.loads(wkb, hex=True)
            self.osm_area.append([
                'area',
                multipolygon,
                a.id,
                a.version,
                a.visible,
                pd.Timestamp(a.timestamp),
                a.uid,
                a.user,
                a.changeset,
                len(a.tags),
                {tag.k:tag.v for tag in a.tags}, 
                ])
        except:
            pass      
        
a_T=datetime.datetime.now()
print("start time:",a_T)
#osm_Chicago_fp=r"F:\GitHubBigData\osm_small_clip.osm" #待读取的.osm数据路径, 用提取的小范围数据调试代码
osm_Chicago_fp=r"F:\GitHubBigData\osm_clip.osm" #用小批量数据调试完之后，计算实际的实验数据

osm_handler=osmHandler() #实例化类osmHandler()
osm_handler.apply_file(osm_Chicago_fp,locations=True) #调用 class osmium.SimpleHandler的apply_file方法
b_T=datetime.datetime.now()
print("end time:",b_T)
duration=(b_T-a_T).seconds/60
print("Total time spend:%.2f minutes"%duration)
```

    start time: 2020-07-08 16:38:01.285606
    end time: 2020-07-08 17:12:23.316155
    Total time spend:34.37 minutes
    

当读取全部OSM元素数据后，定义保存函数，如果是小批量数据，通常可以一起保存，但是本次实验数据有3.80GB，将读取后的数据转换为GeoDataFrame数据格式，并保存较为花费时间。因此将OSM元素逐个转换保存。同时，注意到在小批量调试时，保存node为GeoJSON格式文件其大小为104MB，而保存为GPKG仅有52.3MB，因此对于实验数据的保存，这里选择后者。


```python
def save_osm(osm_handler,osm_type,save_path=r"./data/",fileType="GPKG"):
    a_T=datetime.datetime.now()
    print("start time:",a_T)
    import geopandas as gpd
    import os
    import datetime
    '''
    function-根据条件逐个保存读取的osm数据（node, way and area）
    
    Paras:
    osm_handler - osm返回的node,way和area数据
    osm_type - 要保存的osm元素类型
    save_path - 保存路径
    fileType - 保存的数据类型，shp, GeoJSON, GPKG
    '''
    def duration(a_T):
        b_T=datetime.datetime.now()
        print("end time:",b_T)
        duration=(b_T-a_T).seconds/60
        print("Total time spend:%.2f minutes"%duration)
        
    def save_gdf(osm_node_gdf,fileType,osm_type):
        if fileType=="GeoJSON":
            osm_node_gdf.to_file(os.path.join(save_path,"osm_%s.geojson"%osm_type),driver='GeoJSON')
        elif fileType=="GPKG":
            osm_node_gdf.to_file(os.path.join(save_path,"osm_%s.gpkg"%osm_type),driver='GPKG')
        elif fileType=="shp":
            osm_node_gdf.to_file(os.path.join(save_path,"osm_%s.shp"%osm_type))

    crs={'init': 'epsg:4326'} #配置坐标系统，参考：https://spatialreference.org/        
    osm_columns=['type','geometry','id','version','visible','ts','uid','user','changeet','tagLen','tags']
    if osm_type=="node":
        osm_node_gdf=gpd.GeoDataFrame(osm_handler.osm_node,columns=osm_columns,crs=crs)
        save_gdf(osm_node_gdf,fileType,osm_type)
        duration(a_T)
        return osm_node_gdf

    elif osm_type=="way":
        osm_way_gdf=gpd.GeoDataFrame(osm_handler.osm_way,columns=osm_columns,crs=crs)
        save_gdf(osm_way_gdf,fileType,osm_type)
        duration(a_T)
        return osm_way_gdf
        
    elif osm_type=="area":
        osm_area_gdf=gpd.GeoDataFrame(osm_handler.osm_area,columns=osm_columns,crs=crs)
        save_gdf(osm_area_gdf,fileType,osm_type)
        duration(a_T)
        return osm_area_gdf
```


```python
node_gdf=save_osm(osm_handler,osm_type="node",save_path=r"./data/",fileType="GPKG")
```

    start time: 2020-07-08 17:13:45.751609
    end time: 2020-07-08 18:40:34.442122
    Total time spend:86.80 minutes
    


```python
way_gdf=save_osm(osm_handler,osm_type="way",save_path=r"./data/",fileType="GPKG")
```

    start time: 2020-07-08 18:45:26.586573
    end time: 2020-07-08 18:57:58.356928
    Total time spend:12.52 minutes
    


```python
area_gdf=save_osm(osm_handler,osm_type="area",save_path=r"./data/",fileType="GPKG")
```

    start time: 2020-07-08 18:59:12.339119
    end time: 2020-07-08 19:09:24.169272
    Total time spend:10.18 minutes
    

在存储过程中，该部分实验数据，node元素存储时间约87分钟，存储的GPKG文件大小为3.10GB，way和area元素则相对存储时间较短，存储文件较小。因为已经转换为GeoDataFrame格式地理空间数据格式，因此可以直接.plot()查看数据分布情况，初步判断是否读取和转换正确。下述代码用来测试读取的时间，其中way和area读取时间较短，而node元素读取时间较长。


```python
def start_time():
    import datetime
    '''
    function-计算当前时间
    '''
    start_time=datetime.datetime.now()
    print("start time:",start_time)
    return start_time

def duration(start_time):
    import datetime
    '''
    function-计算持续时间
    
    Paras:
    start_time - 开始时间
    '''
    end_time=datetime.datetime.now()
    print("end time:",end_time)
    duration=(end_time-start_time).seconds/60
    print("Total time spend:%.2f minutes"%duration)
```


```python
import geopandas as gpd
start_time=start_time()
read_way_gdf=gpd.read_file("./data/osm_way.gpkg")
duration(start_time)
```

    start time: 2020-07-08 20:30:02.328322
    end time: 2020-07-08 20:31:51.139907
    Total time spend:1.80 minutes
    


```python
read_way_gdf.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x2508dff6c48>



<img src="./imgs/4_1.png" height="auto" width="500" title="caDesign">

```python
del read_way_gdf #如果内存有限，可以使用del 删除不再使用的变量，从而节约内存
```


```python
start_time=start_time()
read_area_gdf=gpd.read_file("./data/osm_area.gpkg")
duration(start_time)
```

    start time: 2020-07-08 20:13:53.521419
    end time: 2020-07-08 20:16:28.547289
    Total time spend:2.58 minutes
    


```python
read_area_gdf.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x250ba44aa48>




<img src="./imgs/4_2.png" height="auto" width="500" title="caDesign">



```python
start_time=start_time()
read_node_gdf=gpd.read_file("./data/osm_node.gpkg")
duration(start_time)
```

    start time: 2020-07-08 20:32:25.929397
    end time: 2020-07-08 21:10:42.912870
    Total time spend:38.27 minutes
    


```python
read_node_gdf.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x250ba0ed308>




<img src="./imgs/4_3.png" height="auto" width="500" title="caDesign">


### 1.3 要点
#### 1.3.1 数据处理技术

* .osm数据处理库，由[osmcode.org](https://osmcode.org/)提供的[osmosis](https://wiki.openstreetmap.org/wiki/Osmosis)命令行工具处理原始数据，以及支持python语言处理的[pyosmium](https://docs.osmcode.org/pyosmium/latest/)库。

* python处理地理空间数据最基础的库GDAL

* 用datatime库获取时间，计算程序运行时间花费

* 用del variable的方法删除不使用的变量，节约内存空间

#### 1.3.2 新建立的函数

* function-转换shape的polygon为osmium的polygon数据格式（.txt），用于.osm地图数据的裁切，`shpPolygon2OsmosisTxt(shape_polygon_fp,osmosis_txt_fp)`

* class-通过继承osmium类 class osmium.SimpleHandler读取.osm数据, `osmHandler(osm.SimpleHandler)`

* function-根据条件逐个保存读取的osm数据（node, way and area）,`save_osm(osm_handler,osm_type,save_path=r"./data/",fileType="GPKG")`

* function-计算当前时间，`start_time()`

* function-计算持续时间, `duration(start_time)`

#### 1.3.3 所调用的python库


```python
from osgeo import ogr #osgeo包含在GDAL库中
import osmium as osm
import pandas as pd
import datetime
import shapely.wkb as wkblib
import geopandas as gpd
import os
```