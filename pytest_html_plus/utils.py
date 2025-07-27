def extract_trace_block(trace: str) -> str:
    try:
        if not trace:
            return ""
        lines = trace.splitlines()
        trace_lines = []

        for line in lines:
            if line.lstrip().startswith("E "):
                break
            trace_lines.append(line)
        return "\n".join(trace_lines)
    except Exception as e:
        return f"[Error extracting trace block: {e}]"


def extract_error_block(error: str) -> str:
    try:
        if not error:
            return ""
        error_lines = [line for line in error.splitlines() if line.strip().startswith("E ")]
        return "\n".join(error_lines).strip() or error.strip()
    except Exception as e:
        return f"[Error extracting error block: {e}]"
