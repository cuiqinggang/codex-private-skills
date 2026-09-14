def environment_drift_fails(drift, mde):
    return abs(drift["projected_span_ms"]) > mde and drift["permutation_p_two_sided"] < 0.05

def order_effect_state(order_ci, equivalence_bound_ms):
    low, high = order_ci
    if low >= -equivalence_bound_ms and high <= equivalence_bound_ms:
        return "PASS"
    if low > equivalence_bound_ms or high < -equivalence_bound_ms:
        return "FAIL"
    return "INCONCLUSIVE"
