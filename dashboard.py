import streamlit as st
import numpy as np
import pandas as pd 
import plotly.graph_objects as go
from plotly.offline import iplot
import chart_studio.plotly as py
import plotly
import matplotlib.pyplot as plt
from plotly.offline import init_notebook_mode, iplot
import plotly.figure_factory as ff
import cufflinks
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='pearl')
import chart_studio
chart_studio.tools.set_credentials_file(username='XXX', api_key='XXX')
init_notebook_mode(connected=True)
pd.set_option('display.max_columns', 100)


st.set_page_config(layout="wide")
# load data
xls = pd.ExcelFile('network_connection_analysis_dashboard.xlsx', engine = 'openpyxl')

# Display statistics for all city 
st.title('网络连接情况对比分析')
st.markdown("### **选择城市：**")
list_of_city = ['全部','广州&深圳','成都','武汉','北京','上海','沈阳']
select_city = st.selectbox('', list_of_city)
city_df = pd.read_excel(xls, sheet_name=select_city)

st.table(city_df.assign(hack='').set_index('hack'))

# Display Box Chart for all city

text1=city_df['测试内容'].tolist()

trace0 = go.Box(
    
    y=city_df['Baseline'],
    name = 'Baseline',
    text=text1,
    boxpoints='all',
    marker = dict(
        color = 'rgb(214, 12, 140)',
    )
)

trace1 = go.Box(
    y=city_df['HKT_VPN'],
    text=text1,
    name = 'HKT_VPN',
    boxpoints='all',
    marker = dict(
        color = 'rgb(0, 128, 128)',
    )
)

trace2 = go.Box(
    y=city_df['CN_VPN'],
    text=text1,
    name = 'CN_VPN',
    boxpoints='all',
    marker = dict(
        color = 'rgb(12, 102, 14)',
    
    )
)

trace3 = go.Box(
    y=city_df['PGN'],
    text=text1,
    name = 'PGN',
    boxpoints='all',
    marker = dict(
        color = 'rgb(10, 0, 100)',
    )
)

trace4 = go.Box(
    y=city_df['Internet'],
    text=text1,
    name = 'Internet',
    boxpoints='all',
    marker = dict(
        color = 'rgb(100, 0, 10)',
    )
)

data = [trace0,trace1,trace2,trace3,trace4]


fig = go.Figure(data=data)
fig.update_layout( title = select_city+" 网络速度测试直方图"  ,autosize=False,width=1200,height=600)
st.plotly_chart(fig)


#Display Box Chart for all steps
st.markdown("### **选择测试内容：**")
list_of_test = ['系统登陆','测试一','测试二','测试三','测试四','测试五','测试六','测试七']

select_test = st.selectbox('', list_of_test)
test_df = pd.read_excel(xls, sheet_name=select_test)

#st.table(test_df.assign(hack='').set_index('hack'))
baseline=test_df['Baseline'][0]
horizon=test_df['Baseline'].copy(deep=True)

test_df.drop(columns=['Baseline'],inplace=True)
st.text("The baseline value is: "+str(baseline)+' (Red: > Baseline + 3s, Green: Otherwise).')
def color_survived(val):
    color = 'green' if (val<=baseline+3) else 'red'
    return f'background-color: {color}'



st.table(test_df.style.applymap(color_survived, subset=['HKT_VPN','CN_VPN','PGN','Internet']))


# Display Box Chart for all Test

trace5 = go.Box(
    
    y=test_df['HKT_VPN'],
    name = 'HKT_VPN',
    text=test_df['城市'].tolist(),
    boxpoints='all',
    marker = dict(
        color = 'rgb(214, 12, 140)',
    )
)


trace6 = go.Box(
    y=test_df['CN_VPN'],
    text=test_df['城市'].tolist(),
    name = 'CN_VPN',
    boxpoints='all',
    marker = dict(
        color = 'rgb(12, 102, 14)',
    
    )
)

trace7 = go.Box(
    y=test_df['PGN'],
    text=test_df['城市'].tolist(),
    name = 'PGN',
    boxpoints='all',
    marker = dict(
        color = 'rgb(10, 0, 100)',
    )
)

trace8 = go.Box(
    y=test_df['Internet'],
    text=test_df['城市'].tolist(),
    name = 'Internet',
    boxpoints='all',
    marker = dict(
        color = 'rgb(100, 0, 10)',
    )
)

data2 = [trace5,trace6,trace7,trace8]

fig2 = go.Figure(data=data2)
fig2.add_trace(go.Scatter(x=['HKT_VPN','CN_VPN','PGN','Internet'], y=horizon, mode="lines", name="Baseline"))
fig2.update_layout( title = select_test+" 网络速度测试直方图"  ,autosize=False,width=1200,height=600)
st.plotly_chart(fig2)