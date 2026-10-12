"""Context Window Semantic Compression & Salience Pruner.
100% Python Standard Library.
"""

class ContextWindowSaliencePruner:
    """Prunes low-salience conversational turns and verbose tool logs to fit strict LLM context token budgets."""

    @staticmethod
    def prune_context(messages: list, max_tokens: int = 1000) -> dict:
        scored = []
        for idx, msg in enumerate(messages):
            role = msg.get("role", "user")
            text = msg.get("content", "")
            tokens = max(1, len(text) // 4)
            salience = 1.0 if role == "system" or idx == len(messages) - 1 else (0.8 if "?" in text or "error" in text.lower() else 0.4)
            scored.append({
                "index": idx,
                "role": role,
                "content": text,
                "tokens": tokens,
                "salience": salience
            })

        scored_sorted = sorted(scored, key=lambda x: (x["salience"], x["index"]), reverse=True)
        retained = []
        used_tokens = 0
        for item in scored_sorted:
            if used_tokens + item["tokens"] <= max_tokens:
                retained.append(item)
                used_tokens += item["tokens"]

        retained.sort(key=lambda x: x["index"])
        return {
            "original_messages_count": len(messages),
            "retained_messages_count": len(retained),
            "used_tokens": used_tokens,
            "retained_messages": [{"role": r["role"], "content": r["content"]} for r in retained]
        }
