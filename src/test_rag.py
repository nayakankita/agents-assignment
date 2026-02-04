from .rag_agent import get_rag_answer

if __name__ == "__main__":
    q = "What is the process for approval to request time off?"
    print(get_rag_answer(q))

