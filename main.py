import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama

st.title('AI Web Scrapper')

# Text input for the URL
url = st.text_input('Enter a web URL:')

# Scrape button and process
if st.button('Scrape'):
    st.write('Scraping...')
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_body_content = clean_body_content(body_content)

    # Store the cleaned content in session state
    st.session_state.dom_content = cleaned_body_content

# Only show this part if 'dom_content' is already in session state
if "dom_content" in st.session_state:
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", st.session_state.dom_content, height=400)

    # Text area for parse description
    parse_description = st.text_area("Describe what you want to parse:")

    # Parse button and process
    if st.button("Parse"):
        if parse_description:
            st.write('Parsing...')

            # Split content and parse
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)

            # Display the result
            st.write(result)
