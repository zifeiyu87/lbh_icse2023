import os
import pandas as pd
from LabelData.Config import *
from sklearn.cluster import KMeans


'''
功能：提取聚类特征(PR包含的事件类型)
'''
def cal_activity_profile(scene: str):
    input_path = f"{SCENE_PROCESS_LOG_DIR}/{scene}_process_log.csv"
    df = pd.read_csv(input_path)
    df = df.loc[df['scene'] == scene]
    activity_profile = []
    for case_id, group in df.groupby('case:concept:name'):
        repo = case_id.split("#")[0]
        pr_number = case_id.split("#")[1]
        submit_commit_cnt = 1 if group.loc[group['concept:name'] == 'SubmitCommit'].shape[0] > 0 else 0
        open_pr_cnt = 1 if group.loc[group['concept:name'] == 'OpenPR'].shape[0] > 0 else 0
        revise_cnt = 1 if group.loc[group['concept:name'] == 'Revise'].shape[0] > 0 else 0
        issue_comment_cnt = 1 if group.loc[group['concept:name'] == 'IssueComment'].shape[0] > 0 else 0
        review_comment_cnt = 1 if group.loc[group['concept:name'] == 'ReviewComment'].shape[0] > 0 else 0
        review_approved_cnt = 1 if group.loc[group['concept:name'] == 'ReviewApproved'].shape[0] > 0 else 0
        review_rejected_cnt = 1 if group.loc[group['concept:name'] == 'ReviewRejected'].shape[0] > 0 else 0
        close_pr_cnt = 1 if group.loc[group['concept:name'] == 'ClosePR'].shape[0] > 0 else 0
        merge_pr_cnt = 1 if group.loc[group['concept:name'] == 'MergePR'].shape[0] > 0 else 0
        delete_branch_cnt = 1 if group.loc[group['concept:name'] == 'DeleteBranch'].shape[0] > 0 else 0
        # reopen_pr_cnt = 1 if group.loc[group['concept:name'] == 'ReopenPR'].shape[0] > 0 else 0
        # review_dismissed_cnt = 1 if group.loc[group['concept:name'] == 'ReviewDismissed'].shape[0] > 0 else 0

        feature = [repo, pr_number, submit_commit_cnt, open_pr_cnt, revise_cnt, issue_comment_cnt, review_comment_cnt,
                   review_approved_cnt, review_rejected_cnt, close_pr_cnt, merge_pr_cnt, delete_branch_cnt]
        activity_profile.append(feature)
    # 保存到文件
    columns = ['repo', 'pr_number', 'SubmitCommit', 'OpenPR', 'Revise', 'IssueComment', 'ReviewComment',
               'ReviewApproved', 'ReviewRejected', 'ClosePR', 'MergePR', 'DeleteBranch']
    df_activity = pd.DataFrame(data=activity_profile, columns=columns)
    return df_activity


'''
功能：提取聚类特征(边向量)
'''
def cal_transition_profile(scene: str):
    input_path = f"{SCENE_PROCESS_LOG_DIR}/{scene}_process_log.csv"
    df = pd.read_csv(input_path)
    transition_profile = []
    for case_id, group in df.groupby('case:concept:name'):
        repo = case_id.split("#")[0]
        pr_number = case_id.split("#")[1]
        edge_vector = {'repo': repo, 'pr_number': pr_number}
        for i in range(group.shape[0] - 1):
            prev = group['concept:name'].iloc[i]
            next = group['concept:name'].iloc[i+1]
            edge = prev + "_" + next
            if edge not in edge_vector:
                edge_vector[edge] = 1
            else:
                edge_vector[edge] += 1
        transition_profile.append(edge_vector)
    df_transition = pd.DataFrame(transition_profile)
    df_transition.fillna(0, inplace=True)
    return df_transition


'''
功能：K-means聚类算法
'''
def k_means_algorithm(scene, k):
    input_path = f"{CLUSTER_DIR}/{scene}_cluster.csv"
    df = pd.read_csv(input_path)
    feature = df.iloc[:, 2:]
    model = KMeans(n_clusters=k, random_state=0).fit(feature)
    df['label'] = model.labels_
    df.to_csv(input_path, index=False, header=True)


'''
功能：手肘法确定最佳聚类数量 https://blog.csdn.net/qq_40290810/article/details/112788973
'''
def kmeans_elbow(scene):
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans

    # 准备数据
    input_path = f"{CLUSTER_DIR}/{scene}_cluster.csv"
    df = pd.read_csv(input_path)
    feature = df.iloc[:, 2:]
    # 计算不同簇对应的SSE
    min_cluster = 2
    max_cluster = 15
    distortions = []
    for i in range(min_cluster, max_cluster):
        kmModel = KMeans(n_clusters=i)
        kmModel.fit(feature)
        distortions.append(kmModel.inertia_)  # 获取K-means算法的SSE
    # 绘制曲线
    plt.title(scene)
    plt.plot(range(min_cluster, max_cluster), distortions, marker="o")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel("簇数量")
    plt.ylabel("簇内误方差(SSE)")
    plt.show()


'''
功能：自动化流程
'''
def auto_analysis(scene):
    # 先删除旧文件
    filepath = f"{CLUSTER_DIR}/{scene}_cluster.csv"
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"删除旧文件{filepath}")
    # 计算聚类特征
    df_transition = cal_transition_profile(scene)
    # 保存为文件
    output_path = f"{CLUSTER_DIR}/{scene}_cluster.csv"
    df_transition.to_csv(output_path, index=False, header=True)


if __name__ == '__main__':
    for scene in PR_TYPES:
        auto_analysis(scene)
        print(f"{scene} process done")

    # kmeans_elbow("fork_merge")

    # k_means_algorithm("fork_merge", 6)
    # k_means_algorithm("fork_close", 6)
    # k_means_algorithm("unfork_merge", 4)
    # k_means_algorithm("unfork_close", 4)