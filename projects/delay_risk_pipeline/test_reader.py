from fact_packet_reader import load_fact_packets, get_fact_packets_for_projects

df = load_fact_packets("outputs/project_fact_packets.csv")
packets = get_fact_packets_for_projects(df, ["A"])

print(packets[0])
