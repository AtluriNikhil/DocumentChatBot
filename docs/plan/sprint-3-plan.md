# Sprint 3: Experiments & Optimization

**Duration:** Days 7-10
**Start Date:** 2026-01-26
**Status:** Planning
**DSM Version:** 1.3.1

---

## Sprint Philosophy

Sprint 3 follows an **experiment-driven development** approach based on DSM v1.3.1 Appendix C extensions:

| DSM Section | Purpose | Usage in Sprint 3 |
|-------------|---------|-------------------|
| **C.1.3** Capability Experiment Template | Combined quant + qual evaluation | All experiments (EXP-002 to EXP-005) |
| **C.1.4** RAG Evaluation Metrics Reference | RAGAS, RAGBench, TRACe metrics | Day 8 retrieval comparison |
| **C.1.5** Limitation Discovery Protocol | Disposition matrix, severity guidance | All experiments |

Each day includes:
1. **Implementation** - Build or enhance a feature
2. **Capability Experiment** - Validate using C.1.3 template (internal + external metrics)
3. **Limitation Discovery** - Document per C.1.5 protocol (Fix Now / Accept MVP / Defer)
4. **Documentation** - Record findings with quantitative targets for future improvements
5. **DSM Validation** - Log feedback on methodology effectiveness in [dsm-validation-tracker.md](../dsm-validation-tracker.md)

---

## Day 7: German Language Support

### Implementation Tasks

| Task | Description |
|------|-------------|
| Multilingual embeddings | Add HuggingFace `multilingual-e5-large` as embedding option |
| German prompt templates | Create German system prompts and response formatting |
| Language detection | Auto-detect query language and select appropriate prompts |
| German test documents | Prepare technical/regulatory documents in German |

### Experiment: EXP-002 Cross-Lingual Retrieval

**Objective:** Test whether the system can retrieve relevant documents across languages.

**Test Cases (per C.1.3 Template):**

| Test Case | Expected | Status |
|-----------|----------|--------|
| German query → German docs | Relevant chunks retrieved | Pending |
| German query → English docs | Relevant chunks retrieved (cross-lingual) | Pending |
| English query → German docs | Relevant chunks retrieved (cross-lingual) | Pending |
| Mixed-language query | Best matching language docs retrieved | Pending |

**Metrics (per C.1.4):**

| Category | Metric | Baseline (English) | German |
|----------|--------|-------------------|--------|
| **Internal** | context_precision | ? | ? |
| **Internal** | faithfulness | ? | ? |
| **Qualitative** | Pass/Fail/Partial | N/A | Per test case |

**Limitation Discovery (per C.1.5):**
- Document any cross-lingual retrieval failures
- Disposition: Fix Now / Accept MVP / Defer with severity rating

### Deliverables

- [ ] Multilingual embedding support
- [ ] German prompt templates
- [ ] EXP-002 experiment documentation
- [ ] Day 7 checkpoint

---

## Day 8: Hybrid Search

### Implementation Tasks

| Task | Description |
|------|-------------|
| BM25 retriever | Add keyword-based retrieval using rank_bm25 |
| Retrieval fusion | Combine semantic + BM25 results (reciprocal rank fusion) |
| Configuration | Allow switching between semantic-only, BM25-only, hybrid |
| API update | Add retrieval_mode parameter to query endpoint |

### Experiment: EXP-003 Retrieval Strategy Comparison

**Objective:** Compare retrieval quality across different strategies.

**Test Cases (per C.1.3 Template):**

| Test Case | Semantic | BM25 | Hybrid | Notes |
|-----------|----------|------|--------|-------|
| Exact keyword match | ? | ? | ? | e.g., "error code 404" |
| Semantic similarity | ? | ? | ? | e.g., "application crashed" vs "program stopped working" |
| Technical acronyms | ? | ? | ? | e.g., "RAG" vs "retrieval augmented generation" |
| Multi-concept query | ? | ? | ? | e.g., "German documents about authentication" |

**Metrics (per C.1.4 RAG Evaluation Reference):**

| Category | Metric | Source |
|----------|--------|--------|
| **Internal - Traditional** | Precision@K, Recall@K | Manual |
| **Internal - LLM-based** | context_precision, context_recall | RAGAS |
| **Internal - TRACe** | Context Relevance, Completeness | RAGBench |
| **Qualitative** | Which strategy found most relevant docs | Manual |

**Limitation Discovery (per C.1.5):**
- Document any retrieval failures with disposition (Fix Now / Accept MVP / Defer)

### Deliverables

- [ ] BM25 retriever implementation
- [ ] Hybrid search with fusion
- [ ] EXP-003 experiment documentation
- [ ] Day 8 checkpoint

---

## Day 9: Performance & Robustness

### Implementation Tasks

| Task | Description |
|------|-------------|
| Response caching | Cache repeated queries (LRU cache or Redis) |
| Token tracking | Log token usage per request (input/output/embedding) |
| Cost calculation | Estimate cost per query based on token usage |
| Structured logging | JSON format logs for production monitoring |

### Experiment: EXP-004 Performance & Robustness Testing

**Objective:** Measure system performance and robustness under various conditions.

**Part A: Latency Benchmarks (per C.1.3 Template)**

| Test Case | Baseline | With Cache | Notes |
|-----------|----------|------------|-------|
| Cold query (first time) | ? ms | N/A | Establish baseline |
| Warm query (repeated) | ? ms | ? ms | Cache effectiveness |
| Large document (10k tokens) | ? ms | ? ms | Chunking impact |
| Multiple retrievals (k=10) | ? ms | ? ms | Retrieval scaling |

