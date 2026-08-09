# Semantic Evaluation Suite

This directory contains semantic decision evaluations for AI-RD-Studio.

These evaluations are intentionally separated from ordinary software
correctness tests.

## Development

`development/` contains visible semantic cases used during implementation.

These cases may be inspected, debugged, and used to improve deterministic
decision behavior.

They are not pristine holdout evidence.

## Holdout

`holdout/` is reserved for milestone evaluation cases that have not been used
as ordinary tuning targets.

A holdout case that is inspected and then used to modify system behavior is
no longer considered pristine holdout.

Such a case must be treated as a development case and replaced by a new
unseen holdout before future unbiased milestone evaluation.

## Interpretation

Software tests answer:

> Does the implementation satisfy its contracts?

Semantic evaluations answer:

> Does the system behave appropriately under controlled changes in meaning,
> evidence, wording, and irrelevant context?

Semantic pass rates are not claims of intelligence, scientific accuracy, or
real-world success prediction.