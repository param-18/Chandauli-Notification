#"https://chandaulisamachar.com/"
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def send_email(sub,msg):
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'chandaulitest@gmail.com'
    sender_password = 'rabkettcorobwknf'
    recipient_email = 'sainiarun8569803094@gmail.com'
    subject = sub
    message = msg

    # Create the email
    email = MIMEMultipart()
    email['From'] = sender_email
    email['To'] = recipient_email
    email['Subject'] = subject

    email.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Enable secure connection
        server.login(sender_email, sender_password)
        server.send_message(email)
        print('Email sent successfully!')

# Set up the Selenium ChromeDriver for local
service = Service('chrome-driver-path')  # Replace with the path to your chromedriver executable
options = Options()
options.add_argument('--headless')  # Optional: Run the browser in headless mode
driver = webdriver.Chrome(service=service, options=options)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

# Define the URL of the website you want to monitor
url = 'https://chandaulisamachar.com/top-news-chandauli/'

# Navigate to the website
driver.get(url)

# Select the target element you want to monitor for changes
posts = driver.find_element(By.CSS_SELECTOR, 'div.highlighted-story').find_element(By.CSS_SELECTOR,'div.colombiaonesuccess').find_elements(By.CSS_SELECTOR,'div')
# Store the initial state of the target element
initial_post = posts[0].text.strip()

# Run this code periodically to check for changes
while True:
    # Refresh the page to get the latest content
    driver.refresh()

    # Select the target element again
    target_post = driver.find_element(By.CSS_SELECTOR, 'div.highlighted-story').find_element(By.CSS_SELECTOR,'div.colombiaonesuccess').find_elements(By.CSS_SELECTOR,'div')[0]

    # Get the current state of the target element
    current_post = target_post.text.strip()
    print(current_post)
    # Compare the current state with the initial state
    if current_post != initial_post:
        lines = current_post.split(sep='\n')
        send_email('New News from Chandauli Samachar',lines[0])
        # Perform actions or generate alerts as needed

    # Update the initial state with the current state for the next iteration
    initial_post = current_post

# Quit the browser when done
driver.quit()
