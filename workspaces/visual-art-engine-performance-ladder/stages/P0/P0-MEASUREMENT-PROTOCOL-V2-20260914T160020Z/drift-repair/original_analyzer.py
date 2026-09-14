def aa_drift_fails(summary, mde):
    drift = max(
        abs(summary["drift_A"]["projected_span_ms"]),
        abs(summary["drift_A"]["early_minus_late_ms"]),
        abs(summary["pattern_effect_ms"]),
    )
    return drift > mde
