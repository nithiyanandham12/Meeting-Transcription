import streamlit as st

# Define the company logo and app details
company_logo = "sba.jpg"  # Replace with the path to your company logo
app_details = [
    {"logo": "_8fd6e0cf-fde4-4843-8edd-a64337932233.jpg", "name": "PDF URL ANALYZER", "link": "http://link_to_app1.com"},
    {"logo": "_55bc0b3f-2019-494c-9978-bbb0129a11d8.jpg", "name": "AUDIO ANALYZER", "link": "http://link_to_app2.com"},
    {"logo": "_67719771-fafa-467e-b2f8-557b229d48fc.jpg", "name": "MEETING TRANSCRIPTION", "link": "http://link_to_app3.com"},
    {"logo": "_8590e2f5-3550-4dfd-be77-1606a13e4a34.jpg", "name": "SPEECH TO TEXT", "link": "http://link_to_app4.com"},
]

# Set the page layout
st.set_page_config(layout="wide")

# Sidebar with company logo and name
st.sidebar.image(company_logo, use_column_width=True)
st.sidebar.title("SBA INFO SOLUTIONS")

# Main area with app logos, names, and launch buttons
cols = st.columns(4)

for col, app in zip(cols, app_details):
    with col:
        st.image(app["logo"], use_column_width=True)
        st.write(f"**{app['name']}**")
        if st.button("Launch", key=app['name']):
            st.write(f"Redirecting to {app['link']}...")
            st.markdown(f'<meta http-equiv="refresh" content="0; url={app["link"]}">', unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    st.title("Home Screen")
