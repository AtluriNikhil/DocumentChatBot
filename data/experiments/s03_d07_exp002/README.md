# EXP-002: Cross-Lingual Retrieval

**Sprint:** 3 | **Day:** 7 | **Date:** 2026-01-26

## Summary

Validate that multilingual-e5-large enables cross-lingual retrieval (German query retrieves English documents and vice versa).

## Files

| File | Description |
|------|-------------|
| `exp_002_cross_lingual.py` | Experiment script with methodology documentation |
| `exp_002_results.json` | Experiment results |

## Configuration

| Parameter | Value |
|-----------|-------|
| Embedding Model | intfloat/multilingual-e5-large |
| Vector Dimension | 1024 |
| Test Cases | 4 (2 DE→EN, 2 EN→DE) |

## Key Finding

- Cross-lingual retrieval effective with multilingual-e5-large
- 75% success rate on language-mismatch queries
- One EN→DE case retrieved same-language docs

## Result

**PASS** - 75% cross-lingual retrieval success rate

## References

- [MMTEB Benchmark](https://arxiv.org/html/2502.13595v4)
- [Multilingual E5 Technical Report](https://arxiv.org/html/2402.05672v1)
