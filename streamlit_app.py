# ------------------------------
# 3. DATA RETRIEVAL FROM SQL
# ------------------------------
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

engine = create_engine("sqlite:///phonepe.db")

# ------------------------------
# 4. STREAMLIT HOME PAGE CONFIGURATION
# ------------------------------

st.set_page_config(page_title="📊 PhonePe Pulse Dashboard", layout="wide")
st.title("📊 PhonePe Pulse Dashboard")
st.markdown("Explore Digital Transactions, Users & Insurance Data Across India")

st.sidebar.header("Navigation")
page=st.sidebar.radio("Select a page",["Project Introduction","Home","Analysis","Creator Info"])
if page=="Project Introduction":
    st.title("PhonePe Transaction Insights")
    st.subheader("Data Visualization & Analysis")
    st.write("With the increasing reliance on digital payment systems like PhonePe, understanding the dynamics of transactions, user engagement, and insurance-related data is crucial for improving services and targeting users effectively. This project aims to analyze and visualize aggregated values of payment categories, create maps for total values at state and district levels, and identify top-performing states, districts, and pin codes.")
    st.image("data:image/jpeg;base64,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")
elif page=="Home":
    st.sidebar.subheader("🔍 Filters")
    years = pd.read_sql("SELECT DISTINCT Year FROM aggregate_transaction ORDER BY Year", engine)["Year"].tolist()
    quarters = pd.read_sql("SELECT DISTINCT Quarter FROM aggregate_transaction ORDER BY Quarter", engine)["Quarter"].tolist()
    states = pd.read_sql("SELECT DISTINCT State FROM aggregate_transaction ORDER BY State", engine)["State"].tolist()

    metric = st.sidebar.selectbox("Select Metric",["Transactions", "Users"])
    year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)
    quarter = st.sidebar.selectbox("Select Quarter", quarters, index=len(quarters)-1)
    selected_state = st.sidebar.selectbox("Select State", ["All India"] + states)

    if metric=="Transactions":
        if selected_state == "All India":
            query = f"""
                SELECT State, Transaction_type,
                        SUM(Transaction_count) AS Transaction_count,
                        SUM(Transaction_amount) AS Transaction_amount
                FROM aggregate_transaction
                WHERE Year = '{year}' AND Quarter = {quarter}
                GROUP BY State, Transaction_type
            """
        else:
            query = f"""
                SELECT State, Transaction_type,
                        SUM(Transaction_count) AS Transaction_count,
                        SUM(Transaction_amount) AS Transaction_amount
                FROM aggregate_transaction
                WHERE Year = '{year}' AND Quarter = {quarter}
                  AND State = '{selected_state}'
                GROUP BY State, Transaction_type
            """

        df_filtered = pd.read_sql(query, engine)

    # ------------------------------
    # 5. METRICS
    # ------------------------------
        query = f"""SELECT
                SUM(Transaction_count) AS total_txn,
                SUM(Transaction_amount) AS total_amt,
                SUM(Transaction_amount) / SUM(Transaction_count) AS avg_amt
                FROM aggregate_transaction
                WHERE Year = '{year}' AND Quarter = {quarter}
                {"AND State = '" + selected_state + "'" if selected_state != "All India" else ""}"""

        result = pd.read_sql(query, engine)
        total_txn = result["total_txn"].iloc[0]
        total_amt = result["total_amt"].iloc[0]
        total_amt1 = total_amt / 1e7
        avg_amt = result["avg_amt"].iloc[0]

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Transactions", f"{total_txn:,.0f}")
        c2.metric("Total Payment Value", f"₹{total_amt1:,.0f} Cr")
        c3.metric("Avg. Transaction Value", f"₹{avg_amt:,.0f}")
    
    # ------------------------------
    # 6. VISUALIZATIONS
    # ------------------------------

    ## 6.1 Transactions by State
        st.subheader("📍 Transactions by State")
        state_query = f"""
            SELECT State, SUM(Transaction_count) AS Transaction_count, 
                   SUM(Transaction_amount) AS Transaction_amount
            FROM aggregate_transaction
            WHERE Year = '{year}' AND Quarter = {quarter}
            {"AND State = '" + selected_state + "'" if selected_state != "All India" else ""}
            GROUP BY State
        """
        df_state = pd.read_sql(state_query, engine)
        df_state["Trans_amount"] = (df_state["Transaction_amount"] / 10**7).round().astype(int).apply(lambda x: f"{x:,} Cr")
        df_state["Trans_count"] = df_state["Transaction_count"].astype(int).apply(lambda x: f"{x:,}")

        fig = px.choropleth(
            df_state,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Transaction_count',
            hover_name="State",
            hover_data={"Trans_count": True,
                        "Trans_amount": True,
                        "Transaction_count": False,
                        "Transaction_amount": False},  
            color_continuous_scale='Reds'
            )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # ------------------------------
    # Categories with sorted transaction counts
    # ------------------------------

        st.subheader("📂 Categories")

        cat_query = f"""
                SELECT Transaction_type,
                    SUM(Transaction_count) AS Transaction_count,
                    SUM(Transaction_amount) AS Transaction_amount
                    FROM aggregate_transaction
                WHERE Year = '{year}' AND Quarter = {quarter}
                {"AND State = '" + selected_state + "'" if selected_state != "All India" else ""}
                GROUP BY Transaction_type
                ORDER BY Transaction_count DESC
        """
        df_cat = pd.read_sql(cat_query, engine)
        df_cat["Transaction_count"] = df_cat["Transaction_count"].astype(int).apply(lambda x: f"{x:,}")
        df_cat.index = range(1, len(df_cat) + 1)
        st.table(df_cat[["Transaction_type", "Transaction_count"]])

        st.subheader("🏆 Top Rankings")
        tab1, tab2, tab3 = st.tabs(["State", "District", "Pin Code"])

        with tab1:
            if selected_state == "All India":
                query_top_states = f"""
                    SELECT State, ROUND(SUM(Transaction_count)/10000000, 2) AS Transaction_count_Cr
                    FROM aggregate_transaction
                    WHERE Year = '{year}' AND Quarter = {quarter}
                    GROUP BY State
                    ORDER BY Transaction_count_Cr DESC
                    LIMIT 10
                """
            else:
                query_top_states = f"""
                    SELECT State, ROUND(SUM(Transaction_count)/10000000, 2) AS Transaction_count_Cr
                    FROM aggregate_transaction
                    WHERE Year = '{year}' AND Quarter = {quarter}
                    AND State = '{selected_state}'
                    GROUP BY State
                """
    
            top_states = pd.read_sql(query_top_states, engine)
            top_states["Transaction_count_Cr"] = top_states["Transaction_count_Cr"].apply(lambda x: f"{x:.2f} Cr")
            top_states.index = range(1, len(top_states) + 1)
            st.table(top_states)

        with tab2:
            district_rank_query = f"""
                SELECT State,
                REPLACE(District, ' district', '') AS District,
                    SUM(Transaction_count)/1e7 AS Transaction_count_Cr
                FROM map_transaction
                WHERE Year = '{year}' AND Quarter = {quarter}
                {"AND State = '" + selected_state + "'" if selected_state != "All India" else ""}
                GROUP BY State, District
                ORDER BY Transaction_count_Cr DESC
                LIMIT 10
            """
            top_districts = pd.read_sql(district_rank_query, engine)
            top_districts["District"] = top_districts["District"].str.title()
            top_districts["Transaction_count_Cr"] = top_districts["Transaction_count_Cr"].apply(lambda x: f"{x:,.2f} Cr")
            top_districts.index = range(1, len(top_districts) + 1)
            st.table(top_districts)

        with tab3:
            pin_rank_query = f"""
                SELECT State,
                    Pincode,
                    SUM(Transaction_count)/1e7 AS Transaction_count_Cr
                FROM top_transaction
                WHERE Year = '{year}' AND Quarter = {quarter}
                {"AND State = '" + selected_state + "'" if selected_state != "All India" else ""}
                GROUP BY State, Pincode
                ORDER BY Transaction_count_Cr DESC
                LIMIT 10
            """
            top_pins = pd.read_sql(pin_rank_query, engine)
            top_pins["Transaction_count_Cr"] = top_pins["Transaction_count_Cr"].apply(lambda x: f"{x:,.2f} Cr")
            top_pins.index = range(1, len(top_pins) + 1)
            st.table(top_pins)
    
    else:
        query_users = f"""
            SELECT State, SUM(Registered_User) AS Registered_User, SUM(App_Opens) AS App_Opens
            FROM aggregate_user
            WHERE Year = '{year}' AND Quarter = {quarter}
            {"AND State='" + selected_state + "'" if selected_state != "All India" else ""}
            GROUP BY State
        """
        df_filtered1 = pd.read_sql(query_users, engine)

        if selected_state == "All India":
            reg_users = df_filtered1["Registered_User"].sum()
            app_opens = df_filtered1["App_Opens"].sum()
        else:
            reg_users = df_filtered1["Registered_User"].iloc[0]
            app_opens = df_filtered1["App_Opens"].iloc[0]

        c1, c2 = st.columns(2)
        c1.metric("Registered PhonePe users", f"{reg_users:,.0f}")
        c2.metric("PhonePe app opens", f"{app_opens:,.0f}")

        st.subheader("📍 Users by State")
        query_users = f"""
            SELECT State, SUM(Registered_User) AS Registered_User, SUM(App_Opens) AS App_Opens
            FROM aggregate_user
            WHERE Year = '{year}' AND Quarter = {quarter}
            {"AND State = '" + selected_state + "'" if selected_state != "All India" else ""}
            GROUP BY State
        """
        df_state1 = pd.read_sql(query_users, engine)
        df_state1["Regd_User"] = df_state1["Registered_User"].astype(int).apply(lambda x: f"{x:,}")
        df_state1["App_Open"] = df_state1["App_Opens"].astype(int).apply(lambda x: f"{x:,}")

        fig1 = px.choropleth(
            df_state1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Registered_User',
            hover_name="State",
            hover_data={"Regd_User": True,
                "App_Open": True,   
                "Registered_User": False,      
                "App_Opens": False },     
            color_continuous_scale='Reds'
            )
        fig1.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("🏆 Top Rankings")
        tab1, tab2,tab3 = st.tabs(["State","District", "Pin Code"])

        with tab1:
            if selected_state == "All India":
                query = f"""
                    SELECT State, SUM(Registered_User) AS Registered_User
                    FROM aggregate_user
                    WHERE Year = '{year}' AND Quarter = {quarter}
                    GROUP BY State
                    ORDER BY Registered_User DESC
                    LIMIT 10
                """
                df_top_states = pd.read_sql(query, engine)
            else:
                query = f"""
                    SELECT State, SUM(Registered_User) AS Registered_User
                    FROM aggregate_user
                    WHERE Year = '{year}' AND Quarter = {quarter} AND State = '{selected_state}'
                    GROUP BY State
                """
                df_top_states = pd.read_sql(query, engine)

            df_top_states["Registered_User_Cr"] = df_top_states["Registered_User"].apply(lambda x: f"{x / 1e7:.2f} Cr")

            st.table(df_top_states[["State", "Registered_User_Cr"]])

        with tab2:
            query_top_districts = f"""
                SELECT State, REPLACE(District, ' district','') AS District, SUM(Registered_User) AS Registered_User
                FROM map_user
                WHERE Year = '{year}' AND Quarter = {quarter}
                {"AND State='"+selected_state+"'" if selected_state!="All India" else ""}
                GROUP BY State, District
                ORDER BY SUM(Registered_User) DESC
                LIMIT 10
            """
            top_districts = pd.read_sql(query_top_districts, engine)
            top_districts["Registered_User"] = top_districts["Registered_User"].apply(lambda x: f"{x/1e7:.2f} Cr" if x >= 1e7 else f"{x/1e5:.2f} L")
            top_districts.index = range(1, len(top_districts) + 1)
            st.table(top_districts)

        with tab3:
            query_top_pins = f"""
                SELECT State, Pincode, SUM(Registered_User) AS Registered_User
                FROM top_user
                WHERE Year = '{year}' AND Quarter = {quarter}
                {"AND State='"+selected_state+"'" if selected_state!="All India" else ""}
                GROUP BY State, Pincode
                ORDER BY SUM(Registered_User) DESC
                LIMIT 10
            """
            top_pins = pd.read_sql(query_top_pins, engine)
            top_pins["Registered_User"] = top_pins["Registered_User"].apply(lambda x: f"{x/1e7:.2f} Cr" if x >= 1e7 else f"{x/1e5:.2f} L")
            top_pins.index = range(1, len(top_pins) + 1)
            st.table(top_pins)

