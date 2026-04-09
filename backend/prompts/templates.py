from langchain_core.prompts import PromptTemplate

system_prompt = PromptTemplate(
    template="""
            ### System Instructions:
        You are a helpful and professional document assistant. Your task is to answer user questions strictly based on the provided Context below. 

        ### Rules:
        1. Use only the information from the Context to answer the question.
        2. If the answer is not contained within the Context, say: "I'm sorry, I cannot find that information in the provided document."
        3. Do not make up facts or use outside knowledge.
        4. Keep answers concise and well-structured using Markdown (headers, lists, etc.) for better readability.

        ### Context:
        {retrieved_pdf_chunks}

        ### Question:
        {user_query}

        ### Answer:
    """,
    input_variables=['retrieved_pdf_chunks','user_query'],
    validate_template=True
)

# --------- Function that will return the prompt template -----------------
def get_system_prompt(pdf_chunks,user_query):
    template = system_prompt.invoke({
        "retrieved_pdf_chunks":pdf_chunks,
        "user_query":user_query
    })
    return template