import os

from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Set OPENAI_API_KEY in your .env file")


# TOOL: The agent can call this function
def get_refund_policy() -> str:
    """Retrieve CloudCart's official refund policy."""
    return (
        "CloudCart accepts returns within 30 days of delivery. "
        "Items must be unused and in original packaging. "
        "Refunds are issued to the original payment method "
        "within 5-7 business days after return approval."
    )


# AGENT: LLM + tools + instructions
agent = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[get_refund_policy],
    system_prompt=(
        "You are CloudCart's customer support agent. "
        "Be professional, helpful, and concise. "
        "For refund policy questions, use get_refund_policy. "
        "Do not invent company policies or guarantees. "
        "If you do not have enough information, say so."
    ),
)


# RUN: Send a customer message to the agent

# Reusable function for the API
def ask_agent(question: str) -> str:
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    return str(result["messages"][-1].content)


# Only runs when executing agent.py directly
if __name__ == "__main__":
    question = "What is your refund policy?"
    print(ask_agent(question))
