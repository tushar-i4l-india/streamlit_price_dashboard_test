import streamlit as st # type: ignore
import pandas as pd # type: ignore
import importlib.util
import plotly.express as px # type: ignore

st.set_page_config(page_title="Competitor Price Comparison Dashboard", layout="wide", menu_items={'Get Help': 'https://www.extremelycoolapp.com/help', 
                                                                                                  'Report a bug': "https://www.extremelycoolapp.com/bug", 
                                                                                                  'About': "# This is a header. This is an *extremely* cool app!"})

st.title("Competitor Price Comparison Dashboard 💷")
script_options = {
    "Celotex": "Final_Celotex_Prices.py",
    "Recticel": "Final_Recticel_Prices.py",
    "Knauf": "script3.py"
}
selected_script = st.selectbox("Select a Brand", list(script_options.keys()))

@st.cache_data
def run_script(script_path):
    spec = importlib.util.spec_from_file_location("dynamic_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "result_df") and isinstance(module.result_df, pd.DataFrame):
        return module.result_df
    else:
        return None  
    
df = pd.DataFrame()
if st.button("Run Script"):
    script_path = script_options[selected_script]
    df = run_script(script_path)
    if df is not None:
        st.session_state["df"] = df  # Store DataFrame in session state
        st.session_state["script_ran"] = True  # Mark script as executed

# Check if DataFrame exists in session state
if "df" in st.session_state and st.session_state["script_ran"]:
    df = st.session_state["df"]  # Retrieve stored DataFrame

    st.write(f"### Output of `{selected_script}`")
    st.dataframe(df, hide_index=True)

    products = df["Product"].unique()
    selected_product = st.selectbox("Select a Product:", products)

    filtered_product = df[df["Product"] == selected_product]

    if not filtered_product.empty:
        melted_data = filtered_product.melt(id_vars=["Product", "SKU"], var_name="Competitor", value_name="Price")
        st.write(f"Showing price comparison for **{selected_product}**:")
        # melted_data["Price"] = melted_data["Price"].replace({'[£,]': '', 'Price Not Found': '0'}, regex=True).astype(float)
        melted_data["Price"] = melted_data["Price"].replace({'[£,]': '', 'Price Not Found': '0'}, regex=True)
        melted_data["Price"] = pd.to_numeric(melted_data["Price"], errors='coerce')
        melted_data = melted_data.dropna(subset=["Price"])
        melted_data.sort_values(by = "Price", ascending= True, inplace = True)
        
        fig = px.bar(
            melted_data,
            x="Competitor",
            y="Price",
            color="Competitor",
            title=f"Price Comparison for {selected_product}",
            text = "Price",
            # barmode="group"
        )
        st.plotly_chart(fig)
        st.dataframe(melted_data, hide_index=True)
    else:
        st.write("No data available for this product.")