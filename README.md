# 12TH BIG CONTEST
~~~bash
$> tree
.
└── data
    ├── AFSNT.csv
    ├── AFSNT_DLY.csv
    └── SFSNT.csv
~~~

1. [Set database](https://github.com/miintto/7th_BIG_CONTEST/wiki/Database)

2. Insert pandas dataframe into sql table
~~~bash
$> python to_sql.py insert_into afsnt sfsnt afsnt_dly
~~~
3. Calculating time between departure and arrival
~~~bash
$> python dataframe.py calculate_time ./data/AFSNT.csv ./data/AFSNT_addtime.csv
~~~
4. Counting the number of flights in the airports
~~~bash
$> python dataframe.py count_num_flt ./data/AFSNT_addtime.csv ./data/AFSNT_dev.csv
~~~
