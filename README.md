# 12TH BIG CONTEST
~~~bash
$> tree
.
├── img
└── data
    ├── tmp
    ├── weather
    ├── (AFSNT.csv)
    ├── (AFSNT_DLY.csv)
    └── (SFSNT.csv)
~~~

- Requirement
  * imblearn : over sampling
  * xgboost : boosting module
~~~bash
$> pip install imblearn
$> pip install xgboost
~~~

## Process
1. [Set database](https://github.com/miintto/7th_BIG_CONTEST/wiki/Database)
<br>

2. Insert pandas dataframe into sql table
~~~bash
$> python to_sql.py insert_into afsnt sfsnt afsnt_dly
~~~
<br>

3. Calculating scheduled & actual time between departure and arrival
~~~bash
$> python dataframe.py calculate_STT_time ./data/AFSNT.csv ./data/tmp/AFSNT_addtime.csv
$> python dataframe.py calculate_ATT_time ./data/tmp/AFSNT_addtime.csv ./data/tmp/AFSNT_addtime.csv
~~~
<br>

4. Counting the number of flights in the airports
~~~bash
$> python dataframe.py count_num_flt ./data/tmp/AFSNT_addtime.csv ./data/tmp/AFSNT_dev.csv
~~~
<br>

5. Load weather data
~~~bash
$> python dataframe.py load_weather_data ./data/weather/WEATHER_total.csv
~~~
<br>

6. Merge the AFSNT and weather data
~~~bash
$> python dataframe.py merge_weather_data ./data/weather/WEATHER_total.csv ./data/tmp/afsnt_dev.csv ./data/tmp/AFSNT_WEATHER.csv
~~~
<br>

7. Predict
~~~bash
$> python dataframe.py data_processing ./data/tmp/AFSNT_WEATHER.csv ./data/tmp/
$> python model.py   # deep learning model
$> python model2.py   # SVM model
$> python model3.py   # decision tree model
$> python model4.py   # random forest model
$> python model5.py   # ada boosting model
~~~
