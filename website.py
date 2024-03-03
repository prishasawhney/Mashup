# Name : Prisha Sawhney
# Group : 3CS10
# Roll Number : 102116052

import streamlit as st
from mashup import *
import re

def main():
    # Custom CSS styling
    custom_css = """
    <style>
        /* Add your custom CSS code here */
        body {
            font-family: Arial, sans-serif;
        }
        .stApp {
            margin: 0 auto;
            padding: 20px;
        }
        .stTextInput, .stNumberInput, .stButton {
            margin-bottom: 15px;
        }
        .stButton {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .stButton:hover {
            background-color: #45a049;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.title("Mashup")
    singer_name = st.text_input("Singer Name")
    num_videos = st.number_input("Number of Videos", min_value=0, step=1)
    video_duration = st.number_input("Duration of Videos (in seconds)", min_value=0, step=1)
    email_id = st.text_input("Email ID")

    # Submit Button
    if st.button("Submit"):
        if not is_valid_email(email_id):
            st.write("Invalid email address. Please enter a valid email address.")
            return
        process_form_data(singer_name, num_videos, video_duration, email_id)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def process_form_data(singer_name, num_videos, video_duration, email_id):
    output_mp3 = "102116052-output.mp3"
    output_zip = output_mp3.replace(".mp3", ".zip")

    if num_videos < 10:
        st.write("Number of songs should be greater than 10")
        return
    links = get_urls(singer_name, num_videos)
    mp3_files = extract_audio(links, singer_name)
    if (video_duration < 20):
        st.write("Duration should be greater than 20 seconds")
        return
    cut_paths = cut_duration(mp3_files, video_duration)
    st.write(cut_paths)
    merge_audio(cut_paths, output_mp3)
    zip_file(output_mp3, output_zip)
    send_mail(email_id, output_zip)
    st.write("Emailed Successfully to {}".format(email_id))

if __name__ == "__main__":
    main()