from crisisbench.data import load_tasks
from crisisbench.verify import verify_dataset

def test_dataset_contract():
    v=verify_dataset("."); assert v["status"]=="PASS"; assert v["base_tasks"]==36; assert v["condition_cells"]==180

def test_domains_balanced():
    tasks=load_tasks("data/base_tasks"); counts={}
    for t in tasks: counts[t.domain]=counts.get(t.domain,0)+1
    assert set(counts.values())=={6}
