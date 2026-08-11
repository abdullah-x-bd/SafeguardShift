from safeguardshift.analysis import bootstrap_mean,cluster_summary,completeness,wilson
from safeguardshift.data import load_tasks


def test_wilson():
    lo,hi=wilson(1,156); assert 0<=lo<hi<=1


def test_bootstrap_deterministic():
    assert bootstrap_mean([0,1,1],reps=100)==bootstrap_mean([0,1,1],reps=100)


def test_cluster_summary_collapses_within_task_before_bootstrap():
    result=cluster_summary({"task-a":[0.0,1.0],"task-b":[1.0,1.0]},seed=1)
    assert result["task_n"]==2
    assert result["task_values"]=={"task-a":0.5,"task-b":1.0}
    assert result["mean"]==0.75


def test_backbone_completeness_contract_is_4320_unique_cells():
    tasks=load_tasks(); models=["m0","m1","m2","m3"]
    rows=[]
    for model in models:
        for task in tasks:
            for rep in (1,2,3):
                for condition in ("full","relevant_ablation","irrelevant_ablation","substitute","compound_ablation"):
                    rows.append({"model":model,"task_id":task.task_id,"replicate":rep,"condition":condition})
    result=completeness(rows,expected_models=4,expected_tasks=72,expected_replicates={1,2,3})
    assert result["status"]=="PASS"
    assert result["rows"]==4320
    assert result["unique_cells"]==4320
    assert result["missing_count"]==0
