# Adversarial Audit

> The purpose of this audit is to look for explanations that weaken an apparent treatment gain.

## Pattern concentration

{
  "rate_deltas": {
    "binary_search": -0.11428571428571427,
    "brute_force_implementation": -0.07500000000000007,
    "dynamic_programming": -0.025000000000000022,
    "graph_traversal_dfs_bfs": -0.02857142857142858
  },
  "net_hits": {
    "binary_search": -4,
    "brute_force_implementation": -3,
    "dynamic_programming": -1,
    "graph_traversal_dfs_bfs": -1
  },
  "dominant_positive_pattern": "dynamic_programming",
  "dominant_positive_pattern_share": null
}

## Program influence

{
  "n_programs": 30,
  "original_delta": -0.06000000000000001,
  "min": -0.07586206896551725,
  "max": -0.048275862068965524,
  "most_influential": "35962547",
  "delta_without_most_influential": -0.07586206896551725
}

## Repetition dependence

{
  "1": -0.13333333333333336,
  "2": -0.1333333333333333,
  "3": 0.0,
  "4": 0.0,
  "5": -0.033333333333333326
}

## Parser failures

{
  "no_prior": {
    "failures": 0,
    "total": 150
  },
  "generic_prior": {
    "failures": 1,
    "total": 150
  }
}

## Prompt-length confound

{
  "no_prior": {
    "mean_chars": 3934.366666666667,
    "mean_tokens_estimate": 984.0333333333333
  },
  "generic_prior": {
    "mean_chars": 4802.633333333333,
    "mean_tokens_estimate": 1201.1333333333334
  }
}

The treatment is necessarily longer because it contains the prior. A token-matched placebo arm is required to separate prior content from prompt-length effects; this two-arm pilot cannot.

## Reasonable statistical alternatives

{
  "paired_program_repetitions": 149,
  "top1_delta": -0.05500000000000001,
  "exam_delta": 0.051899235592136016
}

## Audit verdict

This pilot does not establish a reliable Top-1 improvement: the mean paired delta was -0.060 and its 95% bootstrap interval [-0.127, 0.007] included zero.
