from typing import Dict, List
from deepdiff import DeepDiff


def diff_ssr_states(states: Dict[str, dict]) -> List[dict]:
    """
    Diff SSR states across auth contexts.
    The first context is treated as baseline.
    """
    findings = []

    context_names = list(states.keys())
    if len(context_names) < 2:
        return findings

    baseline_name = context_names[0]
    baseline_state = states[baseline_name]

    for other_name in context_names[1:]:
        diff = DeepDiff(
            baseline_state,
            states[other_name],
            ignore_order=True,
            verbose_level=2,
        )

        if diff:
            findings.append(
                {
                    "type": "authorization_inconsistency",
                    "baseline": baseline_name,
                    "other": other_name,
                    "diff": diff.to_dict(),
                }
            )

    return findings