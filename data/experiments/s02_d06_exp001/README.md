# EXP-001: Multi-Source Conflict Detection

**Sprint:** 2 | **Day:** 6 | **Date:** 2026-01-25

## Summary

Test whether the RAG system can identify and cite different sources when documents contain conflicting information.

## Full Documentation

See: [docs/experiments/EXP-001_multi-source-detection.md](../../../docs/experiments/EXP-001_multi-source-detection.md)

## Test Data

| File | Description |
|------|-------------|
| `policy_2023.md` | Policy with 30-day refund window |
| `policy_2024.md` | Policy with 60-day refund window |

## Key Finding

- Retrieval works correctly (both sources retrieved)
- Conflict detection depends on query phrasing
- Simple queries may cite only one source

## Result

**PARTIAL** - Cross-source retrieval works, conflict identification inconsistent
