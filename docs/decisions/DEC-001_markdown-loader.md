# DEC-001: Use TextLoader for Markdown Files

**Date:** 2026-01-18
**Category:** Library Choice
**Status:** Accepted

---

## Context

Need to load markdown files as part of the document ingestion pipeline. LangChain provides `UnstructuredMarkdownLoader` for this purpose.

## Decision

Use `TextLoader` instead of `UnstructuredMarkdownLoader` for markdown files.

## Alternatives Considered

1. **UnstructuredMarkdownLoader** - Rejected
   - Requires `unstructured` package (~500MB+ with dependencies)
   - Adds complexity for minimal benefit
   - Markdown is plain text; advanced parsing not needed for RAG

2. **TextLoader** - Selected
   - No extra dependencies
   - Markdown content preserved as-is
   - Sufficient for chunking and embedding

3. **Custom loader with markdown parsing** - Rejected
   - Over-engineering for current requirements
   - Could add later if structure extraction needed

## Rationale

For RAG applications, we chunk and embed the text content. Markdown formatting (headers, lists, links) is preserved as text, which is sufficient for semantic search. The `unstructured` package would add significant installation overhead without meaningful benefit.

## Implications

- Markdown structure (headers, sections) not parsed into separate elements
- If future requirements need markdown structure awareness (e.g., section-based retrieval), revisit this decision
- Keeps dependencies lightweight and installation fast

## Related

- `src/ingestion/loaders.py`: `load_markdown()` function
- `tests/test_ingestion.py`: `TestMarkdownLoader` class
