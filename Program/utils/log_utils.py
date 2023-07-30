import pandas as pd
import pm4py
from utils.mysql_utils import select_all

'''
func desc: load event log from file
'''
def get_event_log_from_file(filepath):
    log = pd.read_csv(filepath, parse_dates=['time:timestamp'])
    log['case:concept:name'] = log['case:concept:name'].astype(str)
    return log


'''
func desc: load event log from database
'''
def get_event_log_from_sql(repo: str):
    table = f"{repo.replace('-', '_')}_event_log"
    sql = f"select * from `{table}`"
    data = select_all(sql)
    return data


'''
func desc: print log info
'''
def log_info(log):
    cases = log['case:concept:name'].unique()
    variants = pm4py.get_variants(log)
    case_num = len(cases)
    variants_num = len(variants)
    print(f"case num:{case_num}, variants num:{variants_num}")
    return case_num, variants_num


'''
func desc: process event log
'''
def process_log(scene, log):
    anomaly_branchs = ['ReviewRequested_DeleteBranch', 'ReviewApproved_DeleteBranch', 'DeleteBranch_DeleteBranch', 'ClosePR_ClosePR',
                       'MergePR_Revise', 'MergePR_ReviewRequested', 'MergePR_ReviewRequestRemoved', 'MergePR_ReviewApproved',
                       'ClosePR_Revise', 'ClosePR_ReviewRequested', 'ClosePR_ReviewRequestRemoved', 'ClosePR_ReviewApproved',
                       'ReviewRequested_MergePR', 'ReviewRequested_ClosePR', 'ReviewRejected_MergePR', 'ReviewApproved_ClosePR']
    input_path = f"../LabelData/cluster/{scene}_cluster.csv"
    df = pd.read_csv(input_path)
    df['case_id'] = df.apply(lambda x: x['repo'] + '#' + str(x['pr_number']), axis=1)
    for branch in anomaly_branchs:
        if branch in df.columns:
            df = df.loc[df[branch] == 0]
    case_list = df['case_id'].tolist()
    log = log.loc[log['case:concept:name'].isin(case_list)]
    return log


'''
func desc: Select high-frequency variants based on the minimum overall coverage rate {min_coverage}
'''
def filter_variants_by_min_total_coverage(log, min_coverage: float):
    total_case = len(log['case:concept:name'].unique())
    case_num_threshold = int(min_coverage * total_case)

    filter_variant = []
    cnt = 0

    variants = pm4py.get_variants(log)
    order_variants = sorted(variants.items(), key=lambda x: x[1], reverse=True)
    for variant in order_variants:
        variant_name = variant[0]
        variant_num = variant[1]
        cnt += variant_num
        filter_variant.append(variant_name)
        if cnt >= case_num_threshold:
            break
    return filter_variant