"""Code analysis graph boundary.

The concrete LangGraph implementation will orchestrate:
file parsing -> structure analysis -> quality review -> capability evidence -> report generation.
"""


class CodeAnalysisGraph:
    name = "code_analysis"

    def describe(self) -> list[str]:
        return [
            "parse_files",
            "summarize_structure",
            "review_quality",
            "extract_capability_evidence",
            "generate_report",
        ]
