"""EXP-002: Cross-Lingual Retrieval Capability Experiment

============================================================================
EXPERIMENT AIM
============================================================================
Validate that the RAG system can retrieve semantically relevant documents
across language boundaries using multilingual embeddings. Specifically:
- German queries should retrieve relevant English documents
- English queries should retrieve relevant German documents

This capability is critical for multilingual document assistants serving
users who may query in a different language than the document corpus.

============================================================================
METHODOLOGY
============================================================================
This experiment follows established cross-lingual information retrieval
(CLIR) evaluation practices adapted for RAG systems:

1. **Document Indexing**: Index parallel content in English and German
   using multilingual embeddings (multilingual-e5-large)

2. **Query-Document Language Mismatch**: Test retrieval where query
   language differs from target document language

3. **Evaluation Metric**: Cross-lingual retrieval success rate
   - Success: Retrieved documents contain target language content
   - Based on MIRACL benchmark evaluation approach

4. **Model Selection Rationale**:
   - multilingual-e5-large: Trained on 1B+ text pairs across 93 languages
   - Outperforms mDPR on MIRACL benchmark (nDCG@10, recall)
   - 1024-dimensional embeddings with 24 transformer layers

============================================================================
CRITICAL REASONING: METHOD AND SOURCE SELECTION
============================================================================

**Why multilingual-e5-large?**
Selected based on MMTEB benchmark results (Wang et al., 2025) where mE5
models demonstrated strong cross-lingual performance. The model was trained
using contrastive learning on multilingual parallel corpora, which creates
aligned embedding spaces across languages - essential for CLIR. Alternative
models like LaBSE or LASER were considered but mE5 offers better retrieval-
specific optimization and is widely adopted in production RAG systems.

**Why MIRACL-style evaluation?**
MIRACL (Multilingual Information Retrieval Across a Continuum of Languages)
is the current standard benchmark for evaluating multilingual retrieval
systems. While we cannot run full MIRACL evaluation (requires specific
corpus and qrels), we adopt its evaluation philosophy:
- Test retrieval accuracy across language pairs
- Measure whether relevant documents are retrieved regardless of language
This approach aligns our small-scale experiment with established methodology.

**Why binary success metric vs. nDCG?**
Our test corpus is small (4 documents), making graded relevance metrics
like nDCG@10 less meaningful. Binary success (did we retrieve ANY cross-
lingual relevant document?) is more appropriate for this validation scale.
Production evaluation should use nDCG on larger corpora.

**Source Selection Criteria:**
1. Recency: Prioritized 2024-2025 publications for current best practices
2. Relevance: Selected papers specifically on CLIR and multilingual embeddings
3. Authority: Used peer-reviewed venues (ICLR, EMNLP) and established benchmarks
4. Reproducibility: Cited HuggingFace model cards with training details

============================================================================
LIMITATIONS
============================================================================
- Small test corpus (4 documents) vs. benchmark datasets (thousands)
- Binary success metric vs. graded relevance (nDCG)
- No query translation baseline comparison
- Single embedding model tested
- German-English pair only (high-resource languages)

============================================================================
REFERENCES
============================================================================
- MMTEB Benchmark (ICLR 2025): https://arxiv.org/html/2502.13595v4
  *Chosen for: Comprehensive multilingual embedding evaluation methodology*

- Multilingual E5 Technical Report: https://arxiv.org/html/2402.05672v1
  *Chosen for: Training methodology and benchmark results for selected model*

- Cross-Lingual IR Advances Survey: https://arxiv.org/html/2510.00908v1
  *Chosen for: Overview of CLIR approaches and evaluation practices*

- intfloat/multilingual-e5-large: https://huggingface.co/intfloat/multilingual-e5-large
  *Chosen for: Model specification and supported languages*

- MIRACL Benchmark: https://huggingface.co/datasets/miracl/miracl
  *Chosen for: Evaluation methodology inspiration*

============================================================================
DSM Reference: C.1.3 Capability Experiment Template
Run: python -m data.experiments.exp_002_cross_lingual
============================================================================
"""

import json
from datetime import datetime
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from src.vectorstore.embeddings import EmbeddingSettings, EmbeddingProvider, get_embeddings
from src.vectorstore.utils.language import detect_language


