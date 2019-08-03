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

3. add AFSNT data into the NUM_FLT column
~~~bash
$> python dataframe.py count_num_flt ./data/AFSNT_2.csv
~~~
