import runpy,unittest,copy
from pathlib import Path

# Only an offline gate test; no business/model/runtime is called.
ns=runpy.run_path('evaluate_value_v2.py')
test=runpy.run_path('test_evaluate_value.py')
data=test['fixture']()
data['preregistered_orders']=[['B','A'] if n%2 else ['A','B'] for n in range(1,11)]
for p,order in zip(data['pairs'],data['preregistered_orders']):p['order']=order
assert ns['evaluate'](data)['ten_round_gate_passed']
bad=copy.deepcopy(data);bad['pairs'][0]['order']=['A','B']
assert not ns['evaluate'](bad)['time_comparison_valid']
bad=copy.deepcopy(data);bad['preregistered_orders']=[['A','B']]*10
assert not ns['evaluate'](bad)['time_comparison_valid']
print('3/3 explicit-order gate cases passed; synthetic only')