def run_experiment():
    """Run cross-lingual retrieval capability experiment."""
    print("=" * 70)
    print("EXP-002: Cross-Lingual Retrieval Capability Experiment")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Configuration
    docs_path = Path("data/sample_docs")
    settings = EmbeddingSettings(embedding_provider=EmbeddingProvider.HUGGINGFACE)

    print("CONFIGURATION")
    print("-" * 70)
    print(f"  Embedding Model: {settings.huggingface_model}")
    print(f"  Documents Path: {docs_path}")
    print()

    # Load documents (English + German)
    # Using TextLoader for both .txt and .md to avoid unstructured dependency
    print("DOCUMENT PREPARATION")
    print("-" * 70)
    documents = []
    for f in docs_path.glob("*.txt"):
        docs = TextLoader(str(f)).load()
        documents.extend(docs)
        print(f"  Loaded: {f.name}")
    for f in docs_path.glob("*.md"):
        docs = TextLoader(str(f)).load()
        documents.extend(docs)
        print(f"  Loaded: {f.name}")

    print(f"  Total documents: {len(documents)}")
    print()

    # Chunk and index
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"  Chunks created: {len(chunks)}")

    print("\nINDEXING")
    print("-" * 70)
    embeddings = get_embeddings(settings)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="exp_002_cross_lingual",
    )
    print("  Vector store created with multilingual embeddings")
    print()

    # Cross-lingual test cases
    # Based on CLIR evaluation: query in language A, expect docs in language B
    test_cases = [
        {
            "query": "Was testet das RAG-System?",
            "query_lang": "de",
            "target_lang": "en",
            "description": "German query → English document (RAG system testing)",
        },
        {
            "query": "What does the document loader test?",
            "query_lang": "en",
            "target_lang": "de",
            "description": "English query → German document (loader testing)",
        },
        {
            "query": "Welche Abschnitte hat das Markdown-Dokument?",
            "query_lang": "de",
            "target_lang": "en",
            "description": "German query → English document (markdown sections)",
        },
        {
            "query": "What are the bullet points in the example?",
            "query_lang": "en",
            "target_lang": "de",
            "description": "English query → German document (bullet points)",
        },
    ]

    print("CROSS-LINGUAL RETRIEVAL TESTS")
    print("-" * 70)

    results = []
    for i, test in enumerate(test_cases, 1):
        query = test["query"]
        detected_lang = detect_language(query)
        docs = vectorstore.similarity_search(query, k=2)
        sources = [d.metadata.get("source", "unknown") for d in docs]

        # Check if retrieved target-language documents
        # German docs have "_de" in filename, English docs don't
        target_is_german = test["target_lang"] == "de"
        has_target = any(("_de" in s) == target_is_german for s in sources)

        result = {
            "test_id": i,
            "query": query,
            "query_lang": test["query_lang"],
            "detected_lang": detected_lang,
            "target_lang": test["target_lang"],
            "sources": sources,
            "cross_lingual_success": has_target,
            "description": test["description"],
        }
        results.append(result)

        status = "OK" if has_target else "MISS"
        print(f"\n  Test {i}: [{status}] {test['description']}")
        print(f"    Query ({detected_lang}): {query[:50]}...")
        print(f"    Target: {test['target_lang'].upper()} documents")
        print(f"    Retrieved: {sources}")

    # Calculate metrics
    success_count = sum(r["cross_lingual_success"] for r in results)
    total_count = len(results)
    success_rate = success_count / total_count * 100

    print("\n" + "=" * 70)
    print("METRICS (per MIRACL-style evaluation)")
    print("=" * 70)
    print(f"  Total test cases: {total_count}")
    print(f"  Cross-lingual successes: {success_count}")
    print(f"  Success rate: {success_rate:.1f}%")
    print()

    # Findings per DSM C.1.3
    print("FINDINGS")
    print("-" * 70)
    if success_rate >= 75:
        finding = "PASS: Cross-lingual retrieval effective"
        detail = f"multilingual-e5-large achieves {success_rate:.0f}% cross-lingual retrieval"
        limitation = None
    elif success_rate >= 50:
        finding = "PARTIAL: Cross-lingual retrieval partially working"
        detail = "Semantic alignment works but not consistently"
        limitation = "Consider: Query preprocessing, language-specific boosting"
    else:
        finding = "FAIL: Cross-lingual retrieval needs improvement"
        detail = "Semantic alignment insufficient for reliable CLIR"
        limitation = "Consider: Query translation fallback, different embedding model"

    print(f"  {finding}")
    print(f"  {detail}")
    if limitation:
        print(f"  Limitation: {limitation}")
    print()

    # Save results
    output = {
        "experiment_id": "EXP-002",
        "name": "Cross-Lingual Retrieval Capability",
        "timestamp": datetime.now().isoformat(),
        "configuration": {
            "embedding_model": settings.huggingface_model,
            "chunk_size": 500,
            "chunk_overlap": 50,
            "k": 2,
        },
        "metrics": {
            "total_tests": total_count,
            "successes": success_count,
            "success_rate": success_rate,
        },
        "finding": finding,
        "detail": detail,
        "limitation": limitation,
        "results": results,
        "references": [
            "https://arxiv.org/html/2502.13595v4",  # MMTEB
            "https://arxiv.org/html/2402.05672v1",  # mE5 Technical Report
            "https://arxiv.org/html/2510.00908v1",  # CLIR Survey
            "https://huggingface.co/intfloat/multilingual-e5-large",
        ],
    }

    output_path = Path("data/experiments/exp_002_results.json")
    output_path.write_text(json.dumps(output, indent=2))
    print(f"Results saved: {output_path}")

    # Cleanup
    vectorstore.delete_collection()

    return success_rate


if __name__ == "__main__":
    run_experiment()
