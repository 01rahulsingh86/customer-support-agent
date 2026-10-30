
from llm_judge import semantic_correctness

reference = {
    "answer": (
        "CloudCart accepts returns within 30 days of delivery. "
        "Items must be unused and in original packaging. "
        "Refunds are issued to the original payment method "
        "within 5-7 business days after return approval."
    )
}

cases = [
    {
        "name": "Correct answer",
        "answer": reference["answer"],
        "expected": 1,
    },
    {
        "name": "Incorrect return window",
        "answer": (
            "CloudCart accepts returns within 60 days. "
            "Items must be unused and in original packaging. "
            "Refunds go to the original payment method "
            "within 5-7 business days after approval."
        ),
        "expected": 0,
    },
    {
        "name": "Incomplete answer",
        "answer": "You can return your purchase within 30 days.",
        "expected": 0,
    },
    {
        "name": "Adversarial negation",
        "answer": (
            "CloudCart does NOT accept returns within 30 days. "
            "Items must be unused and in original packaging. "
            "Refunds are NEVER issued to the original payment "
            "method within 5-7 business days after approval."
        ),
        "expected": 0,
    },
]

for case in cases:
    result = semantic_correctness(
        outputs={"answer": case["answer"]},
        reference_outputs=reference,
    )

    actual = result["score"]
    passed = actual == case["expected"]

    print(f"\nTEST: {case['name']}")
    print(f"Expected: {case['expected']}")
    print(f"Actual:   {actual}")
    print(f"Reason:   {result['comment']}")
    print("PASS" if passed else "FAIL")

    assert passed, f"Judge misclassified: {case['name']}"

print("\nAll judge calibration cases passed!")
