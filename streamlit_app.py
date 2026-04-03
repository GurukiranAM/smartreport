import streamlit as st
from google import genai

st.set_page_config(page_title="SmartReport AI", layout="wide")

st.title("📄 SmartReport AI - Project Report Generator")

# ✅ NEW SDK CLIENT
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

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

if st.button("🚀 Generate Report"):

    if not topic.strip():
        st.warning("Enter topic")

    else:
        final_report = ""

        with st.spinner("Generating report..."):

            for section in ordered_sections.split(","):
                section = section.strip()

                if not section:
                    continue

                prompt = f"""
Write a detailed {section} for a project report.

Topic: {topic}

Use formal academic language and proper structure.
"""

                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",   # 🔥 THIS IS THE FIX
                        contents=prompt
                    )

                    content = response.text

                    st.subheader(section)
                    st.write(content)

                    final_report += f"\n\n{section}\n{content}"

                except Exception as e:
                    st.error(f"Error in {section}: {e}")

        st.download_button(
            "Download Report",
            final_report,
            "report.txt"
        )