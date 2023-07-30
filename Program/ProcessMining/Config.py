from utils.file_utils import create_dir_if_not_exist

COVERAGE_THRESHOLD = 0.8

PR_TYPES = ["fork_merge", "fork_close", "unfork_merge", "unfork_close"]

EVENT_LOG_DIR = "../DataAcquire/event_log"

# dir of event
PROCESS_LOG_DIR = "process_log"
SCENE_PROCESS_LOG_DIR = "scene_process_log"

# dir of process model
PROCESS_MODEL_DIR = "process_model"
BPMN_DIR = f"{PROCESS_MODEL_DIR}/bpmn"
PETRI_NET_DIR = f"{PROCESS_MODEL_DIR}/petri_net"

# dir of conformance checking result
CONFORMANCE_CHECK_DIR = "conformance_check"
ALIGNMENTS_DIR = f"{CONFORMANCE_CHECK_DIR}/alignments"
TBR_DIR = f"{CONFORMANCE_CHECK_DIR}/tbr"

# dir of the evaluation result of process model
MODEL_EVALUATION_DIR = f"model_evaluation"

create_dir_if_not_exist(PROCESS_LOG_DIR)
create_dir_if_not_exist(SCENE_PROCESS_LOG_DIR)

create_dir_if_not_exist(PROCESS_MODEL_DIR)
create_dir_if_not_exist(BPMN_DIR)
create_dir_if_not_exist(PETRI_NET_DIR)

create_dir_if_not_exist(CONFORMANCE_CHECK_DIR)
create_dir_if_not_exist(TBR_DIR)
create_dir_if_not_exist(ALIGNMENTS_DIR)

create_dir_if_not_exist(MODEL_EVALUATION_DIR)