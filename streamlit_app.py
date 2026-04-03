import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="SmartReport AI", layout="wide")

st.title("📄 SmartReport AI - Project Report Generator")

# Step 1: Select Sections
st.header("1. Select Report Sections")

sections = [
    "Abstract", "Introduction", "Literature Review",
    "Methodology", "Results", "Conclusion", "References"
]

selected_sections = st.multiselect(
    "Choose sections:",
    sections,
    default=sections
)

# Step 2: Arrange Sections
st.header("2. Arrange Sections")

ordered_sections = st.text_area(
    "Enter sections in order (comma separated):",
    ",".join(selected_sections)
)

# Step 3: Topic Input
st.header("3. Enter Topic")

topic = st.text_input("Enter your project topic:")

# Step 4: Generate Report
st.header("4. Generate Report")

if st.button("🚀 Generate Report"):

    if not topic:
        st.warning("Please enter a topic")

    elif not ordered_sections:
        st.warning("Please define sections")

    else:
        st.info("Generating report... please wait ⏳")

        final_report = ""

        for section in ordered_sections.split(","):
            section = section.strip()

            prompt = f"""
Write a professional {section} for a project report on the topic:
{topic}.

Requirements:
- Formal academic language
- Clear structure
- Concise and meaningful content
"""

            try:
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=prompt
                )
                content = response.output_text

            except Exception as e:
                st.error(f"Error in {section}: {e}")
                content = "Error generating content."

            # Display section
            st.subheader(f"📌 {section}")
            st.write(content)

            final_report += f"\n\n{section}\n{content}"

        st.success("✅ Report Generated Successfully!")
