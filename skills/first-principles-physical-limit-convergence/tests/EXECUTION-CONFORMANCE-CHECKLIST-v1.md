# v3.1 Execution Conformance Regression Checklist

任何应用本技能的真实任务，FINAL-99 前必须证明：

~~~text
E01 METHOD_VERSION=3.1.0
E02 TASK_CONTRACT frozen
E03 VALID_CONTRACT frozen
E04 Gate 0 mature-solution evidence exists
E05 Step 2 only runs from FROZEN CALIBRATION_PLAN
E06 Step 4 only runs from FROZEN VIRTUAL_99_FINAL_PLAN
E07 every real action passed PRE_ACTION_CONFORMANCE_GATE
E08 EXECUTION_CONFORMANCE_RATE=100%
E09 UNAUTHORIZED_ACTION_COUNT=0
E10 REAL_SEARCH_ACTION_COUNT=0
E11 PLAN_MUTATION_DURING_REAL_EXECUTION=0
E12 OUT_OF_PLAN_CONTINUE_COUNT=0
E13 unknown/out-of-plan event -> STOP + REALITY_DELTA + RETURN_TO_GPT
E14 legacy L0/L1/L2/L3/L4 cannot authorize current action
E15 PASS_BY_DESIGN is not accepted as runtime proof
E16 evidence coverage=100%
~~~

任一 FAIL：

~~~text
FINAL_99=NO
FREEZE=NO
~~~