elif page=="Analysis":
    years = pd.read_sql("SELECT DISTINCT Year FROM aggregate_transaction ORDER BY Year", engine)["Year"].tolist()
    quarters = pd.read_sql("SELECT DISTINCT Quarter FROM aggregate_transaction ORDER BY Quarter", engine)["Quarter"].tolist()
    states = pd.read_sql("SELECT DISTINCT State FROM aggregate_transaction ORDER BY State", engine)["State"].tolist()
    
    st.title("PHONE TRANSACTION INSIGHTS")
    scenario=st.selectbox("Choose a scenario",["Decoding Transaction Dynamics on PhonePe","Device Dominance and User Engagement Analysis","Insurance Penetration and Growth Potential Analysis",
                                      "Transaction Analysis for Market Expansion","User Engagement and Growth Strategy"])
    if scenario=="Decoding Transaction Dynamics on PhonePe":
        st.header("Statewise Transaction Analysis")
        sel_state=st.selectbox("Choose a State",states)
        c1,c2=st.columns(2)
        query_11 = f"""SELECT Year, 
                    SUM(Transaction_count) AS Total_Transactions, 
                    SUM(Transaction_amount) AS Total_Amount
                    FROM aggregate_transaction
                    WHERE State = '{sel_state}'
                    GROUP BY Year
                    ORDER BY Year"""
        df_txn_11 = pd.read_sql(query_11, engine)

        df_txn_11["Year"] = df_txn_11["Year"].astype(int)

        with c1:
            st.subheader("Total Transaction over Years")
            fig1=px.line(df_txn_11,x="Year",y="Total_Transactions",markers=True)
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            st.subheader("Total Transaction Amount Over Years")
            fig2 = px.line(df_txn_11, x="Year", y="Total_Amount", markers=True)
            st.plotly_chart(fig2, use_container_width=True)
        
        st.header("Payment Categorywise Performance")
        c1,c2=st.columns(2)
        query_12 = f"""SELECT Year,Quarter, 
                    SUM(Transaction_count) AS Total_Transactions, 
                    SUM(Transaction_amount) AS Total_Amount
                    FROM aggregate_transaction
                    WHERE State = '{sel_state}'
                    GROUP BY Year,Quarter
                    ORDER BY Year,Quarter"""
        df_txn_12 = pd.read_sql(query_12, engine)

        df_txn_12["Year_Quarter"]=df_txn_12["Year"].astype(str)+"-Q"+df_txn_12["Quarter"].astype(str)

        with c1:
            st.subheader("Total Transaction Count over the Quarters")
            fig3=px.area(df_txn_12,x="Year_Quarter",y="Total_Transactions",markers=True)
            st.plotly_chart(fig3, use_container_width=True)
        
        with c2:
            st.subheader("Total Transaction Amount over the Quarters")
            fig4=px.area(df_txn_12,x="Year_Quarter",y="Total_Amount",markers=True)
            st.plotly_chart(fig4, use_container_width=True)

        st.header("Categorywise Performance Trend")
        c1,c2=st.columns(2)
        query_13 = f"""SELECT Transaction_type, 
                    SUM(Transaction_count) AS Total_Transactions, 
                    SUM(Transaction_amount) AS Total_Amount
                    FROM aggregate_transaction
                    WHERE State = '{sel_state}'
                    GROUP BY Transaction_type
                    ORDER BY Transaction_type"""
        df_txn_13 = pd.read_sql(query_13, engine)

        with c1:
            st.subheader("Categorywise transaction count")
            fig5=px.bar(df_txn_13,x="Transaction_type",y="Total_Transactions",text_auto=True)
            st.plotly_chart(fig5, use_container_width=True)
        
        with c2:
            st.subheader("Categorywise transaction amount")
            fig6=px.bar(df_txn_13,x="Transaction_type",y="Total_Amount",text_auto=True)
            st.plotly_chart(fig6, use_container_width=True)

        st.header("YoY Growth")
        query_14 = f"""SELECT Year,
                    SUM(Transaction_count) AS Total_Transactions, 
                    SUM(Transaction_amount) AS Total_Amount
                    FROM aggregate_transaction
                    WHERE State = '{sel_state}'
                    GROUP BY Year
                    ORDER BY Year"""
        df_txn_14 = pd.read_sql(query_14, engine)
        df_txn_14["YoY_Growth%(Count)"] = df_txn_14["Total_Transactions"].pct_change() * 100
        df_txn_14["YoY_Growth%(Amount)"] = df_txn_14["Total_Amount"].pct_change() * 100

        fig7=px.bar(df_txn_14,x="Year",y="YoY_Growth%(Amount)",text_auto=True)
        st.plotly_chart(fig7, use_container_width=True)

        st.header("🏆 Top 5 States by Transaction Value (Latest Quarter)")
        query_15 = """
                SELECT Year, Quarter 
                FROM aggregate_transaction
                ORDER BY Year DESC, Quarter DESC
                LIMIT 1
                """
        latest = pd.read_sql(query_15, engine).iloc[0]
        latest_year, latest_quarter = latest["Year"], latest["Quarter"]

        query_top_15 = f"""
                SELECT State, SUM(Transaction_amount) AS Total_Amount
                FROM aggregate_transaction
                WHERE Year = {latest_year} AND Quarter = {latest_quarter}
                GROUP BY State
                ORDER BY Total_Amount DESC
                LIMIT 5
        """
        df_txn_15 = pd.read_sql(query_top_15,engine)

        fig8 = px.bar(df_txn_15, x="State", y="Total_Amount",text_auto=True)
        st.plotly_chart(fig8, use_container_width=True)

    elif scenario=="Device Dominance and User Engagement Analysis":
        st.header("Top Device Brands by Total Registered Users (Nationwide)")

        query_21=f"""SELECT Brand, SUM(User_Count) AS Total_Users
            FROM aggregate_user_device
            GROUP BY Brand
            ORDER BY Total_Users DESC
            LIMIT 10;
        """
        df_txn_21=pd.read_sql(query_21,engine)

        fig1=px.bar(df_txn_21, x="Brand", y="Total_Users",text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)

        st.header("Yearly Trend of Top Device Brands")

        query_22=f"""SELECT Year, Brand, SUM(User_Count) AS Total_Users
            FROM aggregate_user_device
            GROUP BY Year, Brand
            ORDER BY Year, Total_Users DESC;
        """
        df_txn_22=pd.read_sql(query_22,engine)

        fig2=px.line(df_txn_22, x="Year", y="Total_Users", color="Brand",markers=True)
        st.plotly_chart(fig2, use_container_width=True)

        st.header("Device Dominance by State")
        sel_state=st.selectbox("Choose a State",states)
        query_23=f"""SELECT State, Brand, SUM(User_Count) AS Total_Users
            FROM aggregate_user_device
            WHERE State='{sel_state}'
            GROUP BY State, Brand
            ORDER BY State, Total_Users DESC;
        """
        df_txn_23=pd.read_sql(query_23,engine)

        fig3=px.bar(df_txn_23, x="Brand", y="Total_Users", color="Brand",text_auto=True)
        st.plotly_chart(fig3,use_container_width=True)

        st.header("Engagement Ratio (App Opens vs Registered Users per State)")
        query_24=f"""SELECT State, 
            SUM(App_Opens) AS Total_AppOpens, 
            SUM(Registered_User) AS Total_Registered,
            (SUM(App_Opens) / SUM(Registered_User)) AS Engagement_Ratio
            FROM aggregate_user
            GROUP BY State
            ORDER BY Engagement_Ratio DESC;
        """
        df_txn_24=pd.read_sql(query_24,engine)

        fig4 = px.choropleth(df_txn_24, 
                             geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey="properties.ST_NM",
                            locations="State", color="Engagement_Ratio",
                            color_continuous_scale="Viridis")
        fig4.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig4)

        st.header("Underutilized Devices (High Users, Low Engagement)")
        query_25=f"""SELECT aud.Brand,
            SUM(aud.User_Count) AS Total_Users,
            SUM(au.App_Opens) AS Total_AppOpens,
            (SUM(au.App_Opens) / SUM(aud.User_Count)) AS AppOpens_Per_User
            FROM aggregate_user_device aud
            JOIN aggregate_user au 
            ON aud.State = au.State 
            AND aud.Year = au.Year 
            AND aud.Quarter = au.Quarter
            GROUP BY aud.Brand
            ORDER BY AppOpens_Per_User ASC
            LIMIT 10;
        """
        df_txn_25 = pd.read_sql(query_25, engine)

        fig5 = px.scatter(df_txn_25, x="Total_Users", y="AppOpens_Per_User",
                  size="Total_Users", color="Brand",
                  title="Underutilized Devices (App Opens per User)",
                  hover_data=["Total_AppOpens"])
        st.plotly_chart(fig5)

    elif scenario=="Insurance Penetration and Growth Potential Analysis":
        st.header("Total Insurance Transaction Over the Years")
        sel_state=st.selectbox("Choose a State",states)
        c1,c2=st.columns(2)
        query_31 = f"""SELECT Year, 
            SUM(Transaction_count) AS Total_Transactions,
            SUM(Transaction_amount) AS Total_Amount
            FROM aggregate_insurance
            GROUP BY Year
            ORDER BY Total_Amount DESC;
        """
        df_txn_31 = pd.read_sql(query_31, engine)

        df_txn_31["Year"] = df_txn_31["Year"].astype(int)

        with c1:
            st.subheader("Total Transaction over Years")
            fig1=px.line(df_txn_31,x="Year",y="Total_Transactions",markers=True)
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            st.subheader("Total Transaction Amount Over Years")
            fig2 = px.line(df_txn_31, x="Year", y="Total_Amount", markers=True)
            st.plotly_chart(fig2, use_container_width=True)

        st.header("Total Insurance Transaction Amount by State")
        query_32=f"""SELECT State, SUM(Transaction_amount) AS Total_Amount
            FROM aggregate_insurance
            GROUP BY State
            ORDER BY Total_Amount DESC;
        """
        df_txn_32 = pd.read_sql(query_32,engine)

        fig3 = px.bar(df_txn_32, x="State", y="Total_Amount",color="Total_Amount", text_auto=True)
        st.plotly_chart(fig3)

        st.header("Top 10 States Contributing to Insurance Premium Collections")
        query_33=f"""SELECT State, SUM(Transaction_amount) AS Premium_Collection
            FROM aggregate_insurance
            GROUP BY State
            ORDER BY Premium_Collection DESC
            LIMIT 10;
        """
        df_txn_33=pd.read_sql(query_33,engine)

        fig4 = px.bar(df_txn_33, x="State", y="Premium_Collection",color="Premium_Collection", text_auto=True)
        st.plotly_chart(fig4)

        st.header("Quarterly Insurance Transaction Trend")
        query_34=f"""SELECT 
            Year,
            Quarter,
            SUM(Transaction_amount) AS Total_Insurance_Amount
            FROM aggregate_insurance
            WHERE State = '{sel_state}'
            GROUP BY Year, Quarter
            ORDER BY Year, Quarter;
        """
        df_txn_34 = pd.read_sql(query_34, engine)

        fig5 = px.line(df_txn_34, x="Quarter", y="Total_Insurance_Amount",color="Year", markers=True)
        st.plotly_chart(fig5)

        st.header("YoY Growth Rate of Insurance Transaction")
        query_35 = f"""SELECT Year,
                    SUM(Transaction_amount) AS Total_Amount
                    FROM aggregate_transaction
                    WHERE State = '{sel_state}'
                    GROUP BY Year
                    ORDER BY Year
                """
        df_txn_35 = pd.read_sql(query_35, engine)
        df_txn_35["YoY_Growth%(Amount)"] = df_txn_35["Total_Amount"].pct_change() * 100

        fig6=px.bar(df_txn_35,x="Year",y="YoY_Growth%(Amount)",text_auto=True)
        st.plotly_chart(fig6, use_container_width=True)

    elif scenario == "Transaction Analysis for Market Expansion":
        st.header("Transaction Analysis for Market Expansion")

        query_41 = """
            SELECT Year, 
                SUM(Transaction_count) AS Total_Transactions,
                SUM(Transaction_amount) AS Total_Amount
            FROM map_transaction
            GROUP BY Year
            ORDER BY Year;
        """
        df_txn_41 = pd.read_sql(query_41, engine)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Total Transactions Over Years")
            fig1 = px.line(df_txn_41, x="Year", y="Total_Transactions", markers=True)
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            st.subheader("Total Transaction Amount Over Years")
            fig2 = px.line(df_txn_41, x="Year", y="Total_Amount", markers=True)
            st.plotly_chart(fig2, use_container_width=True)

        st.header("Top 10 States by Transaction Amount")
        query_42 = """
            SELECT State, SUM(Transaction_amount) AS Total_Amount
            FROM map_transaction
            GROUP BY State
            ORDER BY Total_Amount DESC
            LIMIT 10;
        """
        df_txn_42 = pd.read_sql(query_42, engine)

        fig3 = px.bar(df_txn_42, x="State", y="Total_Amount", color="Total_Amount", text_auto=True)
        st.plotly_chart(fig3, use_container_width=True)

        st.header("Top Districts by Transaction Amount")
        sel_state=st.selectbox("Choose a State",states)

        query_43 = f"""
            SELECT District, SUM(Transaction_amount) AS Total_Amount
            FROM map_transaction
            WHERE State = '{sel_state}'
            GROUP BY District
            ORDER BY Total_Amount DESC
            LIMIT 10;
        """
        df_txn_43 = pd.read_sql(query_43, engine)

        fig4 = px.bar(df_txn_43, x="District", y="Total_Amount", color="Total_Amount", text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)

        st.header("YoY Growth of Transaction Amount by State")
        query_44 = """
            SELECT State, Year, SUM(Transaction_amount) AS Total_Amount
            FROM map_transaction
            GROUP BY State, Year
            ORDER BY State, Year;
        """
        df_txn_44 = pd.read_sql(query_44, engine)

        df_txn_44["YoY_Growth%"] = df_txn_44.groupby("State")["Total_Amount"].pct_change() * 100

        fig5 = px.line(df_txn_44, x="Year", y="YoY_Growth%", color="State", markers=True)
        st.plotly_chart(fig5, use_container_width=True)

        st.header("State-wise Market Share of Transactions")
        query_45 = """
            SELECT State, SUM(Transaction_amount) AS Total_Amount
            FROM map_transaction
            GROUP BY State
            ORDER BY Total_Amount DESC;
        """
        df_txn_45 = pd.read_sql(query_45, engine)

        fig6 = px.pie(df_txn_45, names="State", values="Total_Amount", hole=0.4,
                    title="State-wise Market Share of Transaction Amount")
        st.plotly_chart(fig6, use_container_width=True)

    else:
        st.header("User Engagement and Growth Strategy")

        query_51 = """
            SELECT Year, 
                SUM(Registered_User) AS Total_Users
            FROM map_user
            GROUP BY Year
            ORDER BY Year;
        """
        df_user_51 = pd.read_sql(query_51, engine)
        df_user_51["YoY_Growth%"] = df_user_51["Total_Users"].pct_change() * 100

        st.subheader("Growth of Registered Users Over Years")
        fig1 = px.line(df_user_51, x="Year", y="Total_Users", markers=True, title="Registered Users Growth")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("YoY Growth % - Registered Users")
        fig1b = px.bar(df_user_51, x="Year", y="YoY_Growth%", text_auto=True, title="YoY Growth of Users")
        st.plotly_chart(fig1b, use_container_width=True)

        query_52 = """
            SELECT Year, 
                SUM(App_Opens) AS Total_AppOpens
            FROM map_user
            GROUP BY Year
            ORDER BY Year;
        """
        df_user_52 = pd.read_sql(query_52, engine)
        df_user_52["YoY_Growth%"] = df_user_52["Total_AppOpens"].pct_change() * 100

        st.subheader("Growth of App Opens Over Years")
        fig2 = px.line(df_user_52, x="Year", y="Total_AppOpens", markers=True, title="App Opens Growth")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("YoY Growth % - App Opens")
        fig2b = px.bar(df_user_52, x="Year", y="YoY_Growth%", text_auto=True, title="YoY Growth of App Opens")
        st.plotly_chart(fig2b, use_container_width=True)

        query_53 = """
            SELECT State, 
                SUM(App_Opens) AS Total_AppOpens,
                SUM(Registered_User) AS Total_Users,
                ROUND(SUM(App_Opens) * 1.0 / SUM(Registered_User), 2) AS Engagement_Ratio
            FROM map_user
            GROUP BY State
            ORDER BY Engagement_Ratio DESC;
        """
        df_user_53 = pd.read_sql(query_53, engine)

        st.subheader("State-wise Engagement Ratio (App Opens per User)")
        fig3 = px.bar(df_user_53, x="State", y="Engagement_Ratio", color="Engagement_Ratio", text_auto=True)
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("Top Districts by Registered Users")


        sel_state=st.selectbox("Choose a State",states)

        query_54 = f"""
            SELECT District, SUM(Registered_User) AS Total_Users
            FROM map_user
            WHERE State = '{sel_state}'
            GROUP BY District
            ORDER BY Total_Users DESC
            LIMIT 10;
        """
        df_user_54 = pd.read_sql(query_54, engine)

        fig4 = px.bar(df_user_54, x="District", y="Total_Users", color="Total_Users", text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)

        query_55 = """
            SELECT Year || '-Q' || Quarter AS Year_Quarter,
                SUM(Registered_User) AS Total_Users,
                SUM(App_Opens) AS Total_AppOpens
            FROM map_user
            GROUP BY Year, Quarter
            ORDER BY Year, Quarter;
        """
        df_user_55 = pd.read_sql(query_55, engine)

        st.subheader("Quarterly User Engagement Trend")
        fig5 = px.line(df_user_55, x="Year_Quarter", y="Total_AppOpens", markers=True, title="App Opens Trend")
        fig6 = px.line(df_user_55, x="Year_Quarter", y="Total_Users", markers=True, title="Registered Users Trend")

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(fig5, use_container_width=True)
        with c2:
            st.plotly_chart(fig6, use_container_width=True)

else:
    st.subheader("Developed by: Priya Roshini S")

    st.subheader("Skills: Python, SQL, Data Analysis,Streamlit, Pandas")


