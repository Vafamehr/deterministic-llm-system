# from tools.contracts import ToolSpec, ToolRequest, ToolResult

# print("OK:", ToolSpec, ToolRequest, ToolResult)


from tools.contracts import ToolRequest
from tools.envelope import ToolEnvelope
from tools.registry import TOOL_REGISTRY
from tools.runner import ToolRunner


def main() -> None:
    runner = ToolRunner(registry=TOOL_REGISTRY)

    envelope = ToolEnvelope(allowed_tools={"get_current_time"}, max_calls=1)

    req = ToolRequest(
        tool_name="get_current_time",
        arguments={},  # no args for this tool
    )

    res = runner.run(req, envelope)
    print("success:", res.success)
    print("data:", res.data)
    print("error:", res.error)
    print("calls_made:", envelope.calls_made)


if __name__ == "__main__":
    main()