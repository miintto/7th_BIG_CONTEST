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

1. [Set database](https://github.com/miintto/7th_BIG_CONTEST/wiki/Database)

2. Insert pandas dataframe into sql table
~~~bash
$> python to_sql.py insert_into afsnt sfsnt afsnt_dly
~~~

3. Calculating scheduled & actual time between departure and arrival
~~~bash
$> python dataframe.py calculate_STT_time ./data/AFSNT.csv ./data/tmp/AFSNT_addtime.csv
$> python dataframe.py calculate_ATT_time ./data/tmp/AFSNT_addtime.csv ./data/tmp/AFSNT_addtime.csv
~~~

4. Counting the number of flights in the airports
~~~bash
$> python dataframe.py count_num_flt ./data/tmp/AFSNT_addtime.csv ./data/tmp/AFSNT_dev.csv
~~~

5. Load weather data
~~~bash
$> python dataframe.py load_weather_data ./data/weather/WEATHER_total.csv
~~~

6. Predict
~~~bash
$> python dataframe.py data_processing ./data/tmp/AFSNT_dev.csv ./data/tmp/
$> python model.py
~~~
