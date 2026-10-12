"""Example usage for Context Window Semantic Compression & Salience Pruner."""
from client import ContextWindowSaliencePruner

if __name__ == "__main__":
    msgs = [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "tool", "content": "x" * 800},
        {"role": "user", "content": "How do I fix this error?"}
    ]
    res = ContextWindowSaliencePruner.prune_context(msgs, max_tokens=100)
    print("Retained Count:", res["retained_messages_count"])
