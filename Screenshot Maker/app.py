import streamlit as st
from selenium import webdriver
import time
import os
import zipfile
from io import BytesIO

# Function to take screenshots of the full page by scrolling down
def take_full_page_screenshot(url):
    # Using headless Chrome for screenshot
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome(options=options)
    
    # Load the web page
    driver.get(url)
    
    # Get initial page height
    initial_height = driver.execute_script("return document.body.scrollHeight")
    
    # Scroll down and capture screenshots
    screenshots = []
    for i in range(4):  # You can adjust this range as needed
        # Scroll down
        driver.execute_script(f"window.scrollTo(0, {i * initial_height / 3});")
        time.sleep(1)  # Wait for page to load
        
        # Capture screenshot
        screenshot_path = f"{url.replace('file://', '').replace('/', '_')}_{i}.png"
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)
    
    # Close the browser
    driver.quit()
    
    return screenshots

# Function to create a zip file containing all the screenshots
def create_zip_file(screenshots):
    zip_file_path = "screenshots.zip"
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for screenshot in screenshots:
            zipf.write(screenshot, os.path.basename(screenshot))
    return zip_file_path

# Streamlit app
def main():
    st.title("Full Page Screenshot Generator")
    st.markdown("Enter the URL of the website you want to take full page screenshots of:")
    
    url = st.text_input("URL:")
    
    if st.button("Take Full Page Screenshots"):
        if url:
            st.markdown("Taking full page screenshots...")
            screenshots = take_full_page_screenshot(url)
            for i, screenshot_path in enumerate(screenshots):
                st.image(screenshot_path, caption=f"Screenshot {i+1}", use_column_width=True)
            zip_file_path = create_zip_file(screenshots)
            with open(zip_file_path, "rb") as f:
                bytes_data = f.read()
                st.download_button(label="Download All Screenshots", data=bytes_data, file_name="screenshots.zip", mime="application/zip")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
