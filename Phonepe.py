# Importing Libraries
import json
import os
import pandas as pd
import streamlit as st
#from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px
import psycopg2 as pg2
from psycopg2 import extras
import plotly.io as pio



#pio.renderers.default = 'browser'

# Connect to PostgreSQL with the specified database
db_config = pg2.connect(
    host="localhost",
    user="postgres",
    password="Jesikather@1206",
    database="phonepe",  # Connect directly to the specified database
    port="5432",
)

# Set autocommit mode
db_config.set_session(autocommit=True)

# Creating a cursor
cursor = db_config.cursor()



img = Image.open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\pngwing.com.png")
st.set_page_config(page_title="PhonePe Pulse", page_icon=img, layout="wide", initial_sidebar_state="expanded"
)
# Get the Agsunset color palette
#agsunset_colors = px.colors.sequential.
sidebar_bg_color = "#5F259F"
appview_bg_color = "#C98ADC"
# Apply the background color using st.markdown

page_bg_color = f"""
<style>
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {sidebar_bg_color};
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background-color: {appview_bg_color};
            background-size: 180%;
            background-position: top left;
            background-repeat: no-repeat;
            background-attachment: local;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        [data-testid="stToolbar"] {{
            right: 2rem;
        }}
    </style>
"""


# Apply the background color using st.markdown
st.markdown(page_bg_color, unsafe_allow_html=True)

           # Specifies the base theme (either "light" or "dark")
 



icons = {
    "Home": "🏠",
    "Geo visualization":"🌏",
    "Basic insights": "🔄",
    "Top Charts": "📈",
    "Explore Data": "🌐",
    "ABOUT": "📊",
    "Readme": "👥",
}

SELECT = st.sidebar.selectbox("Choose an option", list(icons.keys()), format_func=lambda option: f'{icons[option]} {option}', key='selectbox')

