import streamlit as st
import requests
from datetime import datetime
import time

# Configuration
API_URL = "http://backend:8000"
TIMEOUT = 5

# Page config
st.set_page_config(
    page_title="Task Manager",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add Tailwind CSS
st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.3s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def make_api_request(method, endpoint, **kwargs):
    """Make API request with error handling"""
    try:
        url = f"{API_URL}{endpoint}"
        response = requests.request(method, url, timeout=TIMEOUT, **kwargs)
        response.raise_for_status()
        return response.json() if method.lower() == 'get' else response
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to the backend. Please ensure the server is running.")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ Server error: {e}")
        return None
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")
        return None

# Initialize session state
if 'task_count' not in st.session_state:
    st.session_state.task_count = 0

# Header
st.markdown("""
    <div class="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl shadow-xl p-8 mb-8 fade-in">
        <h1 class="text-white text-4xl font-bold text-center mb-2">✅ Task Manager</h1>
        <p class="text-blue-100 text-center text-lg">Organize your tasks efficiently and stay productive</p>
    </div>
""", unsafe_allow_html=True)

# Add task section
st.markdown('<div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 mb-6 fade-in">', unsafe_allow_html=True)
st.markdown('<h2 class="text-2xl font-semibold text-slate-800 mb-4">📝 Add New Task</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    task = st.text_input(
        "Task description",
        placeholder="Enter your task here...",
        label_visibility="collapsed"
    )

with col2:
    add_button = st.button("➕ Add Task", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
# Handle add task
if add_button:
    if task.strip():
        with st.spinner("Adding task..."):
            # Send correct JSON to FastAPI
            response = make_api_request('post', '/tasks', json={"title": task})
            if response:
                st.success("✅ Task added successfully!")
                st.session_state.task_count += 1
                time.sleep(0.5)
                st.rerun()
    else:
        st.warning("⚠️ Please enter a task description")

# Fetch tasks
with st.spinner("Loading tasks..."):
  # Fetch tasks
    tasks = make_api_request('get', '/tasks')

st.markdown('<div class="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 fade-in">', unsafe_allow_html=True)
st.markdown('<h2 class="text-2xl font-semibold text-slate-800 mb-6">📋 Your Tasks</h2>', unsafe_allow_html=True)

if tasks and len(tasks) > 0:
    for t in tasks:
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            st.write(t["title"])

        with col2:
            if st.button("🗑 Delete", key=f"delete-{t['id']}"):
                make_api_request("delete", f"/tasks/{t['id']}")
                st.rerun()
        

else:
    st.markdown("""
        <div class="text-center py-12">
            <div class="text-6xl mb-4">📭</div>
            <h3 class="text-2xl font-semibold text-slate-700 mb-2">No tasks yet</h3>
            <p class="text-slate-500">Add your first task to get started!</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
