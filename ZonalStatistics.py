"""
@author: Arthur Stepchenko
"""
import sys, os, shutil, csv
from qgis.analysis import QgsZonalStatistics
from qgis.core import QgsVectorLayer
from qgis.core import QgsRasterLayer
from osgeo import ogr

def getAttribute(x):
    attribute = []
    if x == 'Meldrājs_ūdenī_poligons':
      attribute = 1
    elif x == 'poligons_Augļudārzs':
      attribute = 2
    elif x == 'poligons_Grīslājs':
      attribute = 3
    elif x == 'poligons_Izcirtums':
      attribute = 4
    elif x == 'poligons_Izdegums':
      attribute = 5
    elif x == 'poligons_Jaunaudze':
      attribute = 6
    elif x == 'poligons_Kapi':
      attribute = 7
    elif x == 'poligons_Krūmājs':
      attribute = 8
    elif x == 'poligons_Krūmaugu_plant':
      attribute = 9
    elif x == 'poligons_Kūdra':
      attribute = 10
    elif x == 'poligons_Meldrājs':
      attribute = 11
    elif x == 'poligons_Meza_kapi':
      attribute = 12
    elif x == 'poligons_Mezs':
      attribute = 13
    elif x == 'poligons_Ogulājs':
      attribute = 14
    elif x == 'poligons_Pārējās_zemes':
      attribute = 15
    elif x == 'poligons_Parks':
      attribute = 16
    elif x == 'poligons_Pļava':
      attribute = 17
    elif x == 'poligons_Sakņudārzs':
      attribute = 18
    elif x == 'poligons_Skrajmezs':
      attribute = 19
    elif x == 'poligons_Smiltājs':
      attribute = 20
    elif x == 'poligons_Sūnājs':
      attribute = 21
    elif x == 'poligons_Zāliens':
      attribute = 22
    elif x == 'Sēklis_poligons':
      attribute = 23
      
    return attribute
    

#specify polygon shapefile vector
polygonLayer = QgsVectorLayer('/home/arturs/Downloads/SHP/landus_A.shp', 'zonepolygons', "ogr") 


subfolders = [ f.name for f in os.scandir('/home/arturs/Data/RGB_Tiles/') if f.is_dir() ]
for subfolder in subfolders:
    filelist = [file for file in os.listdir('/home/arturs/Data/RGB_Tiles/' + subfolder) if file.endswith('.tif')]
    for file in filelist:

        # specify raster filename
        rasterFilePath = '/home/arturs/Data/RGB_Tiles/' + subfolder + '/' + file


        rasterFile = QgsRasterLayer(rasterFilePath, 'raster')

        # usage - QgsZonalStatistics (QgsVectorLayer *polygonLayer, const QString &rasterFile, const QString &attributePrefix="", int rasterBand=1)
        zoneStat = QgsZonalStatistics (polygonLayer, rasterFile, '', 1, QgsZonalStatistics.Count)
        zoneStat.calculateStatistics(None)

        shapefile = "/home/arturs/Downloads/SHP/landus_A.shp"
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataSource = driver.Open(shapefile, 0)
        layer = dataSource.GetLayer()

        layer.SetAttributeFilter("count = 50176")
        if layer.GetFeatureCount()==1:
            for feature in layer:
                x = feature.GetField("FNAME")
                shutil.copy(rasterFilePath, '/home/arturs/Data/LandUse/' + x)
                # read header automatically
                with open('/home/arturs/Data/LandUse/train.csv', "r", encoding="utf-8") as train_file:
                    reader = csv.reader(train_file)
                    for header in reader:
                        break
                with open('/home/arturs/Data/LandUse/train.csv', 'a+', newline='', encoding="utf-8") as train_file:
                    train_writer = csv.writer(train_file)
                    train_writer.writerow(['./' + x + '/' + file, getAttribute(x)])
       
        polygonLayer.dataProvider().deleteAttributes([7])
        polygonLayer.updateFields()

