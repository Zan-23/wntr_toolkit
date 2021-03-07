import json
import time
import pandas as pd
from EPANETUtils import EPANETUtils



def leakage_scenario(name):
    print("Starting simulation.....")
    now = time.time()
    epanet_util_instance_new = EPANETUtils("./../data/RaduNegru11Jan2021WithDemands_2.2.inp", "PDD")

    print("Generating leaks.....")
    dict_leaks, dict_diff = epanet_util_instance_new.run_leakage_scenario(leaks_arr=[0.006, 0.012], generate_diff_dict=True)

    print("To calculate it took: {}s".format(time.time() - now))

    # Files are 130MB smaller if there is no indent , indent=4
    with open("1-leaks-dict.json", 'w') as fp:
        json.dump(dict_leaks, fp)

    print("Leaks to file it took: {}s".format(time.time() - now))

    with open("1-diff-dict.json", 'w') as fp:
        json.dump(dict_diff, fp)       # add , indent=4 for visual effect

    later = time.time()
    print("Total duration: {}s".format(later - now))


if __name__ == '__main__':
    leakage_scenario("PyCharm")


"""
TODO make this a test all OK function

def execution_main(name):
    print("Starting simulation.....")
    now = time.time()
    epanet_util_instance = EPANETUtils("./../data/RaduNegru11Jan2021WithDemands_2.2.inp", "PDD")

    # epanet_util_instance.generate_network_json()
    # epanet_util_instance.generate_pressures_at_nodes(file_name="temp_pressures", to_bars=False)
    # epanet_util_instance.generate_flowrate_on_pipes(file_name="temp_flow")
    # epanet_util_instance.interactive_visualization(node_size=12, title='Scheme of the network', figsize=[1500, 900])
    # epanet_util_instance.add_leakage_on_node_and_run_simulation("", "")
    print("Generating leaks.....")
    dict_leaks, dict_diff = epanet_util_instance.run_leakage_scenario()

    print("To calculate it took: {}s".format(time.time() - now))
    # df_leak.to_json("test-1.json", indent=4)
    with open("just-leaks-dict.json", 'w') as fp:
        json.dump(dict_leaks, fp, indent=4)

    later = time.time()
    print("Total duration: {}s".format(later - now))

    df = pd.DataFrame.from_dict(dict_leaks)
    print(df)
"""