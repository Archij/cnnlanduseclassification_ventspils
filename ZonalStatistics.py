import sys, os, shutil, csv
from qgis.analysis import QgsZonalStatistics
from qgis.core import QgsVectorLayer
from qgis.core import QgsRasterLayer
from osgeo import ogr

def getAttribute(x):
    attribute = []
    if x == 'Meldrajs_udeni_poligons':
      attribute = 1
    elif x == 'poligons_Augludarzs':
      attribute = 2
    elif x == 'poligons_Grislajs':
      attribute = 3
    elif x == 'poligons_Izcirtums':
      attribute = 4
    elif x == 'poligons_Izdegums':
      attribute = 5
    elif x == 'poligons_Jaunaudze':
      attribute = 6
    elif x == 'poligons_Kapi':
      attribute = 7
    elif x == 'poligons_Krumajs':
      attribute = 8
    elif x == 'poligons_Krumaugu_plant':
      attribute = 9
    elif x == 'poligons_Kudra':
      attribute = 10
    elif x == 'poligons_Meldrajs':
      attribute = 11
    elif x == 'poligons_Meza_kapi':
      attribute = 12
    elif x == 'poligons_Mezs':
      attribute = 13
    elif x == 'poligons_Ogulajs':
      attribute = 14
    elif x == 'poligons_Parejas_zemes':
      attribute = 15
    elif x == 'poligons_Parks':
      attribute = 16
    elif x == 'poligons_Plava':
      attribute = 17
    elif x == 'poligons_Saknudarzs':
      attribute = 18
    elif x == 'poligons_Skrajmezs':
      attribute = 19
    elif x == 'poligons_Smiltajs':
      attribute = 20
    elif x == 'poligons_Sunajs':
      attribute = 21
    elif x == 'poligons_Zaliens':
      attribute = 22
    elif x == 'Seklis_poligons':
      attribute = 23
      
    return attribute
    

#specify polygon shapefile vector
polygonLayer = QgsVectorLayer('C:/Users/Professional/Downloads/SHP/landus_A.shp', 'zonepolygons', "ogr") 


subfolders = [ f.name for f in os.scandir('D:/RGB/') if f.is_dir() ]
for subfolder in subfolders:
    filelist = [file for file in os.listdir('D:/RGB/' + subfolder) if file.endswith('.tif')]
    for file in filelist:

        
        rasterFilePath = 'D:/RGB/' + subfolder + '/' + file

        # raster filename
        rasterFile = QgsRasterLayer(rasterFilePath, 'raster')

        zoneStat = QgsZonalStatistics (polygonLayer, rasterFile, '', 1, QgsZonalStatistics.Count)
        zoneStat.calculateStatistics(None)

        shapefile = "C:/Users/Professional/Downloads/SHP/landus_A.shp"
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataSource = driver.Open(shapefile, 0)
        layer = dataSource.GetLayer()

        layer.SetAttributeFilter("count = 50176")
        if layer.GetFeatureCount()==1:
            for feature in layer:
                x = feature.GetField("FNAME")
                shutil.copy(rasterFilePath, 'D:/LandUse/' + x)
                # read header automatically
                with open('D:/LandUse/train.csv', "r", encoding="utf-8") as train_file:
                    reader = csv.reader(train_file)
                    for header in reader:
                        break
                with open('D:/LandUse/train.csv', 'a+', newline='', encoding="utf-8") as train_file:
                    train_writer = csv.writer(train_file)
                    train_writer.writerow(['./' + x + '/' + file, getAttribute(x)])
       
        polygonLayer.dataProvider().deleteAttributes([7])
        polygonLayer.updateFields()

