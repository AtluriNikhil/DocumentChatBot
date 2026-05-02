# DSM Validation Tracker

**Purpose:** Track DSM v1.3.1 methodology usage during RAG Document Assistant development to provide critical feedback for methodology improvement.

**Project:** RAG Document Assistant
**DSM Version:** 1.3.1
**Tracking Period:** 2026-01-17 to present

---

## Validation Approach

Each DSM section used is evaluated on:

| Criterion | Description | Scale |
|-----------|-------------|-------|
| **Clarity** | Was the guidance clear and unambiguous? | 1-5 |
| **Applicability** | Did it fit this project's context? | 1-5 |
| **Completeness** | Was anything missing that we needed? | 1-5 |
| **Efficiency** | Did it save time vs. ad-hoc approach? | 1-5 |

**Overall Score:** Average of 4 criteria (max 5.0)

---

## DSM Sections Used

### Sprint 1-2: Core Development

| DSM Section | Used In | Score | Notes |
|-------------|---------|-------|-------|
| **4.0 Software Engineering Adaptation** | Sprint 1-2 | TBD | App development protocol |
| **2.0 PM Guidelines** | Sprint planning | TBD | Sprint structure |
| **C.1 Experiment Tracking** | Day 5 MLflow | TBD | Numeric metrics |

### Sprint 3: Experiment-Driven Development

| DSM Section | Used In | Score | Notes |
|-------------|---------|-------|-------|
| **C.1.3 Capability Experiment Template** | EXP-001 to EXP-005 | TBD | Combined quant + qual |
| **C.1.4 RAG Evaluation Metrics Reference** | Day 8 | TBD | RAGAS, RAGBench |
| **C.1.5 Limitation Discovery Protocol** | All experiments | TBD | Disposition matrix |

---

## Feedback Log

### FEEDBACK-001: Gap in Capability Experiment Documentation

**Date:** 2026-01-25
**DSM Section:** C.1 Experiment Tracking
**Sprint/Day:** Day 6 (EXP-001)
**Type:** Gap Identified

**Context:**
Conducted EXP-001 (multi-source conflict detection) - a qualitative capability experiment.

**Issue:**
DSM C.1 was designed for ML experiments with numeric metrics (accuracy, F1, loss). No template existed for:
- Qualitative pass/fail/partial results
- Behavioral observations
- Limitation discovery and disposition

**Resolution:**
Created BACKLOG-001, which was implemented as DSM v1.3.1 sections C.1.3, C.1.4, C.1.5.

**Evaluation:**

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Clarity | 4 | Original C.1 was clear for ML, but didn't indicate it was ML-specific |
| Applicability | 2 | Did not apply to software/RAG capability experiments |
| Completeness | 2 | Missing qualitative template, RAG metrics, limitation protocol |
| Efficiency | 3 | Had to create ad-hoc format, then formalize as BACKLOG-001 |

**Overall Score:** 2.75/5.0

**Recommendation:**
- C.1 should explicitly state it's for numeric ML experiments
- Cross-reference to C.1.3 for capability experiments should be prominent
- Consider adding "Experiment Type Decision Tree" to help users select correct template

---

### FEEDBACK-002: Tests vs Experiments Differentiation

**Date:** 2026-01-26
**DSM Section:** C.1.3 Capability Experiment Template
**Sprint/Day:** Sprint 3, Day 7
**Type:** Gap Identified

**Context:**
Implementing German language support required both pytest unit tests (for function correctness) and a capability experiment (EXP-002: Cross-Lingual Retrieval). Initially unclear which validation approach should be used where.

**Issue:**
DSM C.1.3 Capability Experiment Template does not differentiate between:
- **pytest tests**: Validate function correctness (unit/integration level)
- **Capability experiments**: Validate end-to-end feature capability

This caused initial confusion and risk of redundant validation (tests duplicating experiments).

**Resolution:**
Created BACKLOG-008 proposing explicit guidance:
- Tests: `tests/` folder, run on every commit, pass/fail assertions
- Experiments: `data/experiments/`, run at milestones, produce metrics/findings
- Location: `D:\data-science\agentic-ai-data-science-methodology\plan\backlog\BACKLOG-008_experiments-vs-tests-clarification.md`

**Evaluation:**

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Clarity | 4 | C.1.3 template itself is clear |
| Applicability | 3 | Template works but doesn't say when NOT to use it |
| Completeness | 2 | Missing guidance on tests vs experiments distinction |
| Efficiency | 3 | Some time lost deciding where validation code belongs |

**Overall Score:** 3.0/5.0

**Recommendation:**
- Add "Scope" section to C.1.3 clarifying when to use experiments vs tests
- Consider adding decision table: "Function correctness? → pytest. Feature capability? → Experiment"
- Reference pytest/TDD best practices in DSM 4.0 Section 8

---

### FEEDBACK-003: C.1.3 Capability Template Success

**Date:** 2026-01-26
**DSM Section:** C.1.3 Capability Experiment Template
**Sprint/Day:** Sprint 3, Day 7 (EXP-002)
**Type:** Success

