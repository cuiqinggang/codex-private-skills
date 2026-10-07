# SYSTEM RESOURCE LEASE STATE V1

STATE_VERSION=1
CONTRACT_VERSION=4
AUTHORITY=BRAIN19
PURPOSE=Shared-resource arbitration for blind triple stress.

RESOURCE github-main-writer
MODE=EXCLUSIVE_WRITE
OWNER=NONE
QUEUE=EMPTY

RESOURCE persistent-browser
MODE=SINGLE_INSTANCE_CONTROL_LEASE
OWNER=NONE
QUEUE=EMPTY

RESOURCE windows-executor
MODE=EXCLUSIVE_CONTROL_PER_CONFLICTING_NODE
OWNER=NONE
QUEUE=EMPTY

RESOURCE shared-filesystem
MODE=PATH_SCOPED_WRITE_LEASE
OWNER=NONE
QUEUE=EMPTY

RESOURCE upload-download-staging
MODE=PATH_SCOPED_WRITE_LEASE
OWNER=NONE
QUEUE=EMPTY

RESOURCE global-cache-service
MODE=EXCLUSIVE_MUTATION_OR_SHARED_READ
OWNER=NONE
QUEUE=EMPTY

RESOURCE compute-slot
MODE=CAPACITY_SCOPED
OWNER=NONE
QUEUE=EMPTY

LEASE_KEY=RESOURCE_ID + TASK_ID + NODE_ID + OWNER_ID
RULES:
- acquire/release must be evidenced;
- only concrete conflicting nodes serialize;
- no task owns unrelated resources globally;
- release cannot destroy another task's active use;
- absence of provable arbitration on a truly conflicting write/control node is a blocking fault.
