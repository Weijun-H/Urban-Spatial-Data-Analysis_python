# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:58:43 2017 @author: Richie Bao-caDesign设计(cadesign.cn) __+updated Tue Jun 16 14:26:28 2020 by Richie Bao
"""
import urllib, json, csv,os,pathlib
import coordinate_transformation as cc
import geopandas as gpd
from shapely.geometry import Point

def baiduPOI_dataCrawler(query_dic,bound_coordinate,partition,page_num_range,poi_fn_list=False):
    '''function-百度地图开放平台POI数据爬取'''
    urlRoot='http://api.map.baidu.com/place/v2/search?' #数据下载网址，查询百度地图服务文档
    #切分检索区域
    xDis=(bound_coordinate['rightTop'][0]-bound_coordinate['leftBottom'][0])/partition
    yDis=(bound_coordinate['rightTop'][1]-bound_coordinate['leftBottom'][1])/partition    
    #判断是否要写入文件
    if poi_fn_list:
        for file_path in poi_fn_list:
            fP=pathlib.Path(file_path)
            if fP.suffix=='.csv':
                poi_csv=open(fP,'w',encoding='utf-8')
                csv_writer=csv.writer(poi_csv)    
            elif fP.suffix=='.json':
                poi_json=open(fP,'w',encoding='utf-8')
    num=0
    jsonDS=[] #存储读取的数据，用于.json格式数据的保存
    #循环切分的检索区域，逐区下载数据
    print("Start downloading data...")
    for i in range(partition):
        for j in range(partition):
            leftBottomCoordi=[bound_coordinate['leftBottom'][0]+i*xDis,bound_coordinate['leftBottom'][1]+j*yDis]
            rightTopCoordi=[bound_coordinate['leftBottom'][0]+(i+1)*xDis,bound_coordinate['leftBottom'][1]+(j+1)*yDis]
            for p in page_num_range:  
                #更新请求参数
                query_dic.update({'page_num':str(p),
                                  'bounds':str(leftBottomCoordi[1]) + ',' + str(leftBottomCoordi[0]) + ','+str(rightTopCoordi[1]) + ',' + str(rightTopCoordi[0]),
                                  'output':'json',
                                 })
                
                url=urlRoot+urllib.parse.urlencode(query_dic)
                data=urllib.request.urlopen(url)
                responseOfLoad=json.loads(data.read()) 
                if responseOfLoad.get("message")=='ok':
                    results=responseOfLoad.get("results") 
                    for row in range(len(results)):
                        subData=results[row]
                        baidu_coordinateSystem=[subData.get('location').get('lng'),subData.get('location').get('lat')] #获取百度坐标系
                        Mars_coordinateSystem=cc.bd09togcj02(baidu_coordinateSystem[0], baidu_coordinateSystem[1]) #百度坐标系-->火星坐标系
                        WGS84_coordinateSystem=cc.gcj02towgs84(Mars_coordinateSystem[0],Mars_coordinateSystem[1]) #火星坐标系-->WGS84
                        if csv_writer:
                            csv_writer.writerow([subData]) #逐行写入.csv文件
                        jsonDS.append(subData)
            num+=1       
            print("No."+str(num)+" was written to the .csv file.")
    if poi_json:       
        json.dump(jsonDS,poi_json)
        poi_json.write('\n')
        poi_json.close()
    if poi_csv:
        poi_csv.close()
    print("The download is complete.")
    return jsonDS
   
import pandas as pd
from benedict import benedict #benedict库是dict的子类，支持键列表（keylist）/键路径（keypath），应用该库的flatten方法展平嵌套的字典，准备用于DataFrame数据结构
def csv2df(poi_fn_csv):
    '''function-转换.csv格式的POI数据为pandas的DataFrame'''
    n=0
    with open(poi_fn_csv, newline='',encoding='utf-8') as csvfile:
        poi_reader=csv.reader(csvfile)
        poi_dict={}    
        poiExceptions_dict={}
        for row in poi_reader:    
            if row:
                try:
                    row_benedict=benedict(eval(row[0])) #用eval方法，将字符串字典"{}"转换为字典{}
                    flatten_dict=row_benedict.flatten(separator='_') #展平嵌套字典
                    poi_dict[n]=flatten_dict
                except:                    
                    print("incorrect format of data_row number:%s"%n)                    
                    poiExceptions_dict[n]=row
            n+=1
            #if n==5:break #因为循环次数比较多，在调试代码时，可以设置停止的条件，节省时间与方便数据查看
    poi_df=pd.concat([pd.DataFrame(poi_dict[d_k].values(),index=poi_dict[d_k].keys(),columns=[d_k]).T for d_k in poi_dict.keys()], sort=True,axis=0)
    print("_"*50)
    for col in poi_df.columns:
        try:
            poi_df[col]=pd.to_numeric(poi_df[col])
        except:
            print("%s data type is not converted..."%(col))
    print("_"*50)
    print(".csv to DataFrame is completed!")
    #print(poi_df.head()) #查看最终DataFrame格式下POI数据
    #print(poi_df.dtypes) #查看数据类型
    return poi_df

if __name__=="__main__": 
    data_path='./data' #配置数据存储位置
    #定义存储文件名
    poi_fn_csv=os.path.join(data_path,'poi_csv.csv')
    poi_fn_json=os.path.join(data_path,'poi_json.json')
    
    bound_coordinate={'leftBottom':[108.776852,34.186027],'rightTop':[109.129275,34.382171]} #
    page_num_range=range(20)
    partition=3
    query_dic={
        'query':'旅游景点',
        'page_size':'20',
        'scope':2,
        'ak':'uqRcWhrQ6h0pAaSdxYn73GMWgd5uNrRX',
    }
    jsonDS=baiduPOI_dataCrawler(query_dic,bound_coordinate,partition,page_num_range,poi_fn_list=[poi_fn_csv,poi_fn_json]) 

    poi_df=csv2df(poi_fn_csv)
    poi_fn_df=os.path.join(data_path,'poi_df.pkl')
    poi_df.to_pickle(poi_fn_df)
    print("_"*50)
    print(poi_df.head())
    
    poi_df=pd.read_pickle(poi_fn_df) #读取已经保存的.pkl(pickle)数据格式的POI
    
    poi_geoDF=poi_df.copy(deep=True)
    poi_geoDF['geometry']=poi_geoDF.apply(lambda row:Point(row.location_lng,row.location_lat),axis=1) 
    crs={'init': 'epsg:4326'} #配置坐标系统，参考：https://spatialreference.org/  
    poi_gpd=gpd.GeoDataFrame(poi_geoDF,crs=crs)
    poi_gpd.plot(column='detail_info_comment_num') #在这里设置了显示的参数为列`detail_info_comment_num`,即对<'query':'旅游景点'>配置中旅游景点的评论数量
    
    import plotly.express as px
    poi_gpd.detail_info_price=poi_gpd.detail_info_price.fillna(0) #pandas库的方法同样适用于geopandas库，例如对`nan`位置填充指定数值
    mapbox_token='pk.eyJ1IjoicmljaGllYmFvIiwiYSI6ImNrYjB3N2NyMzBlMG8yc254dTRzNnMyeHMifQ.QT7MdjQKs9Y6OtaJaJAn0A'
    px.set_mapbox_access_token(mapbox_token)
    fig=px.scatter_mapbox(poi_gpd,lat=poi_gpd.location_lat, lon=poi_gpd.location_lng,color="detail_info_comment_num",color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10) #亦可以选择列，通过size=""配置增加显示信息
    fig.show()
    
    from plotly.offline import plot
    plot(fig)