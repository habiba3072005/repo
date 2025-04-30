import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="NBA Players Analysis", 
    page_icon="🏀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("NBA Dashboard")
st.sidebar.markdown("Welcome to NBA analysis")
st.sidebar.markdown("---")
st.sidebar.write("📁 Made by Logic Lords Team")

st.title("Full NBA Analysis 🏀")
st.markdown("Explore players, figures, and visualizations.")

df = pd.read_csv("cleand_players.csv")
df.drop_duplicates(inplace=True)

total_players = df['Player'].nunique()
total_teams = df['Team'].nunique()
top_scorer = df.sort_values(by='PTS', ascending=False).iloc[0]['Player']

st.markdown("## 📊 Overview")
col1, col2, col3 = st.columns(3)
col1.metric(label="Number of Players", value=total_players)
col2.metric(label="Number of Teams", value=total_teams)
col3.metric(label="Best Player", value=top_scorer)

st.markdown("## 📈 Visualizations")

st.subheader("📌 Age Distribution of NBA Players")
plt.figure(figsize=(10,6))
sns.histplot(df['Age'], bins=15, kde=True, color='skyblue')
plt.xlabel('Age')
plt.ylabel('Number of Players')
st.pyplot(plt.gcf())
st.markdown("---")

st.subheader("📌 Top 10 Players by Total Points")
top10_pts = df.sort_values(by='PTS', ascending=False).head(10)
plt.figure(figsize=(12,6))
sns.barplot(x='PTS', y='Player', data=top10_pts, palette='viridis')
st.pyplot(plt.gcf())
st.markdown("---")

st.subheader("📌 Top 10 Teams with Most Players")
top_teams = df['Team'].value_counts().head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=top_teams.values, y=top_teams.index, palette='pastel')
st.pyplot(plt.gcf())
st.markdown("---")

st.subheader("📌 Distribution of Player Positions")
pos_counts = df['Pos'].value_counts()
plt.figure(figsize=(8,8))
plt.pie(pos_counts.values, labels=pos_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.axis('equal')
st.pyplot(plt.gcf())
st.markdown("---")

st.subheader("📌 Age vs Total Points")
plt.figure(figsize=(10,6))
sns.scatterplot(x='Age', y='PTS', data=df, color='coral')
st.pyplot(plt.gcf())
st.markdown("---")

st.subheader("📌 Shooting Percentages Distribution")
percentage_cols = ['FG%', '3P%', '2P%', 'FT%']
plt.figure(figsize=(10,6))
sns.boxplot(data=df[percentage_cols], palette='Set2')
st.pyplot(plt.gcf())
st.markdown("---")

st.subheader("📌 Assists vs Total Rebounds by Position")
plt.figure(figsize=(10,6))
sns.scatterplot(x='AST', y='TRB', data=df, hue='Pos', palette='tab10', alpha=0.7)
st.pyplot(plt.gcf())
st.markdown("---")

st.subheader("📌 Top 10 Teams by Average Points")
team_avg_pts = df.groupby('Team')['PTS'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=team_avg_pts.values, y=team_avg_pts.index, palette='coolwarm')
st.pyplot(plt.gcf())
st.markdown("---")

st.subheader("📌 Shooting Percentages of Top 5 Players")
best_players = df.sort_values(by='PTS', ascending=False).head(5)
plt.figure(figsize=(10,6))
for i, player in best_players.iterrows():
    plt.plot(percentage_cols, player[percentage_cols], marker='o', label=player['Player'])
plt.ylabel('Percentage')
plt.legend()
st.pyplot(plt.gcf())
st.markdown("---")

st.subheader("📌 Correlation Heatmap of Player Statistics")
numeric_cols = ['Age', 'G', 'MP', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', '2P%', 'FT%']
plt.figure(figsize=(14,10))
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap='greys', fmt=".2f", linewidths=.5,cbar_kws={"shrink":0.8})
st.pyplot(plt.gcf())
st.markdown("---")

st.sidebar.download_button(
    label="📥 Download CSV File",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='cleand_players.csv',
    mime='text/csv'
)

with open("NBA_Report.pdf", "rb") as f:
    st.sidebar.download_button(
        label="📄 View PDF Report",
        data=f,
        file_name="NBA_Report.pdf",
        mime="application/pdf"
    )

st.header("Player Exploration")
teams = df['Team'].unique()
selected_team = st.selectbox("Choose your team:", teams)

filtered_df = df[df['Team'] == selected_team]
players = filtered_df['Player'].unique()
selected_player = st.selectbox("Choose player", players)

player_info = filtered_df[filtered_df['Player'] == selected_player]
st.subheader(f"Details: {selected_player}")
st.dataframe(player_info)

