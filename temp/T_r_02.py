# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 20:05:35 2020

@author: richi
"""
import pandas as pd

x=[-2.885181,
-2.520594,
11.186939,
-4.132826,
-2.408161,
-2.290709,
-0.8499,
10.33942,
11.491055,
-1.902486,
10.835322,
10.915261,
11.130595,
-2.45135,
5.679025,
12.835934,
-14.979823,
2.376486,
-18.020879,
-19.154666,
2.527985,
-10.301121,
-10.806695,
3.109815]

y=[9.246944,
-1.036282,
2.355666,
-16.075638,
-10.051387,
4.27457,
-22.883173,
10.864029,
-20.489098,
-20.443073,
-13.631979,
-3.591518,
-9.272599,
-5.709143,
17.830317,
9.55421,
19.680556,
-1.386281,
14.956038,
11.809355,
22.41266,
16.019896,
11.586121,
7.638207]
import rpy2
print(rpy2.__version__)    
from rpy2.rinterface import R_VERSION_BUILD
print(R_VERSION_BUILD)
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
#import spatial points pattern analysis
sp=importr("spatstat")
# import R's "base" package
base = importr('base')
# import R's "utils" package
utils = importr('utils')     
    
import pointpats.quadrat_statistics as qs
from shapely import *
from shapely.geometry import *
import libpysal as ps
import numpy as np
from pointpats import PointPattern



import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
packnames = ('pandas2ri','r')
# utils = rpackages.importr('utils')
# utils.install_packages(StrVector(packnames))

from rpy2.robjects import r, pandas2ri #C:\Users\richi\conda\envs\pyG\lib\site-packages\rpy2\robjects\pandas2ri.py:17: FutureWarning: pandas.core.index is deprecated and will be removed in a future version.  The public classes are available in the top-level namespace.  from pandas.core.index import Index as PandasIndex
from pandas.core.index import Index as PandasIndex




df=pd.DataFrame(zip(x,y),columns=["x","y"])


# def r_cal(df):
#     string = """
#     ptsPPP <- function(df) {
#         X <- with(df, ppp(x, y, c(-25,25), c(-25,25)))
#         #plot(X)
        
#         return(X)
#     }
#     """
#     sp = SignatureTranslatedAnonymousPackage(string, "powerpack")   
#     pandas2ri.activate()
#     r_DF=pandas2ri.py2ri(df[["x","y"]])
#     ptsPPP=sp.ptsPPP(r_DF)
#     print("+"*50)
#     print(ptsPPP)
#     return ptsPPP
    
# r_cal(df)

# import rpy2.robjects.packages as rpackages
# from rpy2.robjects.vectors import StrVector
# packnames = ('pandas2ri','r','devtools')
# utils = rpackages.importr('utils')
# utils.install_packages(StrVector(packnames))

def r_cal_b(df):
    robjects.r('''
        # create a function `f`
        f <- function(df, verbose=FALSE) {
            if (verbose) {
                cat("I am calling f().\n")
            }       
            xMin<-min(df$x)
            xMax<-max(df$x)
            yMin<-min(df$y)
            yMax<-max(df$y)
            
            
            #xy_PPP <- with(df, ppp(x, y, c(-25,25), c(-25,25)))
            xy_PPP <- with(df, ppp(x, y, c(xMin,xMax), c(yMin,yMax)))
            plot(xy_PPP)
            
            xy=df
            summary(xy)
            xy <- unique(xy)
            xy<-data.matrix(xy)
            mc <- apply(xy, 2, mean)    
            sd <- sqrt(sum((xy[,1] - mc[1])^2 + (xy[,2] - mc[2])^2) / nrow(xy))
            buffer_area=25*25
            dens <- nrow(xy) / buffer_area
            library(spatstat)
            win<-owin(c(-25,25), c(-25,25))

            #library(devtools)
            #if (!require("rspatial")) devtools::install_github('rspatial/rspatial')
            #remotes::install_github("rspatial/rspatial")

            #devtools::install_github("rspatial/rspatial")
            #devtools::install_github("rstudio/sparkapi")
            
            #library(rspatial)
            #r <- raster(win)
            quadrat_C<-quadratcount(xy_PPP,nx=4,ny=4)
            #plot(quadrat_C)
            # number of quadrats
            quadrats <- sum(quadrat_C)
            f<-table(quadrat_C)
            f<-data.frame(f)
            # number of cases
            cases <- sum(as.integer(f$quadrat_C) * f$Freq)
            mu <- cases / quadrats
            
            ff <- data.frame(as.integer(f$quadrat_C),f$Freq)
            colnames(ff) <- c('K', 'X')
            ff$Kmu <- ff$K - mu
            ff$Kmu2 <- ff$Kmu^2
            ff$XKmu2 <- ff$Kmu2 * ff$X
            s2 <- sum(ff$XKmu2) / (sum(ff$X)-1)
            VMR <- s2 / mu
            
            Fs<-Fest(xy_PPP)
            #plot(Fs)
            Gs<-Gest(xy_PPP)
            #plot(Gs)
            
            km<-Fs$km[10]
            newlist<-list(VMR,km)
            print(VMR)
            return(newlist)
            
            #return(VMR)
        }}
        ''')
    r_f = robjects.r['f']
    pandas2ri.activate()
    r_DF=pandas2ri.py2ri(df[["x","y"]])

    
    res = r_f(r_DF)
    print("+"*50)
    print(res)
    return res

vmr=r_cal_b(df)