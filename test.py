from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Path to the default Chrome user data directory (this might vary based on your OS)
chrome_profile_path = 'C:/Users/ADMIN/AppData/Local/Google/Chrome/User Data'

# Set up Chrome options to use the default profile
options = Options()
options.add_argument(f"user-data-dir={chrome_profile_path}")
options.add_argument("profile-directory=Default")  # Use the default profile

# Path to the ChromeDriver executable
chromedriver_path = 'D:/Testing/chromedriver.exe'  # Replace with your actual path

# Initialize the Chrome driver
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

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
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write("Time\t\t\tMessage\n")  # Header for the log file

        # Process messages
        for message in messages:
            text = message.text
            if 'cash in' in text.lower() or 'you have received' in text.lower():
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{timestamp}\t{text}\n")
                print(f"Saved message: {text}")

    print(f"Messages saved to {log_file}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
