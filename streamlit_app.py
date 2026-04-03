import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(page_title="SmartReport AI", layout="wide")

st.title("📄 SmartReport AI - Project Report Generator")

# ✅ API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ⚠️ Use stable model (important fix)
model = genai.GenerativeModel("gemini-pro")

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
        final_report = ""

        # 🔥 Loading animation
        with st.spinner("Generating AI-powered report... ⏳"):

            for section in ordered_sections.split(","):
                section = section.strip()

                if not section:
                    continue

                prompt = f"""
You are an expert academic writer.

Write a detailed {section} for a professional engineering project report.

Topic: {topic}

Instructions:
- Minimum 300 words
- Formal academic tone
- Well-structured paragraphs
- Include technical depth
- Avoid unnecessary bullet points
"""

                try:
                    response = model.generate_content(
                        prompt,
                        generation_config={
                            "temperature": 0.7,
                            "max_output_tokens": 800
                        }
                    )

                    content = response.text if response.text else "No content generated."

                    # Display
                    st.subheader(f"📌 {section}")
                    st.write(content)

                    final_report += f"\n\n{section}\n{content}"

                except Exception as e:
                    st.error(f"❌ Error in {section}: {e}")

        st.success("✅ Report Generated Successfully!")

        # Download button
        st.download_button(
            label="📥 Download Report",
            data=final_report,
            file_name="SmartReport.txt",
            mime="text/plain"
        )