import pandas as pd
from sklearn import preprocessing


def compare_real_with_simulated_data(real_data_file_names, source_dir=None):
    if len(real_data_file_names) < 1:
        raise Exception("At least one file name must be given in array form !")
    files = real_data_file_names.copy()

    if source_dir is not None:
        temp_file_names = []
        for file_name in real_data_file_names:
            full_path = "{}{}".format(source_dir, file_name)
            temp_file_names.append(full_path)

        real_data_file_names = temp_file_names

    dict_of_dfs = dict()
    for file_name, file_key in zip(real_data_file_names, files):
        dict_of_dfs[file_key] = csv_file_to_pandas_df(file_name)

    return dict_of_dfs
    # take in data frame or file name
    # prepare it in a standard form
    # calculate absolute differences


def csv_file_to_pandas_df(file_name):
    """

    """
    original_df = pd.read_csv(file_name, sep="\t+", engine='python')
    original_df["hour"] = pd.to_datetime(original_df["DateTime"])

    hour = pd.to_timedelta(original_df["hour"].dt.hour, unit='H')
    return original_df.groupby(hour).mean()


def generate_leakage_correlation_matrix(dict_of_leaks, leak_attribute_name, selected_nodes=None, normalize=False):
    # only works with diff dict because of the 24h reference
    if selected_nodes is None:
        # TODO set to all columns
        pass

    correlation_df = pd.DataFrame(columns=selected_nodes)

    for node_with_leak in dict_of_leaks:
        temp_dict = dict()
        for key in dict_of_leaks[node_with_leak][leak_attribute_name]:
            temp_diff_sum = 0
            for hour in dict_of_leaks[node_with_leak][leak_attribute_name][key]:
                # combing together 24 ur differences
                temp_diff_sum += abs(dict_of_leaks[node_with_leak][leak_attribute_name][key][hour])
            temp_dict[key] = temp_diff_sum

        correlation_df.loc[node_with_leak] = temp_dict

    if normalize:
        temp_df = correlation_df.values  # returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(temp_df)
        # TODO check if order of index is guaranteed
        correlation_df = pd.DataFrame(x_scaled, columns=correlation_df.columns, index=correlation_df.index)

    return correlation_df











