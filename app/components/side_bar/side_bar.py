import streamlit as st


def side_bar():
    if "plant" not in st.session_state:
        st.session_state["plant"] = None
    with st.sidebar:
        st.session_state["plant"] = st.selectbox("usina", ["Segredo", "Santo Antonio"])
