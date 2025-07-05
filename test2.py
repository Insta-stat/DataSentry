import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('raw_data/described_data.csv')
df = df.sort_values(by='videoPlayCount', ascending=False).head(1)

df[['videoUrl']].to_csv('input_data/videos.csv', index=False)

print(df)