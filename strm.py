import streamlit as st
import pandas as pd
from pymongo import MongoClient
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="NBA Players Analysis", 
    page_icon="🏀", 
    layout="wide",
    initial_sidebar_state="expanded"
)


st.sidebar.title("NBA Dashboard")
st.sidebar.markdown("""
Welcome to NBA analysis
""")
st.sidebar.markdown("---")
st.sidebar.write("📁made by logic lords team")

st.title("full NBA analysis 🏀")
st.markdown("explore players ,figures and visualisation.")

page_bg = """
<style>
body {
    background-color: #F5F5F5;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)
client = MongoClient("mongodb://localhost:27017/")
db = client["nba_database"] 
players_collection = db['players_stats']

data=list(players_collection.find())
df=pd.DataFrame(data)

if '_id' in df.columns:
    df.drop('_id',axis=1,inplace=True)
    
df.drop_duplicates(inplace=True)

total_players = df['Player'].nunique()
total_teams = df['Team'].nunique()
top_scorer = df.sort_values(by='PTS', ascending=False).iloc[0]['Player']

st.markdown("## 📊 overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="number of players", value=total_players)

with col2:
    st.metric(label="number of teams", value=total_teams)

with col3:
    st.metric(label="best player", value=top_scorer)
st.markdown("## 📈 visualisation")


collection = db["myvisual"]  
plots = list(collection.find())

collection = db["myvisual"]  
plots = list(collection.find())


for plot in plots:
    title = plot['title']
    image_data = plot['image']

    
    image = Image.open(BytesIO(base64.b64decode(image_data)))

    st.subheader(f"📌 {title}")
    st.image(image)
    
    st.markdown("---")
st.sidebar.download_button(
    label="📥 download csv_file",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='cleand_players.csv',
    mime='text/csv'
)

st.markdown("---")

with open("NBA_PROJECT.pdf", "rb") as f:

    st.download_button(
        label="View PDF Report",
        data=f,
        file_name="NBA_Report.pdf",
        mime="application/pdf"
    )

st.header("player exploration")
data = list(players_collection.find())
df = pd.DataFrame(data)

st.title("player details:")

teams = df['Team'].unique()
selected_team = st.selectbox("choose your team:", teams)

filtered_df = df[df['Team'] == selected_team]
players = filtered_df['Player'].unique()
selected_player = st.selectbox("choose player", players)

player_info = filtered_df[filtered_df['Player'] == selected_player]

st.subheader(f"details: {selected_player}")
st.dataframe(player_info)