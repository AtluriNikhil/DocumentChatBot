# Experiments Registry

Central index of all capability experiments conducted during project development.

**Project:** RAG Document Assistant
**DSM Reference:** C.1.3 Capability Experiment Template

---

## Registry

| ID | Name | Sprint | Day | Date | Result | Folder |
|----|------|--------|-----|------|--------|--------|
| EXP-001 | Multi-Source Conflict Detection | 2 | 6 | 2026-01-25 | PARTIAL | `s02_d06_exp001/` |
| EXP-002 | Cross-Lingual Retrieval | 3 | 7 | 2026-01-26 | PASS (75%) | `s03_d07_exp002/` |
| EXP-003 | Answer Quality Evaluation | 3 | 8 | (planned) | - | `s03_d08_exp003/` |
| EXP-004 | Chunk Size Optimization | 3 | 9 | (planned) | - | `s03_d09_exp004/` |
| EXP-005 | Retriever Comparison | 3 | 10 | (planned) | - | `s03_d10_exp005/` |

---

## Folder Naming Convention

```
data/experiments/
├── EXPERIMENTS_REGISTRY.md           # This file
├── s{SS}_d{DD}_exp{NNN}/             # Experiment folder
│   ├── README.md                     # Summary + links
│   ├── exp_{NNN}_*.py                # Experiment script
│   ├── exp_{NNN}_results.json        # Results data
│   └── test_data/                    # Optional test files
```

**Pattern:** `s{sprint}_d{day}_exp{id}`

| Component | Format | Example |
|-----------|--------|---------|
| Sprint | `sXX` | `s03` |
| Day | `dXX` | `d07` |
| Experiment | `expNNN` | `exp002` |

**Full example:** `s03_d07_exp002/` = Sprint 3, Day 7, EXP-002

---

## Result Categories

| Result | Meaning |
|--------|---------|
| **PASS** | Capability validated, meets acceptance criteria |
| **PARTIAL** | Capability works with limitations |
| **FAIL** | Capability does not meet requirements |
| **INCONCLUSIVE** | More testing needed |

---

## Quick Links

### Completed Experiments

- [EXP-001: Multi-Source Conflict Detection](s02_d06_exp001/README.md)
- [EXP-002: Cross-Lingual Retrieval](s03_d07_exp002/README.md)

### Full Documentation

- [docs/experiments/](../../docs/experiments/) - Detailed experiment reports

---

## Adding a New Experiment

1. Create folder: `s{SS}_d{DD}_exp{NNN}/`
2. Add `README.md` with summary
3. Add experiment script and results
4. Update this registry table
5. Link to full documentation in `docs/experiments/` if detailed report exists
