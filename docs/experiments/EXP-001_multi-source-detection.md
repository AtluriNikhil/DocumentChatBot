# EXP-001: Multi-Source Conflict Detection

**Date:** 2026-01-25
**Status:** Completed

---

## Objective

Test whether the RAG system can identify and cite different sources when documents contain conflicting information.

## Setup

**Test Files:**
- `policy_2023.md` - Refund period: 30 days, Return shipping: Customer pays
- `policy_2024.md` - Refund period: 60 days, Return shipping: Free

**Configuration:**
- LLM Provider: OpenAI (gpt-4o-mini)
- Retrieval: Top-4 chunks
- Embeddings: text-embedding-ada-002

## Results

### Query 1: "What is the refund period?"

**Answer:**
> "The refund period is **60 days** from the date of purchase (Source: Document 1)."

**Observation:** Only cited one source (2024), even though both documents were retrieved. The LLM chose the more recent/prominent one without mentioning the conflict.

**Sources Retrieved:** Both policy_2023.md and policy_2024.md

---

### Query 2: "What are the different refund periods mentioned in the documents?"

**Answer:**
> "The refund periods mentioned in the documents are:
> - **60 days** for the year 2024 (Document 1).
> - **30 days** for the year 2023 (Document 2)."

**Observation:** When explicitly asked about differences, the LLM correctly identified both sources and their respective values.

---

### Query 3: "Who pays for return shipping?"

**Answer:**
> "According to the Company Policy 2024, return shipping is now free for all customers (Document 1). In contrast, the Company Policy 2023 states that return shipping costs are the responsibility of the customer (Document 2)."

**Observation:** The LLM proactively identified the conflict and cited both sources with their different policies.

---

## Findings

| Scenario | Multi-Source Detection | Conflict Identification |
|----------|------------------------|------------------------|
| Simple question | Partial - retrieved both, cited one | No |
| Explicit "differences" query | Yes | Yes |
| Question with implicit conflict | Yes | Yes |

## Conclusions

1. **Retrieval works correctly** - Both conflicting sources are retrieved
2. **Citation is inconsistent** - Simple questions may only cite one source
3. **Conflict detection depends on query phrasing** - Explicit questions get better results
4. **LLM reasoning helps** - When context implies conflict, the LLM identifies it

## Limitations Identified

| Limitation | Impact |
|------------|--------|
| Single-answer queries may miss conflicts | User gets incomplete info |
| No automatic version/date awareness | Can't prioritize newer docs |
| Relies on LLM reasoning | Inconsistent behavior |
| Unnamed docs harder to distinguish | Poor source attribution |

## Recommended User Guidance (Current MVP)

To get comprehensive answers when multiple sources exist:
- Ask "What do all documents say about X?"
- Ask "Are there different answers for X?"
- Ask "Compare the sources on X"

---

## Future Improvements (v2.0)

If an improved version of this application is developed, the following enhancements would address the identified limitations:

### 1. Enhanced Prompt for Conflict Detection

**Action:** Modify `src/llm/prompts.py` to include conflict detection instructions:
```
"If the retrieved sources contain different or conflicting answers to the question,
explicitly list ALL variations and cite which document each comes from."
```

**Expected Outcome:**
- Simple queries like "What is the refund period?" would return: "Document A says 30 days, Document B says 60 days"
- Users would always see the full picture without needing to phrase questions specially

---

### 2. Document Date Metadata

**Action:**
- Add `document_date` field during ingestion (extracted from filename, content, or user input)
- Modify prompt to include: "When sources conflict, prioritize the most recent document"

**Expected Outcome:**
- System would automatically prefer `policy_2024.md` over `policy_2023.md`
- Answer: "The current refund period is 60 days (policy_2024). Note: An older policy (2023) stated 30 days."

---

### 3. Semantic Conflict Detection (Pre-LLM)

**Action:**
- After retrieval, compare chunk embeddings to detect high similarity with different content
- Flag potential conflicts before sending to LLM
- Add conflict indicator to prompt context

**Expected Outcome:**
- Faster conflict detection without relying on LLM reasoning
- Consistent behavior regardless of query phrasing
- Could warn users: "Multiple sources found with different information"

---

### 4. Document Title Extraction

**Action:**
- Parse first heading (# Title) from markdown/text during ingestion
- Store as `document_title` in metadata
- Display friendly names instead of file paths

**Expected Outcome:**
- Sources show as "Company Policy 2023" instead of "data/temp_uploads/policy_2023.md"
- Better user experience and clearer attribution

---

### 5. Source Comparison View

**Action:**
- Add UI toggle to show side-by-side comparison of retrieved sources
- Highlight conflicting sections automatically

**Expected Outcome:**
- Users can visually compare sources
- Increases transparency about what the LLM "sees"
- Helps users make informed decisions when sources disagree

---

## Test Files Location

```
data/experiments/
├── policy_2023.md
└── policy_2024.md
```
