import streamlit as st
from backend.py import *
def main():
    st.title("Cover Letter Generator")

    # Input for the link
    link = st.text_input("Enter the Job Posting URL")

    # File uploader for the PDF
    uploaded_pdf = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    # Button to generate cover letter
    if st.button("WRITE COVER LETTER"):
        if link and uploaded_pdf:
            # Assuming the LLM part is handled externally and the cover letter is generated
            # Here, you would call your LLM function and pass the 'link' and 'uploaded_pdf'
            cover_letter = generate_cover_letter(link, uploaded_pdf)

            # Display the generated cover letter
            st.subheader("Generated Cover Letter")
            st.write(cover_letter)
        else:
            st.error("Please provide both the job link and resume PDF.")



if __name__ == "__main__":
    main()
