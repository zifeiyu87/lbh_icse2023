import pm4py
from ProcessMining.Config import *
from utils.log_utils import log_info, get_event_log_from_file

'''
function desc: process event log
'''
def process_event_log(repo: str):
    # load data
    input_path = f"{EVENT_LOG_DIR}/{repo}_event_log.csv"
    log = get_event_log_from_file(input_path)
    print("origin log")
    log_info(log)
    # Filter cases containing low-frequency behavior (ReopenPR)
    log = pm4py.filter_event_attribute_values(log, 'concept:name', ['ReopenPR'], level="case", retain=False)
    print("filter_event_attribute_values (ReopenPR)")
    log_info(log)
    # select key activities
    activities = ['SubmitCommit', 'OpenPR', 'Revise',
                  'IssueComment', 'ReviewComment', 'ReviewApproved', 'ReviewRejected',
                  'ClosePR', 'MergePR', 'DeleteBranch', 'ReviewRequested', 'Referenced', 'HeadRefForcePushed',
                  'ReviewRequestRemoved']
    log = log.loc[log['concept:name'].isin(activities)]
    # convert HeadRefForcePushed to Revise
    log['concept:name'] = log['concept:name'].apply(lambda x: 'Revise' if x == 'HeadRefForcePushed' else x)
    log = log[['case:concept:name', 'concept:name', 'time:timestamp', 'people', 'scene']]
    # save as file
    output_path = f"{PROCESS_LOG_DIR}/{repo}_process_log.csv"
    log.to_csv(output_path, index=False, header=True, encoding="utf-8-sig")


if __name__ == '__main__':
    projects = ['openzipkin/zipkin', 'apache/netbeans', 'opencv/opencv', 'apache/dubbo', 'phoenixframework/phoenix',
                'apache/zookeeper', 'spring-projects/spring-framework', 'spring-cloud/spring-cloud-function',
                'vim/vim', 'gpac/gpac', 'ImageMagick/ImageMagick', 'apache/hadoop', 'libexpat/libexpat',
                'apache/httpd', 'madler/zlib', 'redis/redis', 'stefanberger/swtpm', 'tensorflow/tensorflow']
    for pro in ['faker-js/faker']:
        repo = pro.split('/')[1]
        process_event_log(repo)
        print(f"repo#{repo} process done\n")

