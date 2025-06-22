import tiktoken
import search_request

def build_prompt(query, search_results):
    context_template = """
Q: {question}
A: {text}
""".strip()

    # build the context by applying the template to each hit
    contexts = []
    for doc in search_results:
        contexts.append(context_template.format(
            question=doc["question"],
            text=doc["text"]
        ))
    context = "\n\n".join(contexts)

    prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

    prompt = prompt_template.format(question=query, context=context)
    return prompt



if __name__ == "__main__":
    q = "How do copy a file to a Docker container?"
    results = search_request.elastic_search(q)
    prompt = build_prompt(q, results[:3])
    print(len(prompt))

    encoding = tiktoken.encoding_for_model("gpt-4o")

    tokens = encoding.encode(prompt)
    print("Token count:", len(tokens))