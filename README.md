# GEEKS2_workshop_Pantip_Trend

## install package
```
pipenv install pandas pymysql sqlalchemy jupyterlab
```

## build docker
```
docker build --tag pantip_trend:v1.0 .
```

## run docker
```
docker run --name pantip_trend_test -it -d pantip_trend:v1.0
```

## check log
```
cat cron.log
```

## run pipline
```
python pantip_trend.py
```
