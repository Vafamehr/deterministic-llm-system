from tools.retrieval import RetrievalQuery, execute_retrieval

if __name__ == "__main__":
    q = RetrievalQuery(query="commit boundary trace", top_k=5, namespace="default")
    res = execute_retrieval(q)

    print("\nSOURCES:")
    for s in res.sources:
        print(" -", s)

    print("\nCHUNKS:")
    for i, c in enumerate(res.chunks, 1):
        preview = c.text.replace("\n", " ")[:200]
        print(f"\n{i}) id={c.chunk_id} score={c.score} source={c.source}")
        print("   ", preview)