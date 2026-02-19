from fact_packet_reader import load_fact_packets, get_fact_packets_for_projects
from llm_reasoner import (
    build_prompt,
    call_llm,
    parse_llm_output,
    validate_decision_schema
)


df = load_fact_packets("outputs/project_fact_packets.csv")
packets = get_fact_packets_for_projects(df, ["A", "B"])

prompt = build_prompt(packets)
raw = call_llm(prompt)

print("RAW LLM OUTPUT:")
print(raw)

parsed = parse_llm_output(raw)

print("\nPARSED OUTPUT:")
print(parsed)


validated = validate_decision_schema(parsed)

print("\nVALIDATED OUTPUT:")
print(validated)
