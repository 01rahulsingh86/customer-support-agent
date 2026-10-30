from evaluate_agent import refund_policy_accuracy

reference = {
    "answer": (
        "CloudCart accepts returns within 30 days of delivery. "
        "Items must be unused and in original packaging. "
        "Refunds are issued to the original payment method "
        "within 5-7 business days after return approval."
    )
}

test_cases = [
    {
        "name": "Correct response",
        "answer": (
            "Returns are accepted within 30 days. "
            "Items must be unused and in original packaging. "
            "Refunds go to the original payment method "
            "within 5-7 business days after approval."
        ),
        "expected": 1,
    },
    {
        "name": "Incorrect return policy",
        "answer": (
            "CloudCart accepts returns within 60 days. "
            "Used items can be returned for a full refund."
        ),
        "expected": 0,
    },
    {
        "name": "Incomplete response",
        "answer": (
            "You can return your purchase within 30 days."
        ),
        "expected": 0,
    },
{
    "name": "Adversarial negation",
    "answer": (
        "CloudCart does not accept returns within 30 days. "
        "Items must be unused and in original packaging. "
        "Refunds are never issued within 5-7 business days."
    ),
    "expected": 0,
},

]


for case in test_cases:
    result = refund_policy_accuracy(
        outputs={"answer": case["answer"]},
        reference_outputs=reference,
    )

    actual = result["score"]

    assert actual == case["expected"], (
        f"{case['name']}: "
        f"expected {case['expected']}, got {actual}"
    )

    print(
        f"PASS: {case['name']} "
        f"(expected={case['expected']}, actual={actual})"
    )

print("\nAll evaluator tests passed!")
