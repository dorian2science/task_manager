import pandas as pd,numpy as np
import sys,os
import warnings
warnings.filterwarnings("ignore")
log_hours = 'log_hours.csv'
app_dir = os.path.dirname(__file__)
FULL_LOG = os.path.join(app_dir,log_hours)

### pour le premier lancement
if not os.path.exists(FULL_LOG):
    pd.DataFrame([],columns=['debut','fin','task']).to_csv(FULL_LOG)

time_format = '%A %d %b %y %Hh%M:%S'
strftime_special=lambda x:x.strftime(time_format)
def get_time():
    time_final=None
    if not time_final is None:
        t=strftime_special(pd.Timestamp(time_final,tz='CET'))
    else:
        t=strftime_special(pd.Timestamp.now(tz='CET'))
    return t

def prepare_data():
    df = pd.read_csv(FULL_LOG,index_col=0)
    t = get_time()
    if len(df)==0:
        task_id = 0
    else:
        task_id = df.index.max()
    return df,t,task_id

def decorator(fun):
    def wrapper(*args,**kwargs):
        df = fun(*args,**kwargs)
        df = df.sort_index(ascending=False)
        df.to_csv(FULL_LOG)
        return df
    return wrapper

@decorator
def complete_job():
    df,t,task_id = prepare_data()
    l = df.iloc[0,:]
    if not l[['fin']].isna().squeeze():
        print("You did not start any job. You can't finish them. Your last action was: ")
        print(l)
        return -1

    df.loc[task_id,'fin'] = strftime_special(pd.to_datetime(t,format=time_format))
    print('task ',df.loc[task_id,'task'],'COMPLETED')
    return df

@decorator
def add_task(task):
    df,t,task_id = prepare_data()
    if not len(df)==0:
        l = df.iloc[0,:]
        if l[['fin']].isna().squeeze():
            print("I assume you have just finish your last job. That's why you start a new one")
            df = complete_job()
    df.loc[task_id+1] = [t,np.nan,task.strip()]
    return df

def format_time_elapsed(s):
    if s is np.nan:
        return np.nan
    m = round(s/60)
    h = m//60
    m = m%60
    return str(h)+'h'+str(m)

def assign_categorie(task):
    for l in ['issue_smartsupervision_','issue_setupmanagement_','meeting_']:
        if re.match('^'+l,task):
            return l[:-1]
    return task

def format_log_hours():
    df = pd.read_csv(FULL_LOG,index_col=0)
    time_format = '%A %d %b %y %Hh%M:%S'
    df['t0'] = pd.to_datetime(df['debut'],format=time_format).dt.tz_localize('CET')
    df['t1'] = pd.to_datetime(df['fin'],format=time_format).dt.tz_localize('CET')
    df.loc[df['t0'].idxmax(),'t1'] = pd.Timestamp.now('CET')
    df['total seconds'] = (df['t1'] - df['t0']).dt.total_seconds()
    hours_minutes = df['total seconds'].dropna().apply(lambda x:format_time_elapsed(x))
    hours_minutes.name='time elapsed'
    DF_LOG_HOURS = df.merge(hours_minutes,left_index=True,right_index=True,how='left')
    DF_LOG_HOURS['categorie'] = DF_LOG_HOURS['task'].apply(lambda x:assign_categorie(x))
    DF_LOG_HOURS['date'] = DF_LOG_HOURS['t0'].dt.date
    DF_LOG_HOURS['week'] = [k.week for k in DF_LOG_HOURS['t0']]
    DF_LOG_HOURS['month'] = [k.month for k in DF_LOG_HOURS['t0']]
    return DF_LOG_HOURS

def get_hours_in_week():
    """hours every day this week"""
    df_week = DF_LOG_HOURS[DF_LOG_HOURS['week']==pd.Timestamp.now(tz='CET').week]
    df_week_woPause = df_week[df_week['categorie']!='pause']
    df_hours_week = df_week_woPause.groupby('date').agg({'total seconds':'sum'}).squeeze().apply(format_time_elapsed).iloc[::-1]
    df_hours_week.index = pd.to_datetime(df_hours_week.index).strftime('%A %d %b %y')
    return df_hours_week

def get_total_hours_weeks():
    # ## total hours spent each week
    return DF_LOG_HOURS[DF_LOG_HOURS['categorie']!='pause'].groupby('week').agg({'total seconds':'sum'}).squeeze().apply(format_time_elapsed).iloc[::-1]

def get_nb_working_days_month(month=None):
# ## nb of working days this month
    df_month = DF_LOG_HOURS[DF_LOG_HOURS['month']==pd.Timestamp.now(tz='CET').month]
    df_month_woPause = df_month[df_month['categorie']!='pause']
    df_days_months = df_month_woPause.groupby('date').agg({'total seconds':'sum'}).squeeze()/3600
    return (df_days_months>4).sum()

def get_hours_per_categorie():
    # ## total hours spent on each categorie this month
    df_month = DF_LOG_HOURS[DF_LOG_HOURS['month']==pd.Timestamp.now(tz='CET').month]
    return df_month.groupby('categorie').agg({'total seconds':'sum'}).squeeze().sort_values().apply(format_time_elapsed).iloc[::-1]

def get_hours_avrg_day():
    # ## Hours worked per day in average
    df_woPause = DF_LOG_HOURS[DF_LOG_HOURS['categorie']!='pause']
    df_woPause = df_woPause.groupby('date').agg({'total seconds':'sum'}).squeeze()
    cur_date = pd.Timestamp.now(tz='CET').date()
    if cur_date in df_woPause.index:
        df_woPause=df_woPause.drop(cur_date)
    df_woPause = df_woPause.agg(['max','min','mean','median']).apply(format_time_elapsed)
    df_woPause['count'] = df_woPause.count()
    return df_woPause.to_dict()

import re
df = pd.read_csv(FULL_LOG,index_col=0)
DF_LOG_HOURS = format_log_hours()
