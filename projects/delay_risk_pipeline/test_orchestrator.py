from fact_packet_reader import load_fact_packets, get_fact_packets_for_projects
from projects.delay_risk_pipeline.orchestrator_root_old import run_full_assessment

df = load_fact_packets("outputs/project_fact_packets.csv")
packets = get_fact_packets_for_projects(df, ["A", "B"])

llm_result,deterministic_result = run_full_assessment(packets)



result = run_full_assessment(packets)

print(result)
