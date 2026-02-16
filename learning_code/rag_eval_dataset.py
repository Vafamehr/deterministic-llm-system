# This is your ground truth set.NEw

EVAL_SET = [
    {
        "question": "What is the deadline?",
        "expected_source": "contract_a",
        "expected_fact": "30 days"
    },
    {
        "question": "Who is responsible for payment?",
        "expected_source": "contract_a",
        "expected_fact": "buyer"
    }
]

EVAL_SET = [
    {
        "question": "What is the deadline?",
        "expected_source": "contract_a",
        "expected_facts": ["30 days", "written notice"]
    }
]



def evaluate_response(question, retrieved_source, answer_text, expected):


    q = question.lower()
    a = answer_text.lower()

    if "deadline" in q:
        relevance_ok = ("deadline" in a) or ("days" in a)
    elif "payment" in q:
        relevance_ok = ("payment" in a) or ("buyer" in a) or ("seller" in a)
    else:
        relevance_ok = True


    expected_facts = expected["expected_facts"]

    facts_found = [
        fact for fact in expected_facts
        if fact.lower() in answer_text.lower()
    ]

    completeness_ok = len(facts_found) == len(expected_facts)
    




    results = {
    "retrieval_correct": retrieved_source == expected["expected_source"],
    "fact_present": len(facts_found) > 0,
    "relevance_ok": relevance_ok,
    "completeness_ok": completeness_ok
    }

    results["overall"] = all(results.values())

    results["overall"] = all(results.values())

    return results



if __name__ == "__main__":
    sample_question = EVAL_SET[0]
    

    # pretend this came from your RAG pipeline
    retrieved_source = "contract_a"
    # answer = "The filing deadline is 30 days from execution."
    # answer = "This contract was signed in 2019."
    answer = "The deadline is 30 days."


    score = evaluate_response(
        sample_question["question"],
        retrieved_source,
        answer,
        sample_question
    )

    print(score)
