# 🎫 The "Please Fix My Code" Hub

A lightweight, dual-app support ticket system built with Python and Streamlit. It uses an SQLite backend that *actually* works across multiple threads without throwing a tantrum.

One side lets desperate users dump their broken code into your lap, and the other side lets you sit in your admin chair, look at their syntax errors, and pass judgment (or solutions).

---

## 🛠️ The Architecture (How it works)

Instead of building a massive enterprise monolith, this project splits the workload into two independent apps sharing a single SQLite database pipeline:

* **User Facing App (`Support_System_App.py`)**: A clean UI where users log in with their email, write their problem, and paste their messy code blocks.
* **Admin Control Panel (`Admin_App.py`)**: A secure wide-screen dashboard for you. Enter the admin email, look at the submitted code snippets with syntax highlighting, and send back solutions.
* **The Shared Brain (`tickets_database.py`)**: Conflict-proof database scripts using `check_same_thread=False` and isolated cursor connections. This stops SQLite from panicking when multi-threaded Streamlit reruns happen.

---

## 🚀 Quick Start

### 1. Install Dependencies
You don't need heavy database engines or servers. Just standard Streamlit.
```bash
pip install streamlit
```

### 2. Fire Up the Systems
Because the apps are decoupled, you need to open two separate terminal windows to run them side-by-side.

**Terminal 1 (For your users):**
```bash
streamlit run Support_System_App.py
```

**Terminal 2 (For you, the savior):**
```bash
streamlit run Admin_App.py
```

---

## 🔑 Access Codes

* **User Access**: Enter any name and email in the sidebar to register and unlock the dashboard.
* **Admin Access**: Open the admin app and use `admin@system.com` to bypass the gateway. No password required (we trust you).

---

## 🧠 Why is the database designed this way?

You might notice the Admin Panel never queries a `user_database`. Why? Because when a user creates a ticket, their username and email are stamped directly onto the bug report row. 

It keeps the code incredibly fast, leaves a permanent historical record of who broke what, and means you only have to look at **one** table to fix the world.

---

## 🛑 Pro-Tip For Testing
Streamlit is stateless and updates on page refresh. When you submit a solution in the Admin App, just click back over to the User App and click any tab or button to watch the solution instantly pop up in beautiful formatting. 
