"""Prompt templates for RAG system."""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# System prompt for RAG with source attribution
RAG_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the provided context.

Instructions:
1. Answer the question using ONLY the information from the context below.
2. If the context doesn't contain enough information to answer, say "I don't have enough information to answer this question."
3. Always cite your sources by referencing the document names when possible.
4. Be concise and direct in your answers.

Context:
{context}"""

# Basic RAG prompt (no chat history)
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT),
    ("human", "{question}"),
])

# RAG prompt with conversation history
RAG_CHAT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# Standalone question prompt (for reformulating with history)
CONDENSE_QUESTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question that captures all necessary context.

Chat History:
{chat_history}

Follow-up Question: {question}

Standalone Question:"""),
])


def format_documents(documents: list) -> str:
    """Format documents for inclusion in prompt context.
    
    Args:
        documents: List of Document objects.
        
    Returns:
        Formatted string with document contents and sources.
    """
    formatted = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "Unknown")
        content = doc.page_content.strip()
        formatted.append(f"[Document {i}] (Source: {source})\n{content}")
    
    return "\n\n---\n\n".join(formatted)

# German system prompt for RAG
RAG_SYSTEM_PROMPT_DE = """Du bist ein hilfreicher Assistent, der Fragen basierend auf dem bereitgestellten Kontext beantwortet.

Anweisungen:
1. Beantworte die Frage NUR mit Informationen aus dem untenstehenden Kontext.
2. Wenn der Kontext nicht genügend Informationen enthält, sage "Ich habe nicht genügend Informationen, um diese Frage zu beantworten."
3. Zitiere immer deine Quellen, indem du die Dokumentnamen referenzierst, wenn möglich.
4. Sei prägnant und direkt in deinen Antworten.

Kontext:
{context}"""

# German RAG prompts
RAG_PROMPT_DE = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT_DE),
    ("human", "{question}"),
])

RAG_CHAT_PROMPT_DE = ChatPromptTemplate.from_messages([
    ("system", RAG_SYSTEM_PROMPT_DE),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

CONDENSE_QUESTION_PROMPT_DE = ChatPromptTemplate.from_messages([
    ("system", """Angesichts der folgenden Konversation und einer Folgefrage, formuliere die Folgefrage zu einer eigenständigen Frage um, die den gesamten notwendigen Kontext erfasst.

Chat-Verlauf:
{chat_history}

Folgefrage: {question}

Eigenständige Frage:"""),
])


def get_prompts(language: str = "en") -> dict:
    """Get prompts for the specified language.
    
    Args:
        language: Language code ("en" or "de").
        
    Returns:
        Dictionary with prompt templates.
    """
    if language == "de":
        return {
            "system": RAG_SYSTEM_PROMPT_DE,
            "rag": RAG_PROMPT_DE,
            "chat": RAG_CHAT_PROMPT_DE,
            "condense": CONDENSE_QUESTION_PROMPT_DE,
        }
    
    return {
        "system": RAG_SYSTEM_PROMPT,
        "rag": RAG_PROMPT,
        "chat": RAG_CHAT_PROMPT,
        "condense": CONDENSE_QUESTION_PROMPT,
    }
