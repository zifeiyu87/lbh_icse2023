import os
import pandas as pd
from NormalProcessModel.Config import *


'''
func desc: Extract features for clustering (event type)
'''
def cal_activity_profile(scene: str):
    input_path = f"{NORMAL_PROCESS_LOG_DIR}/{scene}_process_log.csv"
    df = pd.read_csv(input_path)
    df = df.loc[df['scene'] == scene]
    activity_profile = []
    for case_id, group in df.groupby('case:concept:name'):
        repo = case_id.split("#")[0]
        pr_number = case_id.split("#")[1]
        submit_commit_cnt = group.loc[group['concept:name'] == 'SubmitCommit'].shape[0]
        open_pr_cnt = group.loc[group['concept:name'] == 'OpenPR'].shape[0]
        revise_cnt = group.loc[group['concept:name'] == 'Revise'].shape[0]
        review_requested_cnt = group.loc[group['concept:name'] == 'ReviewRequested'].shape[0]
        review_request_removed_cnt = group.loc[group['concept:name'] == 'ReviewRequestRemoved'].shape[0]
        issue_comment_cnt = group.loc[group['concept:name'] == 'IssueComment'].shape[0]
        review_comment_cnt = group.loc[group['concept:name'] == 'ReviewComment'].shape[0]
        review_approved_cnt = group.loc[group['concept:name'] == 'ReviewApproved'].shape[0]
        review_rejected_cnt = group.loc[group['concept:name'] == 'ReviewRejected'].shape[0]
        close_pr_cnt = group.loc[group['concept:name'] == 'ClosePR'].shape[0]
        merge_pr_cnt = group.loc[group['concept:name'] == 'MergePR'].shape[0]
        delete_branch_cnt = group.loc[group['concept:name'] == 'DeleteBranch'].shape[0]
        referenced_cnt = group.loc[group['concept:name'] == 'Referenced'].shape[0]
        # reopen_pr_cnt = group.loc[group['concept:name'] == 'ReopenPR'].shape[0]
        # review_dismissed_cnt = group.loc[group['concept:name'] == 'ReviewDismissed'].shape[0]

        feature = [repo, pr_number, submit_commit_cnt, open_pr_cnt, revise_cnt, review_requested_cnt,
                   review_request_removed_cnt, issue_comment_cnt, review_comment_cnt, review_approved_cnt,
                   review_rejected_cnt, close_pr_cnt, merge_pr_cnt, delete_branch_cnt, referenced_cnt]
        activity_profile.append(feature)
    # save as file
    columns = ['repo', 'pr_number', 'SubmitCommit', 'OpenPR', 'Revise', 'ReviewRequested', 'ReviewRequestRemoved',
               'IssueComment', 'ReviewComment', 'ReviewApproved', 'ReviewRejected', 'ClosePR', 'MergePR',
               'DeleteBranch', 'Referenced']
    df_activity = pd.DataFrame(data=activity_profile, columns=columns)
    return df_activity


'''
func desc: Extract features for clustering (transition type)
'''
def cal_transition_profile(scene: str):
    input_path = f"{NORMAL_PROCESS_LOG_DIR}/{scene}_process_log.csv"
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


def auto_analysis(scene):
    # delete old result file
    filepath = f"{NORMAL_CLUSTER_DIR}/{scene}_cluster.csv"
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"delete old file: {filepath}")
    # calculate feature
    df_activity = cal_activity_profile(scene)
    df_transition = cal_transition_profile(scene)
    df_feature = pd.merge(df_activity, df_transition, how='outer', on=['repo', 'pr_number'])
    df_feature.fillna(0, inplace=True)
    # save as file
    output_path = f"{NORMAL_CLUSTER_DIR}/{scene}_cluster.csv"
    df_feature.to_csv(output_path, index=False, header=True)


if __name__ == '__main__':
    for scene in PR_TYPES:
        auto_analysis(scene)
        print(f"{scene} process done")