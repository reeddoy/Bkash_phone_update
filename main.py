from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time

chrome_profile_path = 'C:/Users/ADMIN/AppData/Local/Google/Chrome/User Data'
options = Options()
options.add_argument(f"user-data-dir={chrome_profile_path}")
options.add_argument("profile-directory=Default")
chromedriver_path = 'D:/Testing/chromedriver.exe' 


service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

def read_logged_messages(log_file):
    logged_messages = set()
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as file:
            next(file)  # Skip header line
            for line in file:
                message = line.strip().split('\t', 1)[1]  # Split by tab and take the message part
                logged_messages.add(message)
    return logged_messages



while True:
    try:
        # Open the web page
        driver.get('https://messages.google.com/web/conversations/7')

        # Wait for the page to load completely
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".text-msg-content"))  # Adjust this selector based on actual website structure
        )

        # Find all messages with the class name 'text-msg-content'
        messages = driver.find_elements(By.CSS_SELECTOR, ".text-msg-content")

        # Prepare to save messages to a text file
        log_file = 'message_log.txt'

        # Read existing logged messages to avoid duplicates
        logged_messages = read_logged_messages(log_file)

        with open(log_file, 'a', encoding='utf-8') as file:
            # Process messages
            for message in messages:
                text = message.text
                if ('cash in' in text.lower() or 'you have received' in text.lower()) and text not in logged_messages:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write(f"{timestamp}\t{text}\n")
                    logged_messages.add(text)  # Add to set to avoid duplicate logging
                    print(f"Saved message: {text}")

        print(f"Messages saved to {log_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(20)

# finally:
#     driver.quit()
