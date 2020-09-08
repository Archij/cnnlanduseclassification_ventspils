# cnnlanduseclassification_ventspils

Результаты в статье: https://www.researchgate.net/publication/344043328_Land-Use_Classification_using_Convolutional_Neural_Networks.

Список файлов:

Tiles.py - для разделения аэроортофото изображений на мелкие фрагменты;

ZonalStatistics.py - чтобы связать каждый фрагмент аэроортофото изображений с соответствующим классом землепользования;

test.py - проверка обученной модели. Входные данные: train.csv с путями к изображениям и значениями классов; Keras модель model.h5 и mapping.pkl;

test_results.zip - результаты обученной модели на тестовой выборке данных.
