def export_to_md(messages):
    return "\n".join([f"{m['role']}: {m['content']}" for m in messages])
