import datetime
import pandas as pd


def decode_dataframe(data_frame):
    if not data_frame.empty:
        if 'Opera_desde' in data_frame:
            data_frame['Opera_desde'] = data_frame.apply(lambda row:
                decode_date(row['Opera_desde']), axis='columns')
        if 'Opera_hasta' in data_frame:
            data_frame['Opera_hasta'] = data_frame.apply(lambda row:
                decode_date(row['Opera_hasta']), axis='columns')
        if 'Hora_Salida' in data_frame:
            data_frame['Hora_Salida'] = data_frame.apply(lambda row:
                decode_time(row['Hora_Salida']), axis='columns')
        if 'Day' in data_frame:
                data_frame['Day'] = data_frame.apply(lambda row:
                    decode_date(row['Day']), axis='columns')

    return data_frame


def encode_dataframe(data_frame):
    if not data_frame.empty:
        if 'Opera_desde' in data_frame:
            data_frame['Opera_desde'] = data_frame.apply(lambda row: 
                # str(row['Opera_desde'].strftime('%d/%m/%Y')), 
                row['Opera_desde'].isoformat(),
                axis='columns')
        if 'Opera_hasta' in data_frame:
            data_frame['Opera_hasta'] = data_frame.apply(lambda row:
                row['Opera_hasta'].strftime('%d/%m/%Y'), axis='columns')   
        if 'Hora_Salida' in data_frame:
            data_frame['Hora_Salida'] = data_frame.apply(lambda row: 
                str(row['Hora_Salida']).split(' ')[-1], axis='columns')
        if 'Day' in data_frame:
            data_frame['Day'] = data_frame.apply(lambda row: 
                row['Day'].strftime('%d/%m/%Y'), axis='columns')

    return data_frame


def decode_date(value):
    if isinstance(value, (float, int)):
        return datetime.date(1900,1,1) + datetime.timedelta(days=int(value)) - datetime.timedelta(days=2)
    elif isinstance(value, str):
        from dateutil import parser
        return parser.parse(value)
    else:
        return value


def decode_time(value):
    if isinstance(value, (float, int)):
        return datetime.timedelta(days=float(value))
    else:
        return value