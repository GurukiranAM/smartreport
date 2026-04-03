import streamlit as st
from google import genai

st.set_page_config(page_title="SmartReport AI", layout="wide")

st.title("📄 SmartReport AI - Project Report Generator")

# ✅ API KEY (Streamlit secrets)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 📌 Sections
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

# 🚀 Generate Button
if st.button("🚀 Generate Report"):

    if not topic:
        st.warning("Please enter a topic")

    elif not ordered_sections:
        st.warning("Please define sections")

    else:
        final_report = ""

        for section in ordered_sections.split(","):
            section = section.strip()

            if not section:
                continue

            prompt = f"""
You are an expert academic writer.

Write a detailed, professional {section} for a project report.

Topic: {topic}

Rules:
- Use formal academic tone
- Be clear and structured
- Avoid bullet points unless necessary
"""

            try:
                # ✅ Correct Gemini API call (NEW SDK)
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )

                content = response.text

                st.subheader(section)
                st.write(content)

                final_report += f"\n\n{section}\n{content}"

            except Exception as e:
                st.error(f"Error in {section}: {e}")

        st.success("✅ Report Generated Successfully!")

        st.download_button(
            label="📥 Download Report",
            data=final_report,
            file_name="SmartReport.txt",
            mime="text/plain"
        )