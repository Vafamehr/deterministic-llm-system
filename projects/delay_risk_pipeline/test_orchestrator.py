from fact_packet_reader import load_fact_packets, get_fact_packets_for_projects
from orchestrator import run_full_assessment

df = load_fact_packets("outputs/project_fact_packets.csv")
packets = get_fact_packets_for_projects(df, ["A", "B"])

result = run_full_assessment(packets)

print(result)
