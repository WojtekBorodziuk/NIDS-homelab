import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="NIDS Dashboard", layout="wide")
st.title("🛡️ NIDS Security Dashboard")

def load_data():
    # Ładujemy dane SQL do obiektu Pandas DataFrame
    conn = sqlite3.connect("nids_alerts.db")
    df = pd.read_sql_query("SELECT * FROM alerts ORDER BY id DESC", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.info("Brak zarejestrowanych incydentów.")
else:
    st.metric("Całkowita liczba ataków", len(df))
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Dziennik Zdarzeń")
        st.dataframe(df, use_container_width=True)
        
    with col2:
        st.subheader("Źródła Ataków")
        st.bar_chart(df['source_ip'].value_counts())

if st.button("Odśwież"):
    st.rerun()
