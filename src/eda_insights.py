import pandas as pd

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


def preparar_datos_web(df_web_1, df_web_2, df_exp_cli, df_final_demo):
    # Concatenar datos web
    df_web = pd.concat([df_web_1, df_web_2], axis=0)
    
    # Convertir date_time a datetime
    df_web['date_time'] = pd.to_datetime(df_web['date_time'], errors='coerce')
    
    # Filtrar clientes con Variation no nulo
    df_exp_cli = df_exp_cli[df_exp_cli["Variation"].notna()]
    
    # Unir web con experimentos
    df_web_v = pd.merge(df_web, df_exp_cli, on='client_id', how='inner')
    
    # Eliminar duplicados
    df_web_v = df_web_v.drop_duplicates()
    
    # Unir con datos demográficos finales
    df = pd.merge(df_final_demo, df_exp_cli, on='client_id', how='inner')
    
    return df_web_v, df


def explorar_datos(df_dict):
    for nombre, df in df_dict.items():
        print(f"--- {nombre} ---")
        print("Shape:", df.shape)
        print(df.head(), "\n")

def limpiar_df_clientes(df):
    df = df.copy()
    
    # Normalizar columnas a minúsculas
    df.columns = df.columns.str.lower()
    
    # Conversión de columnas a Int64 (nullable integer)
    columnas_int = ['clnt_tenure_yr', 'clnt_tenure_mnth', 'num_accts', 'calls_6_mnth', 'logons_6_mnth']
    for col in columnas_int:
        if col in df.columns:
            df[col] = df[col].astype('Int64')
    
    # Rellenar valores nulos en gendr
    if 'gendr' in df.columns:
        df['gendr'] = df['gendr'].fillna('U')
    
    # Rellenar valores nulos en clnt_age con la media
    if 'clnt_age' in df.columns:
        df['clnt_age'] = df['clnt_age'].fillna(df['clnt_age'].mean())
    
    # Eliminar filas con nulos en num_accts
    if 'num_accts' in df.columns:
        df.dropna(subset=['num_accts'], inplace=True)
    
    return df

def filtrar_principales_clientes(df, 
                                 edad_min=30, edad_max=60, 
                                 tenure_min=50, tenure_max=200, 
                                 bal_min=30000, bal_max=110000):
    filtro = (
        (df["clnt_age"] >= edad_min) & (df["clnt_age"] <= edad_max) &
        (df["clnt_tenure_mnth"] >= tenure_min) & (df["clnt_tenure_mnth"] <= tenure_max) &
        (df["bal"] >= bal_min) & (df["bal"] <= bal_max)
    )
    return df[filtro]


def calcular_tasa_finalizacion(df, step_col='process_step', step_objetivo='confirm', cliente_col='client_id', grupo_col='Variation'):
    """
    Calcula la tasa de finalización y cantidades absolutas por grupo.

    Parámetros:
    - df: DataFrame con los datos.
    - step_col: nombre de la columna de pasos (por defecto 'process_step').
    - step_objetivo: paso que se considera como finalización (por defecto 'confirm').
    - cliente_col: columna que identifica al cliente (por defecto 'client_id').
    - grupo_col: columna que representa los grupos de experimento (por defecto 'Variation').

    Devuelve:
    - DataFrame con columnas: [grupo_col, clientes_completados, total_clientes, tasa_%]
    """
    # Clientes que completaron el proceso
    completed = df[df[step_col] == step_objetivo][[cliente_col, grupo_col]].drop_duplicates()
    
    # Total de clientes únicos por grupo
    total_clients = df[[cliente_col, grupo_col]].drop_duplicates().groupby(grupo_col).size().rename('total_clientes')
    
    # Clientes completados por grupo
    completed_clients = completed.groupby(grupo_col).size().rename('clientes_completados')
    
    # Combinar y calcular tasa
    resumen = pd.concat([completed_clients, total_clients], axis=1)
    resumen['tasa_%'] = (resumen['clientes_completados'] / resumen['total_clientes']) * 100
    resumen = resumen.round(2)
    
    return resumen.reset_index()

def calcular_kpis_iqr(df, group_cols, target_col):
    q1 = df.groupby(group_cols)[target_col].quantile(0.25)
    q3 = df.groupby(group_cols)[target_col].quantile(0.75)
    iqr = q3 - q1

    kpis = pd.DataFrame({
        'median': df.groupby(group_cols)[target_col].median(),
        'mode': df.groupby(group_cols)[target_col].agg(lambda x: x.mode().iloc[0]),
        'IQR': iqr
    })

    return kpis.reset_index()

def obtener_primera(df_web_sorted, df_exp_cli):
    # Clientes que completaron confirm
    completed = df_web_sorted[df_web_sorted['process_step'] == 'confirm']['client_id'].unique()
    
    # Filtramos solo registros de esos clientes
    df_completed_clients = df_web_sorted[df_web_sorted['client_id'].isin(completed)]
    
    # Aplicamos filtros de error
    df_valid = df_completed_clients[
        (df_completed_clients['es_error'] == False) &
        (df_completed_clients['repetido_mismo_paso'] == False) &
        (df_completed_clients['retroceso_cero'] == False) &
        (df_completed_clients['salto_grande_atras'] == False)
    ]
    
    # Secuencia ideal de pasos
    ruta_ideal = ['start', 'step_1', 'step_2', 'step_3', 'confirm']
    
    # Agrupamos secuencias de pasos por cliente
    step_sequences = df_valid.groupby('client_id')['process_step'].apply(list)
    
    # Verificamos si la secuencia coincide exactamente con la ideal
    first_attempt_success = [seq == ruta_ideal for seq in step_sequences]
    
    # DataFrame con resultado por cliente
    first_attempt_success_df = pd.DataFrame({
        'client_id': list(step_sequences.index),
        'first_attempt_success': first_attempt_success
    })
    
    # Merge con df_exp_cli para tener info extra
    df_merged = first_attempt_success_df.merge(df_exp_cli, on='client_id', how='inner')
    
    return first_attempt_success_df, df_merged


def calcular_tiempo_total_por_cliente(df, tiempo_col='time_diff_sec', cliente_col='client_id', grupo_col='Variation'):
    """
    Agrupa por cliente y grupo, sumando el tiempo total en segundos.

    Parámetros:
    - df: DataFrame con los datos
    - tiempo_col: nombre de la columna con diferencia de tiempo en segundos
    - cliente_col: nombre de la columna con los IDs de cliente
    - grupo_col: nombre de la columna con la agrupación (por ejemplo, 'Variation')

    Retorna:
    - DataFrame con columnas: cliente, grupo, total_time_sec
    """
    tiempo_total = df.groupby([cliente_col, grupo_col])[tiempo_col].sum().reset_index()
    tiempo_total.rename(columns={tiempo_col: 'total_time_sec'}, inplace=True)
    return tiempo_total