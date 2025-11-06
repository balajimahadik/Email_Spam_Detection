import csv
import random

# Create a better dataset with more distinctive spam features
ham_messages = [
    'Hey, how are you doing today?',
    'Would you like to grab lunch later?',
    'Can you send me the report by end of day?',
    'Thanks for your help with the project.',
    'The meeting has been rescheduled to 3 PM tomorrow.',
    'I will be there in 10 minutes',
    'Please review the attached document',
    'Happy birthday! Hope you have a great day',
    'Can we schedule a call for tomorrow?',
    'I am running late, will be there soon',
    'Thanks for the quick response',
    'Looking forward to our discussion',
    'Please let me know if you need anything else',
    'I have completed the task as requested',
    'Could you please clarify this point?',
    'I agree with your suggestion',
    'Let me know what time works for you',
    'I will get back to you shortly',
    'Hope you are having a good day',
    'Thanks for the update',
    'I appreciate your help with this',
    'Please find the information below',
    'I will attend the meeting',
    'Can you provide more details?',
    'I have sent the files you requested',
    'Looking forward to working together',
    'I will call you back in an hour',
    'Please confirm your availability',
    'I have received your email',
    'Thank you for your time',
    'I will keep you posted',
    'Please see my comments below',
    'I have reviewed the proposal',
    'Can we move our meeting to Thursday?',
    'I am available next week',
    'Please send me the agenda',
    'I will prepare the presentation',
    'Thanks for the reminder',
    'I have added this to my calendar',
    'Please advise on the next steps',
    'I will follow up with the team',
    'Could you send me the link?',
    'I have updated the document',
    'Please review and let me know',
    'I will be out of office tomorrow',
    'Thanks for the clarification',
    'I have shared the folder with you',
    'Please find attached the invoice',
    'I will contact you next week',
    'Hope you are doing well',
    'I have booked the conference room'
]

