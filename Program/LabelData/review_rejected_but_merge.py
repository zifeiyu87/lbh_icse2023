import pandas as pd
from LabelData.Config import *
from utils.url_utils import get_user_email

'''
func desc: Identify semantic anomalies pr (ReviewRejected → MergePR)
'''
def review_rejected_but_merge(repo: str, scene: str):
    anomaly_pr = []
    # Load Edge Vector data
    input_path = f"{CLUSTER_DIR}/{scene}_cluster.csv"
    df = pd.read_csv(input_path)
    if 'ReviewRejected_MergePR' not in df.columns:
        return anomaly_pr
    # Load log data
    log_path = f"{EVENT_LOG_DIR}/{repo}_event_log.csv"
    df_log = pd.read_csv(log_path)
    # Identify semantic anomalies pr (ReviewRejected → MergePR)
    df_check = df.loc[(df['ReviewRejected_MergePR'] > 0) & (df['repo'] == repo)]
    for index, row in df_check.iterrows():
        pr_number = int(row['pr_number'])
        group = df_log.loc[df_log['case:concept:name'] == pr_number]

        # Obtain user information (username, email) for OpenPR
        df_open = group.loc[group['concept:name'] == 'OpenPR']
        contributor_name = df_open['people'].iloc[0]
        contributor_email = get_user_email(contributor_name)

        # Obtain user information (username, email) for the last ReviewRejected
        df_review = group.loc[group['concept:name'] == 'ReviewRejected']
        reviewer_name = df_review['people'].iloc[-1]
        reviewer_email = get_user_email(reviewer_name)

        # Obtain user information (username, email) for MergePR
        df_merge = group.loc[group['concept:name'] == 'MergePR']
        maintainer_name = df_merge['people'].iloc[-1]
        maintainer_email = get_user_email(maintainer_name)

        # Obtain comments after MergePR
        df_merge_comment = group.loc[(group['concept:name'] == 'IssueCommentSupplement')
                                     & (group['people'] == maintainer_name)]
        merge_comment = df_merge_comment['message'].iloc[0] if (df_merge_comment.shape[0] > 0) else None

        # Determine the Subtyping of semantic anomalies PR
        pr_type = 0
        if maintainer_name == contributor_name:
            pr_type = 1
        elif maintainer_name == reviewer_name:
            pr_type = 2
        else:
            pr_type = 3

        pr_subtype = 1 if df_merge_comment.shape[0] > 0 else 2

        anomaly_pr.append([repo, pr_number, pr_type, pr_subtype, merge_comment,
                           contributor_name, contributor_email,
                           reviewer_name, reviewer_email,
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
        result1 = review_rejected_but_merge(repo, "fork_merge")
        result2 = review_rejected_but_merge(repo, "unfork_merge")
        anomaly_pr.extend(result1)
        anomaly_pr.extend(result2)
        print(f"{repo} process done")
    # save as file
    df_file = pd.DataFrame(data=anomaly_pr, columns=[
        'repo', 'pr_number', 'pr_type', 'pr_subtype', 'explain',
        'contributor_name', 'contributor_email',
        'reviewer_name', 'reviewer_email',
        'maintainer_name', 'maintainer_email'])
    output_path = f"{ANOMALY_PR_DIR}/review_rejected_but_merge.xls"
    df_file.to_excel(output_path, index=False, header=True, encoding='utf-8-sig')


if __name__ == '__main__':
    auto_analysis()