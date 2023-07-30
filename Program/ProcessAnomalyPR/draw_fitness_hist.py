import matplotlib.pyplot as plt
import pandas as pd
from matplotlib_venn import venn2
from ProcessAnomalyPR.Config import *


def draw_single_anomaly_pr_fitness_hist(anomaly_type):
    input_path = f"{PROCESS_ANOMALY_PR_DIR}/process_anomaly_pr.xls"
    df = pd.read_excel(input_path)
    df_anomaly = df.loc[df[anomaly_type] == 1]
    fitness_list = df_anomaly['fitness'].tolist()

    # draw hist
    output_path = f"{FIGURE_DIR}/{anomaly_type}_fitness.pdf"
    plt.title(f"Fitness distribution of {anomaly_type.replace('_', ' ')}")
    plt.xlabel("Fitness of sample")
    plt.ylabel("Number of sample")
    plt.hist(fitness_list, bins=20)
    plt.savefig(output_path)
    plt.cla()
    plt.close()


def draw_process_anomaly_pr_fitness_hist():
    input_path = f"{PROCESS_ANOMALY_PR_DIR}/process_anomaly_pr.xls"
    df = pd.read_excel(input_path)
    df_anomaly = df.loc[(df['semantic_anomaly'] == 1) & (df['control_flow_anomaly'] == 1)]
    fitness_list = df_anomaly['fitness'].tolist()

    # draw hist
    output_path = f"{FIGURE_DIR}/process_anomaly_fitness.pdf"
    plt.title('Fitness distribution of semantic & control flow anomaly')
    plt.xlabel("Fitness of sample")
    plt.ylabel("Number of sample")
    plt.hist(fitness_list, bins=20)
    plt.savefig(output_path)
    plt.cla()
    plt.close()


def draw_normal_pr_fitness_hist():
    # get conformance checking result
    alignment_path = f"{ALIGNMENTS_DIR}/alignments_total_result.csv"
    df_alignment = pd.read_csv(alignment_path)

    # get case_id of prs with process anomaly
    anomaly_path = f"{PROCESS_ANOMALY_PR_DIR}/process_anomaly_pr.xls"
    df_anomaly = pd.read_excel(anomaly_path)
    anomaly_case_ids = df_anomaly['case_id'].tolist()

    # fitness of normal sample
    df_normal = df_alignment.loc[~df_alignment['case_id'].isin(anomaly_case_ids)]
    fitness_list = df_normal['fitness'].tolist()

    # draw hist
    output_path = f"{FIGURE_DIR}/normal_fitness.pdf"
    plt.title('Fitness distribution of normal sample')
    plt.xlabel("Fitness of sample")
    plt.ylabel("Number of sample")
    plt.hist(fitness_list, bins=20)
    plt.savefig(output_path)
    plt.cla()
    plt.close()


'''
func desc: draw_venn
'''
def draw_venn_of_process_anomaly():
    input_path = f"{PROCESS_ANOMALY_PR_DIR}/process_anomaly_pr.xls"
    df = pd.read_excel(input_path)

    control_flow_anomaly_num = df.loc[df['control_flow_anomaly'] == 1].shape[0]
    semantic_anomaly_num = df.loc[df['semantic_anomaly'] == 1].shape[0]
    process_anomaly_num = df.loc[(df['semantic_anomaly'] == 1) & (df['control_flow_anomaly'] == 1)].shape[0]

    venn2(subsets=(control_flow_anomaly_num, semantic_anomaly_num, process_anomaly_num),
          set_labels=('control flow anomaly', 'semantic anomaly'))
    # plt.show()
    plt.savefig(f"{FIGURE_DIR}/process_anomaly_venn.pdf")


if __name__ == '__main__':
    # for anomaly_type in ['control_flow_anomaly', 'semantic_anomaly']:
    #     draw_single_anomaly_pr_fitness_hist(anomaly_type)
    # draw_process_anomaly_pr_fitness_hist()
    draw_normal_pr_fitness_hist()
    # draw_venn_of_process_anomaly()
