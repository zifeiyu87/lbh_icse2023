import json

import pandas as pd
from utils.pr_self_utils import get_pr_requested_reviewer_list, cal_pr_subtype, get_user_info_who_close_pr
from LabelData.Config import *
from utils.url_utils import get_user_email

'''
func desc: Identify semantic anomalies pr (ReviewRequested → ClosePR)
'''
def no_reviewer_response_but_close(repo: str, scene: str):
    anomaly_pr = []
    # Load Edge Vector data
    input_path = f"{CLUSTER_DIR}/{scene}_cluster.csv"
    df = pd.read_csv(input_path)
    if 'ReviewRequested_ClosePR' not in df.columns:
        return anomaly_pr
    # Load log data
    log_path = f"{EVENT_LOG_DIR}/{repo}_event_log.csv"
    df_log = pd.read_csv(log_path)
    # Identify semantic anomalies pr (ReviewRequested → MergePR)
    df_check = df.loc[(df['repo'] == repo) & (df['ReviewRequested_ClosePR'] > 0)]
    for index, row in df_check.iterrows():
        pr_number = int(row['pr_number'])
        group = df_log.loc[df_log['case:concept:name'] == pr_number]

        # Obtain user information (username, email) for OpenPR
        df_open = group.loc[group['concept:name'] == 'OpenPR']
        contributor_name = df_open['people'].iloc[0]
        contributor_email = get_user_email(contributor_name)

        # Obtain user information (username, email) for RequestedReviewer
        requested_reviewer_name_list = get_pr_requested_reviewer_list(repo, pr_number)
        requested_reviewer_email_list = [get_user_email(username) for username in requested_reviewer_name_list]

        # Obtain user information (username, email) for ClosePR
        df_close = group.loc[group['concept:name'] == 'ClosePR']
        person = df_close['people'].iloc[-1]
        description = json.loads(df_close['description'].iloc[-1])
        maintainer_name, maintainer_email = get_user_info_who_close_pr(person, description)

        # Determine the Subtyping of semantic anomalies PR
        pr_type = 0
        if maintainer_name == contributor_name:
            pr_type = 1
        elif maintainer_name in requested_reviewer_name_list:
            pr_type = 2
        else:
            pr_type = 3

        pr_subtype, explain = cal_pr_subtype(repo, pr_number, group, maintainer_name)

        anomaly_pr.append([repo, pr_number, pr_type, pr_subtype, explain,
                           contributor_name, contributor_email,
                           str(requested_reviewer_name_list), str(requested_reviewer_email_list),
                           maintainer_name, maintainer_email])
    return anomaly_pr


def auto_analysis():
    projects = ['openzipkin/zipkin', 'apache/netbeans', 'opencv/opencv', 'apache/dubbo', 'phoenixframework/phoenix',
                'apache/zookeeper', 'spring-projects/spring-framework', 'spring-cloud/spring-cloud-function',
                'vim/vim', 'gpac/gpac', 'ImageMagick/ImageMagick', 'apache/hadoop', 'libexpat/libexpat',
                'apache/httpd', 'madler/zlib', 'redis/redis', 'stefanberger/swtpm', 'tensorflow/tensorflow']
    anomaly_pr = []
    for pro in projects:
        repo = pro.split('/')[1]
        result1 = no_reviewer_response_but_close(repo, "fork_close")
        result2 = no_reviewer_response_but_close(repo, "unfork_close")
        anomaly_pr.extend(result1)
        anomaly_pr.extend(result2)
        print(f"{repo} process done")
    df_file = pd.DataFrame(data=anomaly_pr, columns=[
                           'repo', 'pr_number', 'pr_type', 'pr_subtype', 'explain',
                           'contributor_name', 'contributor_email',
                           'requested_reviewer_name', 'requested_reviewer_email',
                           'maintainer_name', 'maintainer_email'])
    output_path = f"{ANOMALY_PR_DIR}/no_reviewer_response_but_close.xls"
    df_file.to_excel(output_path, index=False, header=True, encoding="utf-8-sig")


if __name__ == '__main__':
    auto_analysis()