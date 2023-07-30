import pandas as pd
from ProcessAnomalyPR.Config import *


'''
func desc: calculate the distribution of control_flow anomalies PR
'''
def repo_control_flow_anomaly_pr_num(projects):
    input_path = f"{PROCESS_ANOMALY_PR_DIR}/control_flow_anomaly_pr.xls"
    df = pd.read_excel(input_path)
    df['repo'] = df['case_id'].apply(lambda x: x.split("#")[0])
    df['pr_number'] = df['case_id'].apply(lambda x: x.split("#")[1])

    datas = []
    for pro in projects:
        repo = pro.split("/")[1]
        df_repo = df.loc[df['repo'] == repo]
        total_control_flow_anomaly_pr = df_repo.shape[0]
        repo_anomaly_pr = {'repo': repo, 'total_control_flow_anomaly_pr': total_control_flow_anomaly_pr}
        for index, row in df_repo.iterrows():
            labels = row['category'].split(", ")
            for label in labels:
                if label in repo_anomaly_pr:
                    repo_anomaly_pr[label] += 1
                else:
                    repo_anomaly_pr[label] = 1
        datas.append(repo_anomaly_pr)

    # save as file
    output_path = f"{SUMMARY_DIR}/repo_control_flow_anomaly_pr_num.xls"
    df_file = pd.DataFrame(data=datas)
    df_file.fillna(0, inplace=True)
    df_file.to_excel(output_path, index=False, header=True)


'''
func desc: calculate the distribution of semantic anomalies PR
'''
def repo_semantic_anomaly_pr_num(projects, semantic_anomaly_types):
    input_path = f"{PROCESS_ANOMALY_PR_DIR}/semantic_anomaly_pr.xls"
    df = pd.read_excel(input_path)
    df['repo'] = df['case_id'].apply(lambda x: x.split("#")[0])
    df.fillna(0, inplace=True)
    datas = []
    for pro in projects:
        repo = pro.split("/")[1]
        repo_anomaly_pr = {'repo': repo}
        for anomaly_type in semantic_anomaly_types:
            df_filter = df.loc[(df['repo'] == repo) & (df[anomaly_type] > 0)]
            repo_anomaly_pr[anomaly_type] = df_filter.shape[0]
        datas.append(repo_anomaly_pr)

    # save as file
    df_file = pd.DataFrame(data=datas)
    output_path = f"{SUMMARY_DIR}/repo_semantic_anomaly_pr_num.xls"
    df_file.to_excel(output_path, index=False, header=True)


if __name__ == '__main__':
    projects = ['openzipkin/zipkin', 'apache/netbeans', 'opencv/opencv', 'apache/dubbo', 'phoenixframework/phoenix',
                'apache/zookeeper', 'spring-projects/spring-framework', 'spring-cloud/spring-cloud-function',
                'vim/vim', 'gpac/gpac', 'ImageMagick/ImageMagick', 'apache/hadoop', 'libexpat/libexpat',
                'apache/httpd', 'madler/zlib', 'redis/redis', 'stefanberger/swtpm', 'tensorflow/tensorflow']
    semantic_anomaly_types = ["no_reviewer_response_but_close", "no_reviewer_response_but_merge",
                     "review_approved_but_close", "review_rejected_but_merge"]

    repo_control_flow_anomaly_pr_num(projects)
    # repo_semantic_anomaly_pr_num(projects, semantic_anomaly_types)