### Program Directory
Each directory is a relatively independent module used to complete an independent function, such as data crawl, process mining, etc. The global configuration item information is in the `Config.py` script of each module.

1. **DataAcquire**: crawl data
2. **ProcessMining**：Event log preprocessing, process discovery, conformance checking
3. **LabelData**：Identify semantic anomalies
4. **ProcessAnomalyPR**：Identify control-flow anomalies,  Summarize the identification result of control-flow anomalies and semantic anomalies
5. **NormalProcessModel**：Mining normal process models and extracting typical features of models
6. **Kappa**: Calculate the consistency of the classification results of the root causes of semantic anomalies between two reviewers
7. **Utils**: Tool scripts, such as time conversion, log file reading, database reading and writing
### Detailed introduction of the module
#### DataAcquire
##### Function Description
crawl data
##### Step 1: crawl data

1. `crawl_pr_basic_data.py`: Using [Pulls API](https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#get-a-pull-request) to crawl PR basic information
2. `crawl_pr_log.py`: Using [Timeline API](https://docs.github.com/en/rest/issues/timeline?apiVersion=2022-11-28) to crawl PR event log
> Note: The crawled data is directly saved to the database instead of being saved as a local file

##### Step 2: preprocess event log

1. `log_preprocess.py`
   1. func desc：Preliminary processing of PR event logs, including removing PR that are still in an open state, extracting key activities, and classifying activity types
   2. input：None, Directly reading data from the database
   3. output：Save as CSV file to `event_log` directory
#### ProcessMining
##### Function Description
func desc: Event log preprocessing, process discovery, conformance checking
##### Step 1: Data filtering and grouping

1. `event_log_process.py`
   1. func desc
      1. Filter cases containing low-frequency behavior (ReopenPR) and retain only key activities
      2. Format Event Log
   2. input: `../DataAcquire/event_log/`
   3. output: `process_log/`
2. `scene_process_log.py`
   1. func desc 
      1. Eliminating cyclic structures: Merge repetitive and continuous activities into one
      2. Data group：Group cases according to different collaboration scenarios, i.e. _fork & merge, fork & close, non-fork & merge, non-fork & close_
   2. input: `process_log/`
   3. output: `scene_process_log/`
##### Step 2：Construct quasi-normal process model

1. `process_discovery.py`
   1. func desc：Using MOCLPA algorithm to construct quasi-normal process model
   2. input：`scene_process_log`
   3. output：`process_model/petri_net`and`process_model/bpmn`
##### Step 3：Conformance checking

1. `conformance_checking_*.py`
   1. input：`scene_process_log`, `process_model/petri_net/`
   2. output：`conformance_check/alignments/`
   3. func desc：
      1. `conformance_checking_of_high_freq_variants.py`和`conformance_checking_of_low_freq_variants.py`Conduct conformance checking on the case sets corresponding to high-frequency process variants (80%) and low-frequency process variants (20%) respectively
      2. `conformance_checking_result_merge.py` merge conformance checking result
#### LabelData
##### Function Description
Identify four types of semantic anomalies
##### Step 1：Calculate the edge vector ("Activity A → Activity B") for each case

1. `trace_cluster.py`
   1. func desc: Calculate the number of occurrences of different edge vectors in a case
   2. input：`../ProcessMining/scene_process_log/`
   3. output：`cluster/`
##### Step 2：Identify semantic anomalies

1. `no_reviewer_response_but_close.py`, `no_reviewer_response_but_merge.py`, `review_approved_but_close.py`, `review_rejected_but_merge.py`
   1. func desc: Four scripts are used to identify four types of semantic anomalies
   2. input：`cluster/`
   3. output：`anomaly_pr/`
#### ProcessAnomalyPR
##### Function Description
Identify control-flow anomalies,  Summarize the identification result of control-flow anomalies and semantic anomalies
##### Step 1：Calculation process variants

1. `LogVariant.py`
   1. func desc：Calculate the process variants corresponding to each PR. Process variants were used to analyze the causes of control flow anomalies
   2. input：`scene_process_log/`
   3. output：`log_variant/`
##### Step 2：Identify control_flow anomalies

1. `control_flow_anomaly_pr.py`
   1. func desc: 
      1. Identify control_flow anomalies
      2. analyze the causes of control flow anomalies
   2. input：`../ProcessMining/conformance_check/alignments`
   3. output：`process_anomaly_pr/control_flow_anomaly_pr.xls`
##### Step 3：Summarize the identification results of semantic anomalies

2. `semantic_anomaly_pr`
   1. input：`../LabelData/anomaly_pr/`
   2. output：`process_anomaly_pr/semantic_anomaly_pr.xls`
##### Step 4：Summarize the identification results of control_flow anomalies and semantic anomalies

3. `process_anomaly_pr.py`
   1. input：`process_anomaly_pr/`
   2. output：`process_anomaly_pr/process_anomaly_pr.xls`
##### Step 5：calculate the distribution of control_flow anomalies and semantic anomalies

4. `statistic_anomaly_num.py`
   1. func desc:
      1. Calculate the quantity distribution of control_flow anomalies PR in the project
      2. Calculate the quantity distribution of semantic anomalies PR in the project
      3. Count the reasons why semantic anomaly PR was closed
   2. input：`process_anomaly/`
   3. output：`summary/`
#### NormalProcessModel
##### Function Description
Mining normal process models and extracting typical features of models
##### Step 1：Extract normal sample

1. `normal_event_log.py`
   1. func desc: Eliminate control flow anomalies and semantic anomalies to obtain a normal dataset
   2. input：`../ProcessMining/scene_process_log/`
   3. output：`normal_process_log/`
##### Step 2：Construct normal process model

1. `process_discovery.py`
   1. func desc: Using process discovery algorithm to construct normal process model 
   2. input：`normal_process_log/`
   3. output：
      1. process model ：`process_model/petri_net`and`process_model/bpmn`
      2. model evaluation result：`model_evaluation/`
##### Step 3：Extract feature of process model

1. `transition_freq.py`
   1. func desc:
      1. calculate frequency of transition
      2. extract feature of process model
   2. input：`normal_cluster`
   3. output：
      1. frequency of transition：`transition_freq/`
      2. feature of process model：`summary/transiton_percent.xls`
#### Kappa
##### Function Description
Calculate the consistency of the classification results of the root causes of semantic anomalies between two reviewers
![image.png](https://cdn.nlark.com/yuque/0/2023/png/1980167/1685173943057-069001ac-ca59-4468-8ed8-fd584059514a.png#averageHue=%23272c34&clientId=uf9bdc17f-df9c-4&from=paste&height=95&id=uaa45f908&originHeight=173&originWidth=393&originalType=binary&ratio=1.2999999523162842&rotation=0&showTitle=false&size=9175&status=done&style=none&taskId=u33b6c992-bc58-4297-b72a-b41b000f63f&title=&width=215.93407385448057)
##### Step 1: Calculate the Kappa of semantic anomalies

1. `kappa_semantic_anomaly.py`
