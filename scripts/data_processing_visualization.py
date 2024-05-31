
import pandas as pd, matplotlib.pyplot as plt
import os, sys; sys.path.insert(0, os.path.join(sys.path[0], '..'))
from re import sub

def camel_case(s): 
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])

def aggregate(file_path_or_df, independent_columns, dependent_columns, save_file = False): 
    if isinstance(file_path_or_df, str):
        try:
            df = pd.read_csv(file_path_or_df)
            assets_read_folder = "."
        except:
            df = pd.read_csv(os.path.join("..", file_path_or_df))
            assets_read_folder = ".."
    else:
        df = file_path_or_df
        assets_read_folder = "."
    
    independent_columns_agg = [col for col, options in independent_columns.items() if ("aggregate" in options and options["aggregate"])]
    independent_columns_not_agg = [col for col in independent_columns if not col in independent_columns_agg]
    all_columns = list(independent_columns.keys()) + list(dependent_columns.keys())
    df = df[all_columns]

    for col, options in independent_columns.items():
        if "values" in options:
            df = df[df[col].isin(options["values"])]

    result_df = df.groupby(independent_columns_not_agg).agg({col: 'mean' for col in dependent_columns.keys()}).reset_index()

    independent_columns_not_agg_str = '_'.join(sorted([camel_case(col) for col in independent_columns_not_agg]))
    dependent_columns_str = '_'.join(sorted([camel_case(col) for col in dependent_columns]))

    if (save_file and isinstance(file_path_or_df, str)):
        output_file = os.path.join(assets_read_folder, f'{file_path_or_df[:-4]}-id={independent_columns_not_agg_str}-d={dependent_columns_str}.csv')
        result_df.to_csv(output_file, index=False)
        print(f'Result saved to {output_file}')
    return (result_df)

def time_series(file_path_or_df, independent_columns, dependent_columns, 
                date_column_name = "Value Date", save_file = False): 
    if isinstance(file_path_or_df, str):
        try:
            df = pd.read_csv(file_path_or_df)
            assets_read_folder = "."
        except:
            df = pd.read_csv(os.path.join("..", file_path_or_df))
            assets_read_folder = ".."
    else:
        df = file_path_or_df
        assets_read_folder = "."
    assert (date_column_name in df.columns), f"The input dataframe must have the '{date_column_name}' column. "

    all_columns = list(independent_columns.keys()) + list(dependent_columns.keys())
    if (date_column_name not in all_columns): 
        date_column_name.append(date_column_name)
    df = df[all_columns]
    
    for col, values in independent_columns.items():
        if (col != date_column_name and "values" in values): 
            df = df[df[col].isin(values["values"])]
        elif (col == date_column_name): 
            assert(len(values) == 2), "'Value Date' option list must have 2 values: start date and end date (Fill in None if N/A). "
            start_date, end_date = values
            df = time_ranged(file_path_or_df, start_date, end_date)

    result_df = df.groupby(date_column_name).agg({col: 'mean' for col in dependent_columns.keys()}).reset_index()
    if (save_file and isinstance(file_path_or_df, str)):
        output_file = os.path.join(assets_read_folder, f"{file_path_or_df[:-4]}-timeseries{'-' if start_date or end_date else ''}{'sd=' + start_date.replace('-', '') if start_date else ''}{'-' if start_date and end_date else ''}{'ed=' + end_date.replace('-', '') if end_date else ''}.csv")
        result_df.to_csv(output_file, index=False)
        print(f'Result saved to {output_file}')
    return (result_df)

def time_ranged(file_path_or_df, start_date = None, end_date = None, 
                date_column_name = "Value Date", save_file = False): 
    if isinstance(file_path_or_df, str):
        try:
            df = pd.read_csv(file_path_or_df)
            assets_read_folder = "."
        except:
            df = pd.read_csv(os.path.join("..", file_path_or_df))
            assets_read_folder = ".."
    else:
        df = file_path_or_df
        assets_read_folder = "."
    assert (date_column_name in df.columns), f"The input dataframe must have the '{date_column_name}' column. "
    if start_date is not None:
        df[date_column_name] = pd.to_datetime(df[date_column_name], format="%Y-%m-%d")
        df = df[df[date_column_name] >= pd.to_datetime(start_date, format="%Y-%m-%d")]
    if end_date is not None:
        df[date_column_name] = pd.to_datetime(df[date_column_name], format="%Y-%m-%d")
        df = df[df[date_column_name] <= pd.to_datetime(end_date, format="%Y-%m-%d")]

    if (save_file and isinstance(file_path_or_df, str)):
        output_file = os.path.join(assets_read_folder, f"{file_path_or_df[:-4]}-timeranged{'-' if start_date or end_date else ''}{'sd=' + start_date.replace('-', '') if start_date else ''}{'-' if start_date and end_date else ''}{'ed=' + end_date.replace('-', '') if end_date else ''}.csv")
        df.to_csv(output_file, index=False)
        print(f'Result saved to {output_file}')
    return (df)