**Part B: Robustness Testing (per C.1.4 External Metrics)**

| Test Case | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Typo in query ("refund polcy") | Graceful handling | ? | Pending |
| Empty query | Error message | ? | Pending |
| Very long query (500+ words) | Truncation or handling | ? | Pending |
| Special characters in query | No injection | ? | Pending |
| Query with no relevant docs | "No information" response | ? | Pending |

**Metrics (per C.1.4):**

| Category | Metric | Target |
|----------|--------|--------|
| **Efficiency** | p50, p95, p99 latency | p95 < 3s |
| **Efficiency** | Cost per query | < $0.05 |
| **Robustness** | Error handling rate | 100% graceful |
| **Robustness** | Adversarial query handling | No crashes |

**Limitation Discovery (per C.1.5):**
- Document performance bottlenecks with severity and disposition

### Deliverables

- [ ] Query caching implementation
- [ ] Token usage tracking
- [ ] EXP-004 benchmark documentation
- [ ] Day 9 checkpoint

---

## Day 10: Deployment & Documentation

### Implementation Tasks

| Task | Description |
|------|-------------|
| Dockerfile | Multi-stage build for API and UI |
| docker-compose | Full stack deployment (API + Streamlit + ChromaDB) |
| Architecture diagram | Visual system overview |
| API documentation | OpenAPI spec + usage examples |
| Demo preparation | Sample documents + walkthrough script |

### Experiment: EXP-005 End-to-End System Validation

**Objective:** Validate complete system functionality before deployment.

**Test Cases (per C.1.3 Template):**

| Test Case | Expected | Status |
|-----------|----------|--------|
| Fresh deployment (docker-compose up) | All services healthy | Pending |
| Document upload via UI | Chunks indexed correctly | Pending |
| Query with citations | Answer + sources returned | Pending |
| Provider switching | All 3 providers respond | Pending |
| Clear documents | Database emptied | Pending |
| Error handling | Graceful failures, informative messages | Pending |

**Sprint 3 Limitation Summary (per C.1.5):**

| Limitation | Severity | Disposition | Future Target |
|------------|----------|-------------|---------------|
| (To be filled from EXP-002 to EXP-005) | | | |

### Deliverables

- [ ] Docker configuration
- [ ] Architecture diagram
- [ ] EXP-005 validation documentation
- [ ] Sprint 3 limitation summary (C.1.5 format)
- [ ] Sprint 3 checkpoint

---

## Sprint 3 Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| German retrieval works | Pass EXP-002 | Qualitative |
| Hybrid search improves precision | >10% improvement | context_precision |
| Query latency (cached) | <500ms p95 | EXP-004 benchmarks |
| Docker deployment | All services up | EXP-005 validation |
| Experiments documented | 4 experiments (EXP-002 to EXP-005) | Count |

---

## Experiment Tracking Summary

| Experiment | Day | Focus | DSM Template | Metrics Source |
|------------|-----|-------|--------------|----------------|
| EXP-001 | Day 6 | Multi-source conflict detection | C.1.3 ✓ | Qualitative |
| EXP-002 | Day 7 | Cross-lingual retrieval | C.1.3 | RAGAS + Qualitative |
| EXP-003 | Day 8 | Retrieval strategy comparison | C.1.3 | RAGAS + RAGBench TRACe |
| EXP-004 | Day 9 | Performance & robustness | C.1.3 | Efficiency + Robustness |
| EXP-005 | Day 10 | End-to-end validation | C.1.3 | System validation |

---

## DSM Validation Tracking

This sprint validates DSM v1.3.1 methodology. Feedback is logged in [dsm-validation-tracker.md](../dsm-validation-tracker.md).

**Sections Under Validation:**

| DSM Section | Day Used | Validation Focus |
|-------------|----------|------------------|
| C.1.3 Capability Experiment Template | 7-10 | Does combined quant+qual work for RAG? |
| C.1.4 RAG Evaluation Metrics | 8 | Are RAGAS/RAGBench references sufficient? |
| C.1.5 Limitation Discovery Protocol | 7-10 | Is disposition matrix practical? |
| 4.0 Software Engineering Adaptation | All | Does app dev protocol fit RAG projects? |

**Expected Feedback Items:**
- [ ] FEEDBACK-002: C.1.3 template clarity and completeness (Day 7)
- [ ] FEEDBACK-003: C.1.4 RAG metrics applicability (Day 8)
- [ ] FEEDBACK-004: C.1.5 limitation protocol efficiency (Day 9)
- [ ] FEEDBACK-005: Sprint 3 overall methodology assessment (Day 10)

---

## DSM References

**Methodology Sections (v1.3.1):**
- C.1.3: Capability Experiment Template - Combined quant + qual framework
- C.1.4: RAG Evaluation Metrics Reference - RAGAS, RAGBench, TRACe, SafeRAG
- C.1.5: Limitation Discovery Protocol - Disposition matrix, severity guidance

**External References:**
- [RAGAS Documentation](https://docs.ragas.io/en/stable/concepts/metrics/overview/)
- [RAGBench Paper](https://arxiv.org/abs/2504.14891) - TRACe metrics
- [EXP-001: Multi-Source Conflict Detection](../experiments/EXP-001_multi-source-detection.md)
- [DSM Validation Tracker](../dsm-validation-tracker.md)
