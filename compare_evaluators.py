
from evaluate_agent import refund_policy_accuracy
from llm_judge import semantic_correctness

reference = {
    "answer": (
        "CloudCart accepts returns within 30 days of delivery. "
        "Items must be unused and in original packaging. "
        "Refunds are issued to the original payment method "
        "within 5-7 business days after return approval."
    )
}

wrong_answer = {
    "answer": (
        "CloudCart does NOT accept returns within 30 days. "
        "Items must be unused and in original packaging. "
        "Refunds are NEVER issued to the original payment "
        "method within 5-7 business days after approval."
    )
}

# Evaluator 1: deterministic keyword checks
keyword_result = refund_policy_accuracy(
    outputs=wrong_answer,
    reference_outputs=reference,
)

# Evaluator 2: LLM-as-a-Judge
semantic_result = semantic_correctness(
    outputs=wrong_answer,
    reference_outputs=reference,
)

print("\n=== EVALUATOR COMPARISON ===")
print("Ground truth: 0 (incorrect answer)")
print("Keyword score:", keyword_result["score"])
print("Semantic score:", semantic_result["score"])
print("Judge reasoning:", semantic_result["comment"])

if keyword_result["score"] != semantic_result["score"]:
    print("\nDISAGREEMENT DETECTED")

assert keyword_result["score"] == 1
assert semantic_result["score"] == 0

print("\nComparison completed successfully!")
