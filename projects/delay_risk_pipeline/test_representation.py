import pandas as pd
from delay_risk.features.build_features import build_features
from delay_risk.representation.summarize import summarize_projects

df = pd.read_csv("data/sample_projects.csv")

feat = build_features(df)
summary = summarize_projects(feat)

print(summary)
