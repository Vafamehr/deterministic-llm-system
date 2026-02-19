from fact_packet_reader import load_fact_packets, get_fact_packets_for_projects
from decision_engine import assess_risk_from_packets

df = load_fact_packets("outputs/project_fact_packets.csv")
packets = get_fact_packets_for_projects(df, ["A", "B"])

result = assess_risk_from_packets(packets)

print(result)
