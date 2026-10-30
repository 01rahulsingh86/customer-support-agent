from llm_judge import semantic_correctness

from dotenv import load_dotenv
from langsmith import Client

from agent import ask_agent

load_dotenv()

client = Client()


# STEP A: Run the real agent on a dataset question
def target(inputs: dict) -> dict:
    messages = inputs.get("messages", [])

    # Our example came from a LangGraph trace
    question = next(
        (
            m["content"]
            for m in messages
            if m.get("type") in ("human", "user")
            or m.get("role") in ("human", "user")
        ),
        None,
    )

    if not isinstance(question, str):
        raise ValueError("No customer question found")

    return {"answer": ask_agent(question)}


# STEP B: Evaluate the generated answer
def refund_policy_accuracy(
    outputs: dict,
    reference_outputs: dict,
) -> dict:

    answer = outputs.get("answer", "").lower()
    print("Evaluator reference keys:", list((reference_outputs or {}).keys()))
    reference = reference_outputs.get("answer", "")

    if not reference:
        raise ValueError("Reference answer is missing")

    # Four required policy details
    checks = {
        "return_window": "30 days" in answer,
        "unused_items": "unused" in answer,
        "original_packaging": "original packaging" in answer,
        "refund_timing": (
            "5-7 business days" in answer
            or "5–7 business days" in answer
        ),
    }

    score = int(all(checks.values()))

    return {
        "key": "refund_policy_accuracy",
        "score": score,
        "comment": str(checks),
    }



# STEP C: Execute evaluation in LangSmith
if __name__ == "__main__":
    experiment = client.evaluate(
        target,
        data="cloudcart-support-evals",
        evaluators=[
        refund_policy_accuracy,
        semantic_correctness,
],
        experiment_prefix="cloudcart-refund-v1",
    )

    print("Evaluation submitted.")
