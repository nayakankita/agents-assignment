from .router_graph import build_graph

def main():
    app = build_graph()

    print("Multi-Agent App (RAG + Coding)")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Question> ").strip()
        if question.lower() in {"exit", "quit"}:
            break

        result = app.invoke({"question": question, "route": "rag", "answer": ""})
        print("\n" + result["answer"] + "\n")

if __name__ == "__main__":
    main()