**Context:**
Used C.1.3 template to design and execute EXP-002 Cross-Lingual Retrieval experiment.

**Success:**
The template provided excellent structure for:
- Defining experiment aim and methodology
- Documenting critical reasoning for method selection
- Referencing academic sources (MMTEB, MIRACL, mE5 Technical Report)
- Recording metrics and findings
- Identifying limitations

**Evaluation:**

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Clarity | 5 | Template structure was unambiguous |
| Applicability | 5 | Perfect fit for RAG capability experiment |
| Completeness | 4 | Only missing tests vs experiments guidance |
| Efficiency | 5 | Saved significant time vs ad-hoc approach |

**Overall Score:** 4.75/5.0

**Recommendation:**
- Template works excellently; no changes needed to core structure
- Just needs the scoping clarification mentioned in FEEDBACK-002

---

### FEEDBACK-004: Experiment Artifact Organization Gap

**Date:** 2026-01-26
**DSM Section:** C.1.3 Capability Experiment Template
**Sprint/Day:** Sprint 3, Day 7
**Type:** Gap Identified

**Context:**
After conducting EXP-001 and EXP-002, experiment artifacts (scripts, results, test data) accumulated in a flat `data/experiments/` folder. No guidance in DSM on how to organize these artifacts.

**Issue:**
DSM C.1.3 provides excellent experiment execution guidance but lacks artifact organization standards:
- No folder naming convention
- No central registry/index
- No README template for experiment folders
- Relationship between `data/experiments/` and `docs/experiments/` unclear

**Resolution:**
1. Implemented sprint/day folder organization: `s03_d07_exp002/`
2. Created EXPERIMENTS_REGISTRY.md as central index
3. Added README.md to each experiment folder
4. Created BACKLOG-009 proposing C.1.6 Experiment Artifact Organization

**Evaluation:**

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Clarity | 4 | C.1.3 template is clear for execution |
| Applicability | 4 | Template applies well to experiments |
| Completeness | 2 | Missing artifact organization guidance |
| Efficiency | 3 | Had to create organization ad-hoc |

**Overall Score:** 3.25/5.0

**Recommendation:**
- Add C.1.6 Experiment Artifact Organization section
- Include folder naming convention aligned with `sYY_dXX` pattern
- Provide EXPERIMENTS_REGISTRY.md template
- Clarify data/experiments vs docs/experiments relationship

---

### FEEDBACK-005: (Template for future feedback)

**Date:**
**DSM Section:**
**Sprint/Day:**
**Type:** Gap / Success / Improvement / Pain Point

**Context:**

**Issue/Success:**

**Resolution (if applicable):**

**Evaluation:**

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Clarity | | |
| Applicability | | |
| Completeness | | |
| Efficiency | | |

**Overall Score:** /5.0

**Recommendation:**

---

## Summary Metrics

### By DSM Section

| Section | Times Used | Avg Score | Top Issue |
|---------|------------|-----------|-----------|
| C.1 Experiment Tracking | 1 | 2.75 | Not applicable to capability experiments |
| C.1.3 Capability Template | 3 | 3.67 | Missing artifact organization (C.1.6 needed) |
| C.1.4 RAG Metrics Reference | 0 | - | (Sprint 3 Day 8) |
| C.1.5 Limitation Protocol | 0 | - | (Sprint 3) |
| 4.0 Software Engineering | TBD | - | - |

### By Feedback Type

| Type | Count | Sections Affected |
|------|-------|-------------------|
| Gap Identified | 3 | C.1, C.1.3 (tests vs experiments, artifact org) |
| Success | 1 | C.1.3 |
| Improvement Suggestion | 0 | - |
| Pain Point | 0 | - |

---

## Recommendations for DSM

### High Priority

1. **Add Experiment Type Decision Tree**
   - Help users choose between C.1 (numeric ML) vs C.1.3 (capability)
   - Location: Beginning of Appendix C.1

2. **Add Checkpoint and Feedback Protocol** (BACKLOG-006)
   - Formalize validation tracker approach in DSM
   - Add Section 6.3: Checkpoint and Feedback Protocol
   - Add Appendix E.12: Validation Tracker Template
   - See: `D:\data-science\agentic-ai-data-science-methodology\plan\backlog\BACKLOG-006_checkpoint-feedback-protocol.md`

### Medium Priority

(To be populated as Sprint 3 progresses)

### Low Priority

(To be populated as Sprint 3 progresses)

---

## Version History

| Date | Update |
|------|--------|
| 2026-01-26 | Created tracker, added FEEDBACK-001 |
| 2026-01-26 | Created BACKLOG-006 for checkpoint/feedback protocol |
| 2026-01-26 | Added FEEDBACK-002 (tests vs experiments gap), FEEDBACK-003 (C.1.3 success) |
| 2026-01-26 | Created BACKLOG-008 for experiments vs tests clarification |
| 2026-01-26 | Added FEEDBACK-004 (experiment artifact organization gap) |
| 2026-01-26 | Created BACKLOG-009 for experiment folder organization standard |
