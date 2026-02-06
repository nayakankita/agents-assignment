import streamlit as st
from datetime import datetime

# Import your router / graph entrypoint
# Change these imports based on your actual code
from router_graph import build_graph  # or from router_graph import router_graph

st.set_page_config(page_title="Multi-Agent RAG + Coding Demo", layout="wide")

st.title("Multi-Agent AI System (RAG + Coding Agents)")
st.caption("LangGraph router → RAG agent OR coding agents (generate code → execute → retry on error).")

# Sidebar: config / debug controls
with st.sidebar:
    st.header("Settings")
    debug = st.checkbox("Show debug logs", value=True)
    st.divider()
    st.write("Tip: Keep this ON for evaluation screenshots.")

# Build graph once (cache)
@st.cache_resource
def get_graph():
    return build_graph()   # change if your function is different

graph = get_graph()

# Main input
question = st.text_area("Ask a question:", height=100, placeholder="e.g., Summarize PTO policy OR write code to calculate mean from sample data")

col1, col2 = st.columns([1, 1])
with col1:
    run_btn = st.button("Run", type="primary")
with col2:
    clear_btn = st.button("Clear")

if clear_btn:
    st.session_state.clear()
    st.rerun()

# Output area
if run_btn and question.strip():
    with st.spinner("Running agents..."):
        start = datetime.now()

        # Invoke graph.
        # Common patterns:
        # result = graph.invoke({"question": question})
        # result = graph.invoke({"input": question})
        result = graph.invoke({"question": question, "debug": debug})  # adjust to your graph state schema

        elapsed = (datetime.now() - start).total_seconds()

    st.success(f"Done in {elapsed:.2f}s")

    # ---- Expected result structure (example) ----
    # result = {
    #   "route": "rag" or "code",
    #   "final_answer": "...",
    #   "sources": [...],
    #   "generated_code": "...",
    #   "execution_output": "...",
    #   "error_log": [...],
    #   "debug_log": [...]
    # }

    route = result.get("route", "unknown")
    st.subheader("Router Decision")
    st.write(f"**Route:** `{route}`")

    # Tabs for clean presentation
    tab1, tab2, tab3 = st.tabs(["Final Answer", "Evidence / Logs", "Code (if any)"])

    with tab1:
        st.markdown(result.get("final_answer", "No answer returned."))

    with tab2:
        if route == "rag":
            st.write("### Sources / Citations")
            sources = result.get("sources", [])
            if sources:
                for s in sources:
                    st.write(f"- {s}")
            else:
                st.info("No sources returned.")
        else:
            st.write("### Execution Logs")
            for line in result.get("error_log", []):
                st.code(line)

        if debug:
            st.write("### Debug Log")
            for line in result.get("debug_log", []):
                st.text(line)

    with tab3:
        code = result.get("generated_code")
        if code:
            st.code(code, language="python")
            st.write("### Execution Output")
            st.code(result.get("execution_output", ""), language="text")
        else:
            st.info("No code was generated for this question.")
