# data processing
import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import re

# data visualization
import plotly.graph_objs as go
from plotly.graph_objs import Bar, Layout
from plotly import offline
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

# change text color
import colorama
from colorama import Fore, Style

def GET_csse_covid_19_time_series():
    print('reading [time series] data ......')
    time_series_covid19_confirmed_US = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
    time_series_covid19_confirmed_global = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    time_series_covid19_deaths_US = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
    time_series_covid19_deaths_global = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    time_series_covid19_recovered_global = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    print('finish reading')
    return time_series_covid19_confirmed_US, time_series_covid19_confirmed_global, time_series_covid19_deaths_US, time_series_covid19_deaths_global, time_series_covid19_recovered_global

# user pass in variable 'region'
# if region = 'global', gather global daily reports
# if region = 'us', gather united states daily reports
def GET_csse_covid_19_daily_reports(region):
    '''
   get the latest and previous date cases
    :return:
    '''
    print('reading [cross sectional] data ......')
    if region == 'global':
        region = ''
    elif region == 'us':
        region = '_us'
    # current date
    date = datetime.now()
    latest_data = None
    prev_data = None
    while latest_data is None or prev_data is None:
        if latest_data is None:
            try:
                url1 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports{}/{}.csv'.format(region, date.strftime('%m-%d-%Y'))
                latest_data = pd.read_csv(url1)
            except:
                date = date-timedelta(1)
        else:
            try:
                url2 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports{}/{}.csv'.format(region, date.strftime('%m-%d-%Y'))
                prev_data = pd.read_csv(url2)
            except:
                date = date-timedelta(1)
    print('finish reading')
    return latest_data, prev_data


def GET_shanghai_data():
    '''Gather Shanghai COVID Data (recent 10 days)'''
    print('reading [shanghai] data ......')
    data_name = 'ts_shanghai_covid'
    url = f'https://gitee.com/gzjzg/whale-pkg/raw/master/DATA/{data_name}.csv'
    data1 = pd.read_csv(url,encoding = 'gbk')['detail']

    data2 = data1[data1.apply(lambda x: x.startswith('上海202'))].sort_values()
    data2 = data2.apply(lambda x: re.sub(r'\（.*?\）', '', x))
    data2 = data2.apply(lambda x: x.replace('无新增','0'))

    df_all = pd.DataFrame(map(np.ravel,data2.apply(lambda x: re.findall(r"\d+",x)))).rename({
        0:'year',
        1:'month',
        2:'day',
        3:'local_daily_positive_cases',
        4:'local_asymptomatic_cases'
    },axis=1).iloc[:,:5]
    df_all['date'] = df_all['year'].map(str)+"/"+df_all['month'].map(str)+"/"+df_all['day'].map(str)
    df_all['date'] = pd.to_datetime(df_all['date'])

    df_all = df_all.set_index('date').sort_index()
    df_all = df_all.astype('int32')
    df = df_all.iloc[:,3:5]
    print('finish reading')
    return df

