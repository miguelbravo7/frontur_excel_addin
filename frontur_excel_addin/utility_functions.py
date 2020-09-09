import datetime
import pandas as pd
import frontur_utilities.constants as const


def decode_dataframe(data_frame):
    if not data_frame.empty:
        if const.DF_OPERATION_START_COL_NAME in data_frame:
            data_frame[const.DF_OPERATION_START_COL_NAME] = data_frame.apply(lambda row:
                decode_date(row[const.DF_OPERATION_START_COL_NAME]), axis='columns')
        if const.DF_OPERATION_END_COL_NAME in data_frame:
            data_frame[const.DF_OPERATION_END_COL_NAME] = data_frame.apply(lambda row:
                decode_date(row[const.DF_OPERATION_END_COL_NAME]), axis='columns')
        if const.DF_EMBARK_HOUR in data_frame:
            data_frame[const.DF_EMBARK_HOUR] = data_frame.apply(lambda row:
                decode_time(row[const.DF_EMBARK_HOUR]), axis='columns')
        if const.DF_DAY_COL_NAME in data_frame:
                data_frame[const.DF_DAY_COL_NAME] = data_frame.apply(lambda row:
                    decode_date(row[const.DF_DAY_COL_NAME]), axis='columns')

    return data_frame


def encode_dataframe(data_frame):
    if not data_frame.empty:
        if const.DF_OPERATION_START_COL_NAME in data_frame:
            data_frame[const.DF_OPERATION_START_COL_NAME] = data_frame.apply(lambda row: 
                # str(row['Opera_desde'].strftime('%d/%m/%Y')), 
                row[const.DF_OPERATION_START_COL_NAME].isoformat().split('T')[0],
                axis='columns')
        if const.DF_OPERATION_END_COL_NAME in data_frame:
            data_frame[const.DF_OPERATION_END_COL_NAME] = data_frame.apply(lambda row:
                row[const.DF_OPERATION_END_COL_NAME].strftime('%d/%m/%Y'), axis='columns')   
        if const.DF_EMBARK_HOUR in data_frame:
            data_frame[const.DF_EMBARK_HOUR] = data_frame.apply(lambda row: 
                str(row[const.DF_EMBARK_HOUR]).split(' ')[-1], axis='columns')
        if const.DF_DAY_COL_NAME in data_frame:
            data_frame[const.DF_DAY_COL_NAME] = data_frame.apply(lambda row: 
                row[const.DF_DAY_COL_NAME].strftime('%d/%m/%Y'), axis='columns')

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