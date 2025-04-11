Automated Email Sending Tool

This project automates the process of sending customized emails with attachments, significantly reducing the time required for routine communication tasks. Originally designed to streamline a repetitive workflow in a professional setting, it cut down a process that used to take over 5 hours to just around 1 minute.

🔧 What It Does

Automatically zips specific folders containing files for different clients
Matches each client to their email address based on an Excel list
Customizes the subject and body of each email
Sends emails in bulk with a short delay between each to prevent issues
Provides console feedback about the status of each email sent
📂 Files and Structure

automatic_sending_translated.ipynb: Main notebook that contains all the logic for the automation process
Folder structure:
main_folder/
- client_1/
  - files...
- client_2/
  -files...
- ...
email_list_file.xlsx: Excel file mapping client names to their respective email addresses

📈 Impact

This automation brought a major productivity boost, transforming a manual and time-consuming process into a fast and reliable one. It's a great example of how Python can be applied to solve real business problems and improve operational efficiency.

✅ Requirements

Python 3
pandas, smtplib, email, openpyxl libraries (install with pip install pandas openpyxl)

⚠️ Note

All sensitive information such as email addresses and credentials were removed or hidden for privacy reasons.
