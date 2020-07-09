# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:30:49 2020

@author: richi
"""
import osmium as osm
import pandas as pd
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

#osm_Chicago_fp=r"F:\GitHubBigData\osm_small_clip.osm" #待读取的.osm数据路径, 用提取的小范围数据调试代码
osm_Chicago_fp=r"F:\GitHubBigData\osm_clip.osm" #用小批量数据调试完之后，计算实际的实验数据

osm_handler=osmHandler() #实例化类osmHandler()
osm_handler.apply_file(osm_Chicago_fp,locations=True) #调用 class osmium.SimpleHandler的apply_file方法
print("finished reading OSM data.")

import geopandas as gpd
import os
crs={'init': 'epsg:4326'} #配置坐标系统，参考：https://spatialreference.org/        
osm_columns=['type','geometry','id','version','visible','ts','uid','user','changeet','tagLen','tags']
osm_node_gdf=gpd.GeoDataFrame(osm_handler.osm_node,columns=osm_columns,crs=crs)
osm_way_gdf=gpd.GeoDataFrame(osm_handler.osm_way,columns=osm_columns,crs=crs)
osm_area_gdf=gpd.GeoDataFrame(osm_handler.osm_area,columns=osm_columns,crs=crs)

save_path=r"./data/"
osm_node_gdf.to_file(os.path.join(save_path,"osm_node.geojson"),driver='GeoJSON')
osm_way_gdf.to_file(os.path.join(save_path,"osm_way.geojson"),driver='GeoJSON')
osm_area_gdf.to_file(os.path.join(save_path,"osm_area.geojson"),driver='GeoJSON')
print("finished saving OSM data.")