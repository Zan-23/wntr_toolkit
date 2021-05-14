from DivergenceMatrixProcessor import DivergenceMatrixProcessor

instance = DivergenceMatrixProcessor("./../data/delft_data/Divergence_M.pickle")
df_main = instance.create_df_with_specific_leak_on_one_node(4.1, "SenzorComunarzi-NatVech")
