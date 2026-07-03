import streamlit as st
from tickets_database import fetch_all_tickets, update_ticket_solution

# --- CONFIGURATION SETTINGS ---
# Set up your static administrative login email here
ADMIN_EMAIL_CREDENTIAL = "admin@system.com"

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Support Admin Control Panel",
    page_icon="🛠️",
    layout="wide"
)

# Initialize login session state tracking variable
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# --- SCREEN CONTROLLER ROUTER ---
if not st.session_state.admin_logged_in:
    # --- RENDER THE LOCK SCREEN INTERFACE ---
    _, center_col, _ = st.columns()
    
    with center_col:
        st.write("\n\n")
        st.markdown("<h2 style='text-align: center;'>🔐 Administrator Gateway</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Enter your admin email to view and resolve tickets.</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            input_email = st.text_input("Administrative Email Address", placeholder="admin@system.com")
            
            st.write("")
            if st.button("Unlock Admin Dashboard", type="primary", use_container_width=True):
                # Verify only the email identifier
                if input_email == ADMIN_EMAIL_CREDENTIAL:
                    st.session_state.admin_logged_in = True
                    st.success("Identity Verified. Loading internal structures...")
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid email identifier.")

else:
    # --- RENDER THE UNLOCKED ADMINISTRATIVE DASHBOARD ---
    col_title, col_logout = st.columns()
    with col_title:
        st.title("🛠️ Support System - Admin Control Panel")
        st.markdown("Review submitted system bugs, analyze user source code, and deploy resolutions directly to client dashboards.")
    with col_logout:
        st.write("\n\n")
        if st.button("🔴 Close Admin Session", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()
            
    st.write("---")

    # Fetch all current tickets across the system database row arrays
    all_tickets = fetch_all_tickets()

    if not all_tickets:
        st.info("🎈 Excellent work! No tickets have been submitted to the database yet.")
    else:
        # Separate structural data records dynamically based on status
        open_tickets = [t for t in all_tickets if t[5] == "Open"]
        resolved_tickets = [t for t in all_tickets if t[5] == "Resolved"]
        
        # Display high-level metric boards
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric(label="⚠️ Pending Action (Open)", value=len(open_tickets))
        with metric_col2:
            st.metric(label="✅ Completed (Resolved)", value=len(resolved_tickets))
            
        st.write("---")
        st.subheader("📬 Incoming Tickets Queue")
        
        if not open_tickets:
            st.success("🎉 All tickets have been cleared and resolved!")
        else:
            for ticket in open_tickets:
                t_id, t_name, t_email, t_title, t_code, t_status, t_solution = ticket
                
                # Render each open incident inside an isolated border card
                with st.container(border=True):
                    col_info, col_action = st.columns()
                    
                    with col_info:
                        st.markdown(f"### Ticket #{t_id}: **{t_title}**")
                        st.markdown(f"**Submitted By:** {t_name} (`{t_email}`)")
                        
                        st.markdown("**User's Problem Code Snippet:**")
                        st.code(t_code, language="python")
                    
                    with col_action:
                        st.markdown("#### 💡 Provide Resolution")
                        
                        solution_input = st.text_area(
                            "Type your solution details here:",
                            placeholder="e.g., Fix the thread conflict by passing parameters local to your helper functions.",
                            key=f"sol_{t_id}",
                            height=150
                        )
                        
                        if st.button("Submit & Resolve", type="primary", key=f"btn_{t_id}", use_container_width=True):
                            if solution_input.strip() == "":
                                st.error("Please enter a solution script before marking this ticket as complete.")
                            else:
                                # Overwrite status variables in SQLite storage engine
                                update_ticket_solution(t_id, solution_input)
                                st.success(f"Ticket #{t_id} updated!")
                                st.rerun()

        # --- HISTORICAL REVIEWS EXPANDER SECTION ---
        st.write("---")
        with st.expander("📁 View Resolved Ticket Archive", expanded=False):
            if not resolved_tickets:
                st.write("No closed tickets found in history stores.")
            else:
                for ticket in resolved_tickets:
                    t_id, t_name, t_email, t_title, t_code, t_status, t_solution = ticket
                    with st.container(border=True):
                        st.markdown(f"### [RESOLVED] Ticket #{t_id}: {t_title}")
                        st.markdown(f"**Client Profile:** {t_name} ({t_email})")
                        st.markdown(f"**Deployed Resolution:** *{t_solution}*")
