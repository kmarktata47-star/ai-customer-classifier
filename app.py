import streamlit as st
from classifier import classify

st.title("AI Customer Classifier")

message = st.text_area("Customer message:", height=150)

if st.button("Analyze"):
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                result = classify(message)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
            else:
                st.success("Category: " + result.category)
                st.write("Urgency: " + result.urgency)
                st.caption(result.reason)