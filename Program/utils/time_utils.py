from datetime import datetime, timedelta
import pandas as pd
from utils.math_utils import cal_mean
from typing import List

def time_reverse(time_str):
    try:
        time_temp = time_str.replace('T', ' ')
        time_temp = time_temp.replace('Z', '')
        return datetime.strptime(str(time_temp), '%Y-%m-%d %H:%M:%S')
    except:
        return None


def cal_time_delta_hours(start: datetime, end: datetime):
    if pd.isna(start) or pd.isna(end):
        return None
    delta_seconds = (end - start).total_seconds()
    delta_hours = delta_seconds / 3600
    return delta_hours


def cal_time_delta_minutes(start: datetime, end: datetime):
    if pd.isna(start) or pd.isna(end):
        return None
    delta_seconds = (end - start).total_seconds()
    delta_minutes = delta_seconds / 60
    return delta_minutes


def cal_time_interval(date_list: List):
    date_list.sort()
    interval = []
    for i in range(1, len(date_list)):
        inv = cal_time_delta_minutes(date_list[i - 1], date_list[i])
        interval.append(inv)
    return cal_mean(interval)
