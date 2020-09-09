import re
import json
import datetime
import xlwings as xw
import pandas as pd
import frontur_utilities as df
import frontur_excel_addin.utility_functions as uf
from frontur_utilities.solver_df import df_solver


@xw.func
@xw.ret(index=False, expand='table')
def sample():
    """Elimina todos los espacios de la columna seleccionada"""
    data_frame = df.df_fileloader.load_agenda(df.const.FRONTUR_FILE_PATH)

    data_frame = df.extract_methods.add_plane_data(data_frame, df.const.PLANES_DATA_FILE_PATH)
    data_frame = df.extract_methods.format_dates(data_frame)
    data_frame = df.extract_methods.select_days(data_frame, df.const.DAYS_FILE_PATH)

    return uf.encode_dataframe(data_frame.iloc[:1])


@xw.func
@xw.arg('data_frame', pd.DataFrame, header=True, index=False, dates=datetime.datetime)
@xw.ret(index=False, expand='table')
def format_wk_days(data_frame):
    """Elimina todos los espacios de la columna seleccionada"""
    data_frame = uf.decode_dataframe(data_frame)

    data_frame = df.extract_methods.format_dates(data_frame)
    # df.extract_methods.substitute_values(data_frame, df.const.SUBSTITUTIONS_FILE_PATH)
    data_frame = df.extract_methods.select_days(data_frame, df.const.DAYS_FILE_PATH)
    data_frame[df.const.DF_PLANE_COL_NAME] = data_frame[df.const.DF_PLANE_COL_NAME].apply(lambda x: re.sub(r"\.\d+", '', str(x)))
    data_frame = df.extract_methods.add_plane_data(data_frame, df.const.PLANES_DATA_FILE_PATH)

    return uf.encode_dataframe(data_frame.sort_values(by=[df.const.DF_DAY_COL_NAME]))


@xw.func
@xw.arg('data_frame', pd.DataFrame, header=True, index=False, dates=datetime.datetime)
@xw.ret(index=False, expand='table')
def expand_date_intervals(data_frame):
    """Elimina todos los espacios de la columna seleccionada"""
    data_frame = uf.decode_dataframe(data_frame)
    
    data_frame = df.extract_methods.format_dates(data_frame)

    return uf.encode_dataframe(data_frame.sort_values(by=[df.const.DF_DAY_COL_NAME]))


@xw.func
@xw.arg('data_frame', pd.DataFrame, header=True, index=False, dates=datetime.datetime)
@xw.arg('dates', ndim=2, doc='argumento')
@xw.arg('airport', ndim=1, doc='argumento')
@xw.ret(index=False, expand='table')
def get_flights(data_frame, dates, airport, date_format=df.const.DF_DATAFRAME_DAY_FORMAT):
    """Elimina todos los espacios de la columna seleccionada"""
    data_frame = uf.decode_dataframe(data_frame)

    data_frame = df.extract_methods.select_airport(data_frame, airport[0])
    data_frame = df.extract_methods.format_dates(data_frame, df.const.DF_WEEKDAY_COL_NAME)

    dates = df.utility.flatten(dates)
    dates = [ str(x.strftime(date_format)) for x in dates]
    data_frame = df.df_utility.select_rows(data_frame, dict([
            ('day_column_name', df.const.DF_DAY_COL_NAME),
            ('format', date_format),
            ('days', dates)
        ]),
        # days=dates
        )

    data_frame[df.const.DF_PLANE_COL_NAME] = data_frame[df.const.DF_PLANE_COL_NAME].apply(lambda x: re.sub(r"\.\d+", '', str(x)))
    data_frame = df.extract_methods.add_plane_data(data_frame, df.const.PLANES_DATA_FILE_PATH)

    return uf.encode_dataframe(data_frame)


@xw.func
@xw.arg('data_frame', pd.DataFrame, header=True, index=False, dates=datetime.datetime)
@xw.arg('target_column', ndim=1, doc='argumento')
@xw.arg('date_format', ndim=1, doc='argumento')
@xw.arg('dates', ndim=2, doc='argumento')
@xw.ret(index=False, expand='table')
def pick_selected_dates(data_frame, target_column, dates, date_format):
    data_frame = uf.decode_dataframe(data_frame)
    dates = df.utility.flatten(dates)
    dates = [ str(x.strftime(date_format[0])) for x in dates]
    data_frame = df.df_utility.select_rows(data_frame, dict([
            ('day_column_name', target_column[0]),
            ('format', date_format[0]),
            ('days', dates)
        ]),
        days=dates
        )
    return data_frame


@xw.func
@xw.arg('first_data_frame', pd.DataFrame, header=True, index=False, dates=datetime.datetime)
@xw.arg('second_data_frame', pd.DataFrame, header=True, index=False, dates=datetime.datetime)
@xw.arg('target_column', ndim=1)
@xw.ret(index=False, expand='table')
def inner_merge(first_data_frame, second_data_frame, target_column):
    first_data_frame = uf.decode_dataframe(first_data_frame)
    second_data_frame = uf.decode_dataframe(second_data_frame)
    data_frame = pd.merge(first_data_frame, second_data_frame, how='inner', on=target_column)
    return uf.encode_dataframe(data_frame)


@xw.func
@xw.arg('data_frame', pd.DataFrame, index=False)
@xw.arg('reference_column', ndim=1, doc='argumento')
@xw.arg('target_column', ndim=1, doc='argumento')
@xw.arg('values', ndim=2, doc='argumento')
@xw.arg('replace_value', ndim=1, doc='argumento')
@xw.ret(index=False, expand='table')
def substitute_rows(data_frame, reference_column, target_column, values, replace_value):
    data_frame = uf.decode_dataframe(data_frame) 
    values = df.utility.flatten(values)

    df.df_utility.substitute_rows(data_frame, dict([
        ('column_name', target_column[0]),
        ('reference_column_name', reference_column[0]),
        ('reference_column_values', values),
        ('replace_value', replace_value[0])
    ]))
    return uf.encode_dataframe(data_frame)


@xw.func
@xw.arg('cell_matrix', ndim=2, doc='argumento')
@xw.ret(index=False)
def assemble_cells(*cell_matrix):
    """Elimina todos los espacios de la columna seleccionada"""
    cell_matrix = df.utility.flatten(cell_matrix)
    data_frame = pd.DataFrame(cell_matrix[1:], columns=cell_matrix[0])
    return data_frame


@xw.func(async_mode='threading')
@xw.arg('data_frame', pd.DataFrame, header=True, index=False, dates=datetime.datetime)
@xw.ret(index=False, expand='table')
def solver(data_frame):
    data_frame = uf.decode_dataframe(data_frame) 
    with open(const.REQ_INTERVIEWS_FILE_PATH) as jfile:
        data = json.load(jfile)
    data_frame = df_solver(data_frame, no_groups=True, parameters={
        'workday_time': pd.Timedelta(hours=8).seconds,
        'rest_time': pd.Timedelta(minutes=10).seconds,
        'execution_time_limit': pd.Timedelta(minutes=15).seconds,
        'country_kwargs': {
            'plane_kwargs': {
                'seats_used': 0.8,
                'poll_success': 0.6,
                'poll_time': pd.Timedelta(seconds=30).seconds
            },
            'interviews': data
        }
    })
    return uf.encode_dataframe(data_frame)