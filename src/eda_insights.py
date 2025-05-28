import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os



def filter_outliers_iqr(df, column, lower=True, upper=True, multiplier=1.5):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR

    if lower and upper:
        filtered_df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    elif lower:
        filtered_df = df[df[column] >= lower_bound]
    elif upper:
        filtered_df = df[df[column] <= upper_bound]
    else:
        filtered_df = df.copy()

    return filtered_df

def calcular_tasa(df, evento_col, grupo_col=None, step_col=None):
    if grupo_col and step_col:
        total = df.groupby([grupo_col, step_col]).size().reset_index(name='total_registros')
        eventos = df[df[evento_col]].groupby([grupo_col, step_col]).size().reset_index(name='n_eventos')
        merged = pd.merge(total, eventos, on=[grupo_col, step_col], how='left').fillna(0)
        merged['tasa_%'] = (merged['n_eventos'] / merged['total_registros']) * 100
        return merged.sort_values([grupo_col, step_col])
    elif grupo_col:
        return df.groupby(grupo_col)[evento_col].mean() * 100
    else:
        return df[evento_col].mean() * 100
    

def detectar_errores_funnel(df, step_col='process_step', client_col='client_id', visit_col='visit_id', time_diff_col='time_diff_sec'):
    step_order = {'start': 0, 'step_1': 1, 'step_2': 2, 'step_3': 3, 'confirm': 4}
    df = df.copy()
    
    df['step_num'] = df[step_col].map(step_order)
    df['prev_step_num'] = df.groupby([client_col, visit_col])['step_num'].shift(1)
    df['prev_step'] = df.groupby([client_col, visit_col])[step_col].shift(1)
    
    df['repetido_mismo_paso'] = (
        (df[step_col] == df['prev_step']) &
        (df[time_diff_col] == 0)
    )
    
    df['retroceso_cero'] = (
        (df[time_diff_col] == 0) &
        (df['prev_step_num'] < df['step_num'])
    )
    
    df['salto_grande_atras'] = (
        (df[time_diff_col] == 0) &
        ((df['prev_step_num'] - df['step_num']) >= 2)
    )
    
    df['salto_grande_adelante'] = (
        (df[time_diff_col] == 0) &
        (df['prev_step_num'].notna()) &
        ((df['step_num'] - df['prev_step_num']) >= 2)
    )
    
    df['es_error'] = df[[
        'repetido_mismo_paso',
        'retroceso_cero',
        'salto_grande_atras',
        'salto_grande_adelante'
    ]].any(axis=1)
    
    return df

def calcular_diferencia_tiempo(df, client_col='client_id', visit_col='visit_id', time_col='date_time'):
    df = df.sort_values(by=[client_col, visit_col, time_col]).reset_index(drop=True)
    df['time_diff'] = df.groupby([client_col, visit_col])[time_col].shift(-1) - df[time_col]
    df['time_diff_sec'] = df['time_diff'].dt.total_seconds()
    return df