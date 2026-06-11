import streamlit as st
import pickle
import pandas as pd

pipe=pickle.load(open('pipe.pkl','rb'))
df=pickle.load(open('df.pkl','rb'))


st.markdown(
"""
<h1 style='text-align:center;color:#00BFFF;'>
🏏 IPL WIN PREDICTOR
</h1>
""",
unsafe_allow_html=True
)

teams=sorted(df['batting_team'].unique())
cities=sorted(df['city'].unique())

Batting_team=st.selectbox(
    'select Batting team',
    teams
)

Bowling_team=st.selectbox(
    'select bowling team',
    teams
)

select_city=st.selectbox(
    'select match city',
    cities
)

if Batting_team==Bowling_team:
    st.error('Batting and Bowling team cannot be same.')
    st.stop()
    
col1,col2=st.columns(2)

with col1:
    target=st.number_input('Target')
with col2:
    score=st.number_input('Score')

col3,col4=st.columns(2)

with col3:
    overs=st.number_input('Overs completed.')
    
with col4:
    wickets=st.number_input('wickets out')
    
if st.button('predict probability'):

    if overs <= 0:
        st.error("Overs must be greater than 0")
        st.stop()
    if wickets > 10:
        st.error("Wickets cannot exceed 10")
        st.stop()

    else:
        runs_left = target - score

        balls_left = 120 - (overs * 6)

        wickets_left = 10 - wickets

        crr = score / overs

        rrr = (runs_left * 6) / balls_left

        
        
    input_df = pd.DataFrame({
    'batting_team':[Batting_team],
    'bowling_team':[Bowling_team],
    'city':[select_city],
    'runs_left':[runs_left],
    'balls_left':[balls_left],
    'wickets_left':[wickets_left],
    'target':[target],
    'crr':[crr],
    'rrr':[rrr]
})
    result = pipe.predict_proba(input_df)
        
    
    loss = round(result[0][0] * 100)
    win = round(result[0][1] * 100)

    col1,col2 = st.columns(2)

    with col1:
        st.metric(
        label=Batting_team,
        value=f"{win}%"
    )

    with col2:
        st.metric(
        label=Bowling_team,
        value=f"{loss}%"
    )