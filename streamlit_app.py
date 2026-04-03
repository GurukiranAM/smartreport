import streamlit as st
from google import genai

st.set_page_config(page_title="SmartReport AI", layout="wide")

st.title("📄 SmartReport AI - Project Report Generator")

# ✅ API Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Sections
sections = [
    "Abstract", "Introduction", "Literature Review",
    "Methodology", "Results", "Conclusion", "References"
]

selected_sections = st.multiselect(
    "Choose sections:",
    sections,
    default=sections
)

ordered_sections = st.text_area(
    "Enter sections in order (comma separated):",
    ",".join(selected_sections)
)

topic = st.text_input("Enter your project topic:")

# Generate
if st.button("🚀 Generate Report"):

    if not topic.strip():
        st.warning("⚠️ Please enter a topic")

    elif not ordered_sections.strip():
        st.warning("⚠️ Please define sections")

    else:
        with st.spinner("Generating full report... ⏳"):

            # 🔥 SINGLE PROMPT (MAIN FIX)
            prompt = f"""
You are an expert academic writer.

Write a complete project report on the topic:

{topic}

Include the following sections:
{ordered_sections}

Rules:
- Each section must have a clear heading
- Use formal academic tone
- Well-structured paragraphs
- Add technical depth where needed
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )

                content = response.text

                # Display full report
                st.subheader("📄 Generated Report")
                st.write(content)

                # Download
                st.download_button(
                    label="📥 Download Report",
                    data=content,
                    file_name="SmartReport.txt",
                    mime="text/plain"
                )

                st.success("✅ Report Generated Successfully!")

            except Exception as e:
                st.error(f"❌ Error: {e}")