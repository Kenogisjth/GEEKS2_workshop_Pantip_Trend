# GEEKS2_workshop_Pantip_Trend

## install python and pip
https://www.python.org/downloads/

## install pipenv
```
pip install pipenv
```

## create shell
```
pipenv shell --python ~~python path~~
```

## install package
```
pipenv install pandas pymysql sqlalchemy selenium jupyterlab
```

## run jupyter lab
```
jupyter lab
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

## run pipeline
```
python pantip_trend.py
```
