import streamlit as st
import streamlit.components.v1 as stc

def displayPageTitle(title):
    LOGO_BANNER = """
        <div style="background-color:#464e5f;padding:3px;border-radius:10px";>
        <h1 style="color:white;text-align:center;"> """ + title + """ </h1>
        </div> """

    stc.html(LOGO_BANNER)

def tabs(default_tabs=[], default_active_tab=0):
        if not default_tabs:
            return None
        active_tab = st.radio("", default_tabs, index=default_active_tab)
        child = default_tabs.index(active_tab) + 1
        st.markdown("""  
            <style type="text/css">
            div[role=radiogroup] > label > div:first-of-type {
               display: none
            }
            div[role=radiogroup] {
                flex-direction: unset
            }
            div[role=radiogroup] label {        
                border: 1px solid #999;
                background: #EEE;
                padding: 4px 20px 4px 10px;
                border-radius: 4px 4px 0 0;
                position: relative;
                top: 1px;
                }
            div[role=radiogroup] label:nth-child(""" + str(child) + """) {    
                background: #90ee90 !important;
                border-bottom: 1px solid transparent;
            }         
            .css-qrbaxs {
                min-height: 0px !important;
            }
            </style>
        """, unsafe_allow_html=True)
        return active_tab
