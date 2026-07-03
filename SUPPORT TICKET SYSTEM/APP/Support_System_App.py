import streamlit as st
from DATABASES.user_database import save_user
from DATABASES.tickets_database import init_ticket_db, create_ticket, fetch_user_tickets

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Support Ticket System",
    page_icon="🎫",
    layout="centered"
)

# Initialize Session State memory stores
if "registered" not in st.session_state:
    st.session_state.registered = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "email" not in st.session_state:
    st.session_state.email = ""

# Build/verify the backend tables
init_ticket_db()

st.title("🎫 Smart Support Hub")
st.markdown("Submit your bugs, paste your code snippets, and track ongoing solutions in real-time.")
st.write("---")

# --- SIDEBAR: PROFILE & LOGOUT CONTROLS ---
with st.sidebar:
    st.header("👤 Profile Control Panel")
    
    if not st.session_state.registered:
        st.caption("Please log in to view active tickets.")
        user_name = st.text_input("Full Name", placeholder="John Doe")
        user_email = st.text_input("Email Address", placeholder="john@example.com")
        
        if st.button("Register & Access System", type="primary", use_container_width=True):
            if user_name and user_email:
                save_user(user_name, user_email)
                st.session_state.registered = True
                st.session_state.username = user_name
                st.session_state.email = user_email
                st.rerun()
            else:
                st.error("Please fill in both fields.")
    else:
        # Display the logged-in profile overview
        st.success(f"Active Session:\n\n**{st.session_state.username}**\n\n({st.session_state.email})")
        st.write("---")
        
        # --- THE LOG OUT OPTION ---
        if st.button("🔴 Log Out Account", use_container_width=True):
            # Clear app memory caches completely
            st.session_state.registered = False
            st.session_state.username = ""
            st.session_state.email = ""
            # Wipe everything and lock the tabs instantly
            st.rerun()

# --- MAIN INTERFACE CONTROL ROUTER ---
if not st.session_state.registered:
    st.info("👋 Welcome! Please complete your **Profile Registration** in the left sidebar panel to unlock the support ticket workspace.")
else:
    # --- TOP RIGHT CORNER LOGGED IN USER BRANDING ---
    col_left, col_right = st.columns([3, 1])
    with col_right:
        st.markdown(
            f"<p style='text-align: right; color: #4CAF50; font-weight: bold; margin-bottom: 0px;'>● {st.session_state.username}</p>", 
            unsafe_allow_html=True
        )
    
    # --- MAIN INTERFACE DASHBOARD WORKSPACE ---
    tab1, tab2 = st.tabs(["🚀 Create New Ticket", "🔍 Track My Tickets"])

    # --- TAB 1: TICKET CREATION ENGINE ---
    with tab1:
        st.subheader("Report an Issue")
        
        query = st.text_input(
            'What issue are you facing?', 
            placeholder='e.g., SQLite connection failing inside Streamlit loop'
        )
        
        user_code = st.text_area(
            'Paste Your Python Code Here:', 
            placeholder='# Paste your error-prone code blocks here...',
            height=200
        )
        
        if st.button('Submit Support Ticket', type='primary', use_container_width=True):
            if not query or not user_code:
                st.warning("⚠️ Please provide both an issue description and the relevant code snippet.")
            else:
                create_ticket(st.session_state.username, st.session_state.email, query, user_code)
                st.success('🎉 Your ticket has been logged successfully!')

    # --- TAB 2: USER TICKET TRACKING ENGINE ---
    with tab2:
        st.subheader("Your Active Tickets")
        
        user_tickets = fetch_user_tickets(st.session_state.email)
        
        if user_tickets:
            for ticket in user_tickets:
                t_id, t_title, t_code, t_status, t_solution = ticket
                status_color = "green" if t_status == "Resolved" else "orange"
                
                with st.container(border=True):
                    st.markdown(f"### Ticket #{t_id}: {t_title}")
                    st.markdown(f"**Status:** :{status_color}[{t_status}]")
                    
                    st.markdown("**Submitted Code Snippet:**")
                    st.code(t_code, language="python")
                    
                    st.markdown(f"**💡 Solution:** *{t_solution}*")
        else:
            st.info("No tickets found under your email address yet.")
