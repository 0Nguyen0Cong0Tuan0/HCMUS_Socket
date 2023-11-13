# emails_input = input("Enter emails separated by commas: ")

# # Split the input string into a list of emails
# email_list = emails_input.split(',')

# # Remove any leading or trailing whitespaces from each email
# email_list = [email.strip() for email in email_list]

# # Convert the list to a tuple if needed
# email_tuple = tuple(email_list)

# print("Email Tuple:", email_tuple)

mails_address = []
emails = "1@gmail.com"
mails_address.append(emails)

email_input = "nguyenvanA@gmail.com, nguyenVanB@gmail.com, 2@gmail.com"
email_input = email_input.split(',')
email_input = [email.strip() for email in email_input]
mails_address.extend(email_input)

for mail in mails_address:
    print(mail)