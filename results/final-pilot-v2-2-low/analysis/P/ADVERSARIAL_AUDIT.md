# Adversarial Audit

> The purpose of this audit is to look for explanations that weaken an apparent treatment gain.

## Pattern concentration

{
  "rate_deltas": {
    "binary_search": 0.02857142857142858,
    "brute_force_implementation": 0.17499999999999993,
    "dynamic_programming": -0.10000000000000003,
    "graph_traversal_dfs_bfs": 0.08571428571428572
  },
  "net_hits": {
    "binary_search": 1,
    "brute_force_implementation": 7,
    "dynamic_programming": -4,
    "graph_traversal_dfs_bfs": 3
  },
  "dominant_positive_pattern": "brute_force_implementation",
  "dominant_positive_pattern_share": 0.6363636363636364
}

## Program influence

{
  "n_programs": 30,
  "original_delta": 0.04666666666666667,
  "min": 0.013793103448275865,
  "max": 0.06896551724137931,
  "most_influential": "44917428",
  "delta_without_most_influential": 0.013793103448275865
}

## Repetition dependence

{
  "1": 0.10000000000000003,
  "2": 0.06666666666666665,
  "3": 0.06666666666666671,
  "4": 0.0,
  "5": 0.0
}

## Parser failures

{
  "no_prior": {
    "failures": 0,
    "total": 150
  },
  "pattern_prior": {
    "failures": 0,
    "total": 150
  }
}

## Prompt-length confound

{
  "no_prior": {
    "mean_chars": 3934.366666666667,
    "mean_tokens_estimate": 984.0333333333333
  },
  "pattern_prior": {
    "mean_chars": 4801.7,
    "mean_tokens_estimate": 1200.8
  }
}

The treatment is necessarily longer because it contains the prior. A token-matched placebo arm is required to separate prior content from prompt-length effects; this two-arm pilot cannot.

## Reasonable statistical alternatives

{
  "paired_program_repetitions": 150,
  "top1_delta": 0.04666666666666667,
  "exam_delta": -0.03494862379527952
}

## Audit verdict

This pilot does not establish a reliable Top-1 improvement: the mean paired delta was 0.047 and its 95% bootstrap interval [-0.040, 0.147] included zero.