# MENU 1 - HOME
if SELECT == "Home":
    st.snow()

    col1,col2 = st.columns(2)
    col1.image(Image.open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\phonepe.png"),width = 300)
    with col1:
        
        st.write(" ")
        st.write(" ")
        
        st.subheader("PhonePe is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
          st.video(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\upi.mp4")

if SELECT == "Geo visualization":
    st.balloons()

    india_states = json.load(open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\states_india.geojson", "r"))
                    
    state_id_map = {
                        'telangana': 0,
                        'andaman-&-nicobar-islands': 35,
                        'andhra-pradesh': 28,
                        'arunachal-pradesh': 12,
                        'assam': 18,
                        'bihar': 10,
                        'chhattisgarh': 22,
                        'daman-&-diu': 25,
                        'goa': 30,
                        'gujarat': 24,
                        'haryana': 6,
                        'himachal-pradesh': 2,
                        'jammu-&-kashmir': 1,
                        'jharkhand': 20,
                        'karnataka': 29,
                        'kerala': 32,
                        'ladakh': 31,
                        'madhya-pradesh': 23,
                        'maharashtra': 27,
                        'manipur': 14,
                        'chandigarh': 4,
                        'puducherry': 34,
                        'punjab': 3,
                        'rajasthan': 8,
                        'sikkim': 11,
                        'tamil-nadu': 33,
                        'tripura': 16,
                        'uttar-pradesh': 9,
                        'uttarakhand': 5,
                        'west-bengal': 19,
                        'odisha': 21,
                        'dadra-&-nagar-haveli': 26,
                        'meghalaya': 17,
                        'mizoram': 15,
                        'nagaland': 13,
                        'nct-of-delhi': 7
                    }
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]     

    cursor.execute("SELECT State, SUM(map_count) AS Total_Transactions, SUM(map_amount) AS Total_amount FROM map_transaction WHERE Year = 2018 AND Quarter = 3 GROUP BY State ORDER BY State")
    df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
    df1["id"] = df1["State"].apply(lambda x: state_id_map.get(x, -1))
    
    fig = px.choropleth(
                df1,
                locations="id",
                geojson=india_states,
                title="State Wise Phonepe Transaction",
                color='Total_Transactions',
                color_continuous_scale='sunset',
                hover_name="State",
                hover_data=["State", "Total_amount"]
                
            )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
    legend_title_text="Transaction_type",
    margin=dict(
                l=20, r=10, t=20, b=20
            ),  # Adjust the values to set the margin
            paper_bgcolor="black",  # Set background color
            plot_bgcolor="black",
    
        )
    #fig.show()
    fig.update_layout(
        margin=dict(
            l=20, r=10, t=20, b=20
        ),  # Adjust the values to set the margin
        paper_bgcolor="black",  # Set background color
        plot_bgcolor="black",

    )
    # Set a default color for bars
    st.plotly_chart(fig)
            
   
    
# MENU 2 - Basic insights:
if SELECT == "Basic insights":
    st.snow()

    st.markdown("## :red[BASIC INSIGHTS]")
    
    st.write("----")
    st.subheader("Explore key insights and trends within the dataset")
    options = ["--select--",
               "1. Top 10 states based on year and amount of transaction",
               "2. Least 10 states based on type and amount of transaction",
               "3. Top 10 mobile brands based on percentage of transaction",
               "4. Least 10 mobile brands based on percentage of transaction",
               "5. Top 10 Registered-users based on States and District",
               "6. Least 10 registered-users based on Districts and states",
               "7. Top 10 Districts based on states and amount of transaction",
               "8. Least 10 Districts based on states and amount of transaction",
               "9. Top 10 Districts based on states and registeredUsers",
               "10. Least 10 Districts based on states and registeredUsers"]
    SELECTED = st.selectbox("Select the option",options)
    

    if SELECTED=="1. Top 10 states based on year and amount of transaction":
        cursor.execute("SELECT  State, Year, SUM(top_amount) AS Total_Transaction_Amount FROM top_transaction GROUP BY State, Year ORDER BY Total_Transaction_Amount DESC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(),columns=['State','Year','top_amount'])
        # Corrected column name

        st.markdown(
            "## :black[Top 10 states with the highest transaction amounts per year]"
        )

        col1, col2 = st.columns([4, 4], gap="medium")

        with col1:
            styled_df = df.style.bar(subset=["top_amount"])
            st.dataframe(styled_df, height=390, width=400)

        with col2:
            # Assuming df is your DataFrame with the relevant data
            fig = px.bar(
                df,
                x="top_amount",
                y="State",
                orientation="h",
                color="State",
                color_continuous_scale="purples",
            )
            fig.update_layout(
                xaxis_title="top_amount",
                yaxis_title="State",
                legend_title_text="State",
                margin=dict(
                    l=20, r=10, t=20, b=20
                ),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",  # Set plot background color
            )

            st.plotly_chart(fig)
        

    elif SELECTED=="2. Least 10 states based on type and amount of transaction":
        cursor.execute("SELECT DISTINCT State, SUM(top_count) as Total FROM top_transaction GROUP BY State ORDER BY Total ASC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(),columns=['State','top_amount'])
        st.markdown("## :black[Least 10 states based on transaction type and amount]")

        col1, col2 = st.columns(2)
        with col1:
            styled_df = df.style.bar(subset=["top_amount"])
            st.dataframe(styled_df, height=390, width=400)
        with col2:
            # st.("## :red[Transaction Amounts in Bottom 10 States ]")

            # Create a bordered container for the pie chart
            pie_container = st.container()

            # Display the pie chart inside the container
            with pie_container:
                fig = px.pie(df, values="top_amount", names="State")
                fig.update_traces(
                    textinfo="percent+label", pull=[0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                )  # Adjust the pull values for better visibility
                fig.update_layout(
                    margin=dict(
                        l=20, r=10, t=20, b=20
                    ),  # Adjust the values to set the margin
                    paper_bgcolor="black",  # Set background color
                    plot_bgcolor="black",  # Set plot background color
                )

            st.plotly_chart(fig)

    elif SELECTED=="3. Top 10 mobile brands based on percentage of transaction":
        
        cursor.execute("SELECT DISTINCT user_brand,SUM(user_percentage) as Total_Percentage FROM aggregated_user GROUP BY user_brand ORDER BY Total_Percentage DESC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(),columns=['user_brand','user_percentage'])
        col1, col2 = st.columns([1.5, 2], gap="small")

        with col1:
            # st.write(df)
            styled_df = df.style.bar(subset=["user_percentage"])
            st.dataframe(styled_df, height=390, width=400)

        with col2:
            # Adding a new column for color bands
            fig_sunburst = px.sunburst(df, path=["user_brand", "user_percentage"])
            fig_sunburst.update_layout(
                margin=dict(
                    l=20, r=10, t=20, b=20
                ),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",  # Set plot background color
            )

            # Displaying sunburst chart using Streamlit
            st.plotly_chart(fig_sunburst)


    elif SELECTED=="4. Least 10 mobile brands based on percentage of transaction":
        cursor.execute("SELECT DISTINCT user_brand,SUM(user_percentage) as Total_Percentage FROM aggregated_user GROUP BY user_brand ORDER BY Total_Percentage ASC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(),columns=['user_brand','user_percentage'])
        col1, col2 = st.columns([1.5, 2], gap="small")
        with col1:
            styled_df = df.style.bar(subset=["user_percentage"])
            st.dataframe(styled_df, height=390, width=400)
        with col2:

            fig_scatter = px.scatter(
                df,
                x="user_brand",
                y="user_percentage",
                color="user_brand",
                color_continuous_scale="viridis",
            )
            fig_scatter.update_layout(
                xaxis_title="user_brand",
                yaxis_title="user_percentage",
                legend_title_text="User Brand",
                margin=dict(
                    l=20, r=10, t=20, b=20
                ),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",  # Set plot background color
            )
            st.plotly_chart(fig_scatter)

    elif SELECTED=="5. Top 10 Registered-users based on States and District":
        cursor.execute(
            """SELECT DISTINCT State, district_pincode, SUM(registeredUsers) AS Users
                        FROM top_user
                        GROUP BY State, district_pincode
                        ORDER BY Users DESC
                        LIMIT 10;"""
                        )
        df = pd.DataFrame(cursor.fetchall(),columns=['State','district_pincode','registeredUsers'])

        col1, col2 = st.columns([1.5, 2], gap="small")

        with col1:
            styled_df = df.style.bar(subset=["registeredUsers"])
            st.dataframe(styled_df, height=390, width=370)

        with col2:
            # Creating a 3D scatter plot with different colors for each State
            fig = px.scatter_3d(
                df, x="district_pincode", y="State", z="registeredUsers", color="State"
            )

            # Updating layout settings
            fig.update_layout(
                scene=dict(
                    xaxis_title="District Pincode",
                    yaxis_title="State",
                    zaxis_title="registeredUsers",
                ),
                legend_title_text="User Brand",
                margin=dict(l=20, r=10, t=20, b=20),
                paper_bgcolor="black",
                plot_bgcolor="black",
            )
            # Displaying the 3D scatter plot using Streamlit
            st.plotly_chart(fig)

    elif SELECTED=="6. Least 10 registered-users based on Districts and states":
        cursor.execute("SELECT DISTINCT State,district_pincode,SUM(registeredUsers) AS Users FROM top_user GROUP BY State,district_pincode ORDER BY Users ASC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(),columns=['State','district_pincode','registeredUsers'])
        
        col1, col2 = st.columns([1.5, 2], gap="small")
        with col1:
            styled_df = df.style.bar(subset=["registeredUsers"])
            st.dataframe(styled_df, height=390, width=400)
        with col2:

            fig_polar_bar = px.bar_polar(
                df, r="registeredUsers", theta="district_pincode", color="State"
            )
            # Customizing layout
            fig_polar_bar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        title="registeredUsers",
                        angle=45,
                    ),
                ),
                showlegend=True,
                margin=dict(
                    l=20, r=10, t=20, b=20
                ),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",  # Set plot background color
            )
            st.plotly_chart(fig_polar_bar)



    elif SELECTED=="7. Top 10 Districts based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT State,district_pincode,SUM(top_amount) AS Total  FROM top_transaction GROUP BY State,district_pincode ORDER BY Total DESC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(),columns=['State','district_pincode','top_amount'])

        col1, col2 = st.columns([1.5, 2], gap="small")
        with col1:
            st.write(df)
        with col2:

            fig_pie = px.pie(df, names="State", values="top_amount")

            # Customizing layout if needed
            fig_pie.update_layout(
                legend_title_text="State",
                margin=dict(
                    l=20, r=10, t=20, b=20
                ),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",  # Set plot background color
            )

            st.plotly_chart(fig_pie)

        

    elif SELECTED=="8. Least 10 Districts based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT State,district_pincode,SUM(top_amount) as Total FROM top_transaction GROUP BY State,district_pincode ORDER BY Total ASC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(),columns=['State','district_pincode','top_amount'])

        col1, col2 = st.columns([1.5, 2], gap="small")
        with col1:
            st.write(df)
        with col2:
            fig_pie = px.pie(df, names="State", values="top_amount")

            # Customizing layout if needed
            fig_pie.update_layout(
                legend_title_text="State",
                margin=dict(
                    l=20, r=10, t=20, b=20
                ),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",  # Set plot background color
            )

            st.plotly_chart(fig_pie)


    elif SELECTED=="9. Top 10 Districts based on states and registeredUsers":
        cursor.execute("SELECT DISTINCT State,district,SUM(registeredUsers) AS Total FROM map_user GROUP BY State,district ORDER BY Total DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','district','registeredUsers'])

        col1, col2 = st.columns([1.5, 2], gap="small")
        with col1:
            styled_df = df.style.bar(subset=["registeredUsers"])
            st.dataframe(styled_df, height=390, width=480)
        with col2:
            fig = px.bar(
                df,
                x="district",
                y="registeredUsers",
                labels={"registeredUsers": "Registered Users"},
            )
            fig.update_layout(
                xaxis_title="district",
                yaxis_title="Registered Users",
                margin=dict(
                    l=20, r=10, t=20, b=20
                ),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",  # Set plot background color
                font=dict(color="black"),  # Set font color
            )
            fig.update_traces(marker_color="purple")  # Set a default color for bars
            # fig.update_traces(marker_color='purple', selector=dict(type='bar', marker_color='skyblue'))  # Set color for a specific district
            # fig.update_traces(marker_color='orange', selector=dict(type='bar', marker_color='orange'))  # Set color for another district
            st.plotly_chart(fig)


    elif SELECTED=="10. Least 10 Districts based on states and registeredUsers":
        cursor.execute("SELECT DISTINCT State,district,SUM(registeredUsers) as Total FROM map_user GROUP BY State,district ORDER BY Total ASC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(),columns=['State','district','registeredUsers'])

        col1, col2 = st.columns([1.5, 2], gap="small")
        with col1:
            st.write(df)
        with col2:
            fig = px.bar(
                df,
                x="district",
                y="registeredUsers",
                labels={"registeredUsers": "Registered Users"},
            )
            fig.update_layout(
                xaxis_title="district",
                yaxis_title="Registered Users",
                margin=dict(
                    l=20, r=10, t=20, b=20
                ),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",  # Set plot background color
                font=dict(color="black"),  # Set font color
            )
            fig.update_traces(marker_color="Cyan")  # Set a default color for bars
            st.plotly_chart(fig)


# MENU 3 - TOP CHARTS            
if SELECT == "Top Charts":
    st.balloons()

    st.markdown("## :black[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
            )
        
    # Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")

        with col1:
            st.markdown("### :black[State]")
            cursor.execute(f"SELECT State, SUM(Transaction_count) as Total_Transactions_Count, SUM(Transaction_amount) as Total FROM aggregated_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY State ORDER BY Total DESC LIMIT 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_count','Transaction_amount'])
            fig = px.pie(df, values='Transaction_amount',
                            names='State',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transaction_count'],
                            labels={'Transaction_count':'Transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
                st.markdown("### :violet[District]")
                cursor.execute(f"SELECT district , SUM(map_count) as Total_Count, SUM(map_amount) as Total from map_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district ORDER BY Total DESC LIMIT 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['District', 'map_count','map_amount'])

                fig = px.pie(df, values='map_amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['map_count'],
                                labels={'map_count':'map_count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("### :black[Pincode]")
            cursor.execute(f"SELECT district_pincode, SUM(top_count) as Total_Transactions_Count, SUM(top_amount) as Total from top_transaction WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district_pincode ORDER BY Total DESC LIMIT 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['district_pincode', 'top_count','top_amount'])
            fig = px.pie(df, values='top_amount',
                                names='district_pincode',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['top_count'],
                                labels={'top_count':'top_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

    # Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :black[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                cursor.execute(f"SELECT user_brand, SUM(user_count) AS Total_Count, AVG(user_percentage)*100 AS Avg_Percentage FROM aggregated_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY user_brand order by Total_Count DESC LIMIT 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['user_brand', 'user_count','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="user_count",
                             y="user_brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   

        with col2:
            st.markdown("### :black[District]")
            cursor.execute(f"SELECT district, SUM(RegisteredUserS) as Total_Users FROM map_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)                        

        with col3:
            st.markdown("### :violet[Pincode]")
            cursor.execute(f"SELECT district_pincode, SUM(registeredUsers) AS Total_Users FROM top_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY district_pincode ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['district_pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='district_pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col4:
            st.markdown("### :black[State]")
            cursor.execute(f"SELECT State, SUM(registeredUsers) AS Total_Users  FROM map_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' GROUP BY State ORDER BY Total_Users DESC LIMIT 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Users'],
                             labels={'Total_Users':'Total_Users'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

# MENU 3 - EXPLORE DATA

if SELECT == "Explore Data":
    st.balloons()

    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    
    col1,col2 = st.columns(2)

    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
        
            st.markdown("## :black[Overall State Data - Transactions Count]")

            cursor.execute("SELECT State, SUM(map_count) AS Total_Transactions, SUM(map_amount) AS Total_amount FROM map_transaction WHERE Year = 2018 AND Quarter = 3 GROUP BY State ORDER BY State")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            fig_pie = px.pie(df1, names="State", values="Total_Transactions")

            # Customizing layout if needed
            fig_pie.update_layout(
                legend_title_text="State",
                margin=dict(
                    l=20, r=10, t=20, b=20
                ),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",  # Set plot background color
            )

            st.plotly_chart(fig_pie)
            
        

            # BAR CHART - TOP PAYMENT TYPE
            st.markdown("## :black[Top Payment Type]")
            cursor.execute(f"SELECT Transaction_type, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_amount FROM aggregated_transaction WHERE Year= '{Year}' AND Quarter = '{Quarter}' GROUP BY transaction_type ORDER BY Transaction_type")
            df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

            fig = px.bar(df,
                x="Transaction_type",
                y="Total_Transactions",
                orientation='v',
                color='Transaction_type',
                color_continuous_scale=px.colors.sequential.Agsunset_r)

            # Define pattern shapes for each bar
            patterns = ["x", "+", "."]

            # Update traces to add pattern shapes
            fig.update_traces(marker_pattern_shape=patterns)


            # Update layout settings
            fig.update_layout(
                margin=dict(l=20, r=10, t=20, b=20),  # Adjust the values to set the margin
                paper_bgcolor="black",  # Set background color
                plot_bgcolor="black",
            )

            # Display the bar chart
            st.plotly_chart(fig)



        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("## :black[Select any State to explore more]")
            # Dictionary to map lowercase state names to display names
            state_mapping = {
                'andaman-&-nicobar-islands': 'Andaman & Nicobar',
                'andhra-pradesh': 'Andhra Pradesh',
                'arunachal-pradesh': 'Arunachal Pradesh',
                'assam': 'Assam',
                'bihar': 'Bihar',
                'chandigarh': 'Chandigarh',
                'chhattisgarh': 'Chhattisgarh',
                'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
                'delhi': 'Delhi',
                'goa': 'Goa',
                'gujarat': 'Gujarat',
                'haryana': 'Haryana',
                'himachal-pradesh': 'Himachal Pradesh',
                'jammu-&-kashmir': 'Jammu & Kashmir',
                'jharkhand': 'Jharkhand',
                'karnataka': 'Karnataka',
                'kerala': 'Kerala',
                'ladakh': 'Ladakh',
                'lakshadweep': 'Lakshadweep',
                'madhya-pradesh': 'Madhya Pradesh',
                'maharashtra': 'Maharashtra',
                'manipur': 'Manipur',
                'meghalaya': 'Meghalaya',
                'mizoram': 'Mizoram',
                'nagaland': 'Nagaland',
                'odisha': 'Odisha',
                'puducherry': 'Puducherry',
                'punjab': 'Punjab',
                'rajasthan': 'Rajasthan',
                'sikkim': 'Sikkim',
                'tamil-nadu': 'Tamil Nadu',
                'telangana': 'Telangana',
                'tripura': 'Tripura',
                'uttar-pradesh': 'Uttar Pradesh',
                'uttarakhand': 'Uttarakhand',
                'west-benga': 'West Bengal'
            }

            # Using the mapping dictionary in the selectbox
            selected_state = st.selectbox("",
                                        list(state_mapping.values()),
                                        index=30,
                                        key="selected_state")

            # Reverse mapping to get the lowercase state name
            selected_state_lowercase = next(k for k, v in state_mapping.items() if v == selected_state)

            # Your SQL query
            cursor.execute(f"SELECT State, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_amount FROM aggregated_transaction WHERE Year= '{Year}' AND Quarter = '{Quarter}' AND State = '{selected_state_lowercase}' GROUP BY State ORDER BY State")

            # Creating DataFrame and plot
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            fig = px.bar_polar(df,
                        r='Total_Transactions',
                        theta='State',
                        title=f'Transactions trend in {selected_state}',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Purples_r)

        # Display the polar bar chart
            st.plotly_chart(fig, use_container_width=True)

    # EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :black[Overall State Data - User App opening frequency]")
        
        st.markdown("## :black[Select any State to explore more]")
        state_mapping = {
                'andaman-&-nicobar-islands': 'Andaman & Nicobar',
                'andhra-pradesh': 'Andhra Pradesh',
                'arunachal-pradesh': 'Arunachal Pradesh',
                'assam': 'Assam',
                'bihar': 'Bihar',
                'chandigarh': 'Chandigarh',
                'chhattisgarh': 'Chhattisgarh',
                'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
                'delhi': 'Delhi',
                'goa': 'Goa',
                'gujarat': 'Gujarat',
                'haryana': 'Haryana',
                'himachal-pradesh': 'Himachal Pradesh',
                'jammu-&-kashmir': 'Jammu & Kashmir',
                'jharkhand': 'Jharkhand',
                'karnataka': 'Karnataka',
                'kerala': 'Kerala',
                'ladakh': 'Ladakh',
                'lakshadweep': 'Lakshadweep',
                'madhya-pradesh': 'Madhya Pradesh',
                'maharashtra': 'Maharashtra',
                'manipur': 'Manipur',
                'meghalaya': 'Meghalaya',
                'mizoram': 'Mizoram',
                'nagaland': 'Nagaland',
                'odisha': 'Odisha',
                'puducherry': 'Puducherry',
                'punjab': 'Punjab',
                'rajasthan': 'Rajasthan',
                'sikkim': 'Sikkim',
                'tamil-nadu': 'Tamil Nadu',
                'telangana': 'Telangana',
                'tripura': 'Tripura',
                'uttar-pradesh': 'Uttar Pradesh',
                'uttarakhand': 'Uttarakhand',
                'west-benga': 'West Bengal'
            }
        
        selected_state = st.selectbox("",
                                        list(state_mapping.values()),
                                        index=30,
                                        key="selected_state")

            # Reverse mapping to get the lowercase state name
        selected_state_lowercase = next(k for k, v in state_mapping.items() if v == selected_state)
        cursor.execute(f"SELECT State,Year,Quarter,district,SUM(registeredUsers) AS Total_Users FROM map_user WHERE Year = '{Year}' AND Quarter = '{Quarter}' AND State = '{selected_state_lowercase}' GROUP BY State, district,Year,Quarter ORDER BY State,Year,Quarter,district")
        # Creating DataFrame and plot
        df = pd.DataFrame(cursor.fetchall(), columns=['State','Year','Quarter','district','Total_Users'])
        fig = px.scatter_3d(df,
                    x='Total_Users',
                    y='State',
                    z='district',
                    title=f'User {selected_state}',
                    color='Total_Users',
                    color_continuous_scale=px.colors.sequential.Agsunset)

        # Customizing layout if needed
        fig.update_layout(
            scene=dict(
                xaxis=dict(title='Total Users'),
                yaxis=dict(title='State'),
                zaxis=dict(title='Total Transactions'),
            ),
            margin=dict(l=20, r=10, t=20, b=20),  # Adjust the values to set the margin
            paper_bgcolor="black",  # Set background color
            plot_bgcolor="black",  # Set plot background color
        )

        # Display the 3D scatter plot
        st.plotly_chart(fig, use_container_width=True)

# MENU 4 - ABOUT  
if SELECT == "ABOUT":
    st.snow()

    st.image(Image.open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\phonepe.png"),width = 200)

    col1,col2 = st.columns(2)
    with col1:           
        st.image(Image.open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\190960-untitled-design-35.jpg"),width = 500)
        st.image(Image.open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\phonepe-graphic.png"),width = 500)
    with col2:
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                     " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                    " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                    "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
        st.markdown("")
        st.markdown("") 
        st.markdown("")
        st.markdown("")
        st.markdown("")
       
    st.video(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\upi.mp4")
    st.title("THE BEAT OF PHONEPE")        
    
    col1,col2 = st.columns(2)    
    with col1:  
        
        st.write("---")
        st.image(Image.open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\mobile_phone_coin.jpg"),width = 500)
        st.image(Image.open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\Phonepay-840x400.jpg"),width = 80)

    with col2:
        st.subheader("Third ET BFSI Innovation Tribe Virtual Summit & Awards")
        st.image(Image.open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\394056-PCQ3LZ-663.jpg"),width = 300)
        st.image(Image.open(r"C:\Users\jesik\OneDrive\Desktop\Phonepe\Phonepay-840x400.jpg"),width = 80)



# MENU 5 - Readme
if SELECT=="Readme":
    st.balloons()

    st.title('Phonepe Pulse Data Visualization and Exploration:A User-Friendly Tool Using Streamlit and Plotly')
    st.subheader('Problem Statement')
    st.caption('The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics.' 
               'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.' 
               'Extract data from the Phonepe pulse Github repository through scripting and clone it.' 
               'Transform the data into a suitable format and perform any necessary cleaning and pre-processing steps.' 
               'Insert the transformed data into a PostgreSQL database for efficient storage and retrieval.'
               'Create a live geo visualization dashboard using Streamlit and Plotly in Python to display the data in an interactive and visually appealing manner.'
                'Fetch the data from the MySQL database to display in the dashboard.'
                'Provide at least 10 different dropdown options for users to select different facts and figures to display on the dashboard.'
                'The solution must be secure, efficient, and user-friendly.'
                'The dashboard must be easily accessible and provide valuable insights and information about the data in the Phonepe pulse Github repository.')

    st.subheader('Technology Stack Used')

    st.text('1. Python.')
    st.text('2. JSON.')
    st.text('3. PostgreSQL.')
    st.text('4. OS.')
    st.text('5. Pandas Library.')
    st.text('6. Streamlit.')
    st.text('7. Plotly Library.')
    st.text('8. Image Library.')


    st.subheader('Process')

    st.caption('1. Data Extraction : Utilize scripting to clone the Phonepe Pulse GitHub repository, fetching the data and storing it in a suitable format like CSV or JSON.')
    st.caption('2. Data Transformation : Use Python scripting, along with Pandas and other libraries, to manipulate and pre-process the data. Tasks may include cleaning, handling missing values, and transforming the data for analysis and visualization.')           
    
    st.caption('3. Database Insertion : Employ the "psycopg2 " library in Python to connect to a PostgreSQL database. Insert the transformed data using SQL commands.')      
    st.caption('''4. Dashboard Creation : Utilize Streamlit and Plotly libraries in Python to craft an interactive dashboard. Leverage Plotly's geo map functions for data display, and use Streamlit to create a user-friendly interface with multiple dropdown options for users to select various facts and figures.''')
    st.caption('''5. Data Retrieval : Implement the "psycopg2" library to connect to the PostgreSQL database. Fetch the data into a Pandas dataframe and dynamically update the dashboard with the latest information.''')          
    st.caption('''6. Deployment : Ensure the solution's security, efficiency, and user-friendliness. Thoroughly test the solution before deploying the dashboard publicly, making it easily accessible to users.''') 
    st.caption('''7. Comprehensive Approach : This methodology harnesses the capabilities of Python and its rich library ecosystem to extract, transform, and analyze data. The result is a user-friendly dashboard that visually presents insights derived from the processed data. Note: The approach is adjusted for PostgreSQL usage instead of MySQL.''')     