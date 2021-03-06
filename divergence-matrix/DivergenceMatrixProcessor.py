import pandas as pd
from copy import deepcopy


class DivergenceMatrixProcessor:
    def __init__(self, file_name):
        """
        Takes in the name of the file or to be more specific the path to it.
        """
        self.file_name = file_name
        self.array_of_divergence_dfs = pd.read_pickle(self.file_name)

    def retrieve_indexes_with_specified_leak(self, leak_amount):
        """
        Finds indexes of dataframes where the desired leak was simulated.
        # TODO this can be done with mod (%) more efficiently, but only if the order is guaranteed

        :param leak_amount: Float value of the leak that we want to find in Liters per Second.
        :return: Returns an array of int indexes which correspond to the location in array_of_divergence_dfs.
        """
        if type(leak_amount) != float:
            raise Exception("Leak amount must be of type float ! For example 4.0 !")

        leak_search_string = ", {:.1f}LPS".format(leak_amount)

        index_arr = []
        for index, temp_df in enumerate(self.array_of_divergence_dfs):
            if leak_search_string in temp_df.axes[1].name:
                index_arr.append(index)

        return index_arr

    def create_array_of_dfs_with_selected_column(self, indexes_of_dfs, selected_column):
        """
        Creates an array of dataframes from the main array. New array contains only selected indexes and the dataframe
        contains only one column per node with leak.

        :param indexes_of_dfs: An array of indexes of the dataframe that we wish to keep. Preferably created with
        retrieve_indexes_with_specified_leak method.
        :param selected_column: Name of the column of which values we want to keep.
        :return: Returns an array of selected dataframes with only the selected column.
        """
        if len(indexes_of_dfs) < 1:
            raise Exception("Length of indexes array must be at least 1 !")

        if type(selected_column) != str:
            raise Exception("Selected column must a string !")
        new_array_of_dfs = []
        # to ensure that the original list is not modified
        copy_of_original_df = deepcopy(self.array_of_divergence_dfs)

        for index in indexes_of_dfs:
            temp_df = copy_of_original_df[index][[selected_column]]

            # new_column_name = "{}-{}".format(temp_df.axes[1].name, selected_column)   # TODO which is better
            new_column_name = "{}".format(temp_df.axes[1].name)
            temp_df.columns = [new_column_name]

            new_array_of_dfs.append(temp_df)

        return new_array_of_dfs

    def create_df_with_specific_leak_on_one_node(self, leak_amount, selected_node):
        """
        Combines methods retrieve_indexes_with_specified_leak and create_array_of_dfs_with_selected_column to generate
        a dataframe with all the important data.

        :param selected_node: Name of the column of which values we want to keep.
        :param leak_amount: Float value of the leak that we want to find in Liters per Second.
        :returns: One dataframes containing all the nodes with the simulated leak amount but just for one node. In our
        case this will be the sensors on which we want to see the impact.
        Indexes are node names with leak, columns is timestamp in seconds.
        """
        df_indexes_with_leak = self.retrieve_indexes_with_specified_leak(leak_amount)
        array_of_dfs = self.create_array_of_dfs_with_selected_column(df_indexes_with_leak, selected_node)

        concatenated_transposed_df = pd.concat(array_of_dfs, axis=1).transpose()
        return concatenated_transposed_df

    def calculate_column_correlation(self, leak_amount, selected_node):
        """
        Returns two dataframes which are correlation matrices. First takes into account the order of the elements and
        the second just checks the contents of the arrays.


        :param selected_node: Name of the column of which values we want to keep.
        :param leak_amount: Float value of the leak that we want to find in Liters per Second.
        :returns: Returns two dataframes which are correlation matrices. First takes into account the order of the
        elements and the second just checks the contents of the arrays.
        """
        df = self.create_df_with_specific_leak_on_one_node(leak_amount, selected_node)
        column_name = "sorted_array"

        nodes_order_df = pd.DataFrame(columns=[column_name])
        for timestamp in df.columns:
            arr_of_sorted_nodes = list(df[timestamp].sort_values(ascending=False).index)[:round(len(df.index) * 0.1)]
            nodes_order_df.loc[timestamp] = [arr_of_sorted_nodes]

        timestamp_indexes = list(nodes_order_df.index)
        order_correlation_df = pd.DataFrame(columns=timestamp_indexes, index=timestamp_indexes)
        basic_correlation_df = pd.DataFrame(columns=timestamp_indexes, index=timestamp_indexes)

        for timestamp_1 in timestamp_indexes:
            for timestamp_2 in timestamp_indexes:
                array_1 = nodes_order_df.at[timestamp_1, column_name]
                array_2 = nodes_order_df.at[timestamp_2, column_name]

                order_correlation = 0
                basic_correlation = 0
                num_of_elements = 0
                for element_1, element_2 in zip(array_1, array_2):
                    if element_1 == element_2:
                        order_correlation += 1

                    if element_1 in array_2:
                        basic_correlation += 1

                    num_of_elements += 1

                # TODO handle edge cases for values of 0
                order_correlation_res = (order_correlation / num_of_elements)
                basic_correlation_res = (basic_correlation / num_of_elements)

                order_correlation_df.at[timestamp_1, timestamp_2] = order_correlation_res
                basic_correlation_df.at[timestamp_1, timestamp_2] = basic_correlation_res

        return order_correlation_df, basic_correlation_df