spam_messages = [
    'URGENT!!! You have WON a FREE iPhone!!! Click HERE NOW!!!',
    'CONGRATULATIONS!! You are our 1,000,000th visitor!!! CLAIM your PRIZE!!!',
    '$$$ MAKE MONEY FAST $$$ Work from HOME and earn $5000 per WEEK!!!',
    'FREE!!! Get your FREE Samsung Galaxy S21!!! Limited TIME offer!!!',
    'WINNER!!! You have WON $50,000!!! Click HERE to CLAIM your MONEY!!!',
    'URGENT!!! Your PayPal account is LIMITED!!! Click HERE to VERIFY NOW!!!',
    '$$$ CASH PRIZE $$$ You have WON $1000!!! Text WIN to 12345 NOW!!!',
    'FREE!!! Congratulations! You have WON a FREE vacation to HAWAII!!!',
    'ATTENTION!!! FREE iPad waiting for you!!! Click HERE to CLAIM!!!',
    'URGENT!!! IRS tax refund of $2500 waiting!!! Click HERE to CLAIM!!!',
    '$$$ EASY MONEY $$$ Earn $200 per HOUR working from HOME!!! No experience needed!!!',
    'CONGRATULATIONS!!! You have been SELECTED for a FREE MacBook Pro!!!',
    'FREE!!! FREE Bitcoin worth $1000!!! Claim your FREE cryptocurrency NOW!!!',
    'URGENT!!! Your Netflix account will be SUSPENDED!!! Update payment info NOW!!!',
    'WINNER!!! You have WON a brand NEW car!!! Click HERE to CLAIM your PRIZE!!!',
    '$$$ LOTTERY WINNER $$$ You have WON the LOTTERY!!! $1,000,000 prize!!!',
    'FREE!!! Get your FREE $500 Amazon gift card!!! Limited time offer!!!',
    'URGENT!!! Your bank account will be FROZEN!!! Click HERE NOW to PREVENT!!!',
    'CONGRATULATIONS!!! FREE PlayStation 5 waiting for you!!! Claim it NOW!!!',
    '$$$ GET RICH QUICK $$$ Secret method revealed!!! Make $1000 per DAY!!!',
    'FREE!!! FREE Samsung TV 65 inch!!! You are our lucky WINNER!!!',
    'URGENT!!! Your Apple ID has been COMPROMISED!!! Click HERE to SECURE NOW!!!',
    '$$$ GOVERNMENT GRANT $$$ You are eligible for $25,000 FREE money!!!',
    'WINNER!!! FREE luxury cruise to the BAHAMAS!!! Claim your FREE trip NOW!!!',
    'FREE!!! FREE Walmart gift card worth $1500!!! You have been SELECTED!!!',
    'URGENT!!! Your Amazon account will be CLOSED!!! Click HERE to VERIFY NOW!!!',
    '$$$ PASSIVE INCOME $$$ Make money while you SLEEP!!! $500 per DAY!!!',
    'CONGRATULATIONS!!! You have WON a FREE smart TV!!! Click HERE to CLAIM!!!',
    'FREE!!! FREE groceries for a YEAR!!! You are our WINNER!!! Claim NOW!!!',
    'URGENT!!! Your credit card has been CHARGED!!! Click HERE to DISPUTE NOW!!!',
    '$$$ WORK FROM HOME $$$ Earn $1000 per WEEK!!! Simple online job!!!',
    'WINNER!!! FREE vacation package to PARIS!!! You have WON!!! Claim it NOW!!!',
    'FREE!!! FREE $250 Visa gift card TODAY only!!! Click HERE to GET yours!!!',
    'URGENT!!! Confirm your bank details to AVOID account SUSPENSION!!!',
    'CONGRATULATIONS!!! FREE MacBook Air waiting for you!!! LIMITED time!!!',
    '$$$ ONLINE JOB $$$ No experience needed!!! Earn $500 per DAY from HOME!!!',
    'FREE!!! FREE iPhone 13 Pro Max!!! You are our 1,000,000th customer!!!',
    'URGENT!!! Your IRS refund of $3000 is EXPIRING!!! Click HERE NOW!!!',
    'WINNER!!! You have WON a FREE trip to DISNEY WORLD!!! Family package included!!!',
    '$$$ CASH BONUS $$$ $1000 cash bonus waiting for you!!! Click HERE to CLAIM!!!',
    'FREE!!! FREE gaming laptop worth $2000!!! You have been CHOSEN!!!',
    'URGENT!!! Update your password to PREVENT account HACKING!!! Click HERE!!!',
    'CONGRATULATIONS!!! FREE year of Netflix waiting for you!!! Claim it NOW!!!',
    '$$$ QUICK MONEY $$$ Get $500 cash in 5 minutes!!! No questions asked!!!',
    'FREE!!! FREE drone with camera!!! Limited stock!!! Order yours NOW!!!',
    'URGENT!!! Your PayPal is LIMITED!!! Send documents to RESTORE access NOW!!!',
    'WINNER!!! You have WON a FREE Rolex watch!!! Luxury prize waiting for you!!!',
    '$$$ EASY CASH $$$ $2000 deposited to your account!!! Click to ACTIVATE!!!',
    'FREE!!! FREE home gym equipment!!! You are our fitness WINNER!!! Claim NOW!!!',
    'URGENT!!! Your social security number is at RISK!!! Click HERE to PROTECT!!!',
    'CONGRATULATIONS!!! FREE Tesla Model 3!!! You are our GRAND PRIZE WINNER!!!'
]

# Create balanced dataset
data = []
for msg in ham_messages:
    data.append(['ham', msg])
for msg in spam_messages:
    data.append(['spam', msg])

# Shuffle the data
random.shuffle(data)

# Write to CSV
with open('spam.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['v1', 'v2'])
    writer.writerows(data)

print('Created improved spam.csv with', len(data), 'messages')
print('Ham messages:', len([d for d in data if d[0] == 'ham']))
print('Spam messages:', len([d for d in data if d[0] == 'spam']))