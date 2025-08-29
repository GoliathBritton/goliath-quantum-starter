from hypothesis import given, strategies as st
from src.nqba_stack.core.decision_logic import evaluate_decision

def test_decision_logic_basic():
    assert evaluate_decision({'score': 1}) in [True, False]

@given(st.dictionaries(keys=st.text(), values=st.integers()))
def test_decision_logic_property(input_dict):
    # Should not raise and must return a boolean
    result = evaluate_decision(input_dict)
    assert isinstance(result, bool)
