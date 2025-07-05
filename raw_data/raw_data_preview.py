import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', 500)
pd.set_option('display.expand_frame_repr', True)


df = pd.read_csv('described_data.csv')
df = df[
    [
        'inputUrl',
        'url',
        'videoUrl',
        'timestamp',
        'commentsCount',
        'likesCount',
        'videoPlayCount',
        'videoDuration',
        'engagementRate',
        'commentRate',
        'likeRate',
        'viralityIndex',
        'performanceScore'
    ]
]
print(df)