# ------------------------------
# 3. DATA RETRIEVAL FROM SQL
# ------------------------------
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:Welcome123@127.0.0.1:3306/phonepe')

# ------------------------------
# 4. STREAMLIT HOME PAGE CONFIGURATION
# ------------------------------

st.set_page_config(page_title="📊 PhonePe Pulse Dashboard", layout="wide")
st.title("📊 PhonePe Pulse Dashboard")
st.markdown("Explore Digital Transactions, Users & Insurance Data Across India")

st.sidebar.header("Navigation")
page=st.sidebar.radio("Select a page",["Home","Analysis"])
st.sidebar.subheader("🔍 Filters")
if page=="Home":
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

else:

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
            SELECT CONCAT(Year, '-Q', Quarter) AS Year_Quarter,
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