import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("GROQ_MODEL"),
    temperature=0,
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant for a PDF chatbot.

Rules:
- Answer ONLY using the provided document context.
- Do not invent information.
- If the answer is not present in the context, say:
  "I couldn't find that information in the uploaded document."
- Never mention chunk numbers or internal retrieval.
- Explain concepts clearly and naturally.
- Use bullet points whenever appropriate.
""",
        ),
        (
            "human",
            """
Context:
{context}

User Question:
{question}
""",
        ),
    ]
)


def generate_response_from_llm(top_chunks, user_query):

    if isinstance(top_chunks, list):
        context = "\n\n".join(
    chunk["chunks"] for chunk in top_chunks
)
    else:
        context = str(top_chunks)

    prompt = prompt_template.format_messages(
        context=context,
        question=user_query,
    )

    response = llm.invoke(prompt)

    return response.content