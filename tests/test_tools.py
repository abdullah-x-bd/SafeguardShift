from crisisbench.tools import tool_schema

def test_tool_contract():
    tools=tool_schema(); names=[t["function"]["name"] for t in tools]; assert len(names)==5; assert len(names)==len(set(names)); assert "submit_final_plan" in names
