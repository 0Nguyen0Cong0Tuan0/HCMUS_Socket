Subject = ["urgent", "asap", "important", "action required", "critical", "priority", "attention", "dealine", "approval required", "emergency", "important information", "right now"]
Spam = ['virus', 'hack', 'crack', 'security alert', 'suspicious activity', 
        'unauthorized access', 'account compromise', 'fraud warning', 'phishing attempt',
        'please confirm your identity', 'click here to reset your password', 'verify your account',
        'unusual login activity', 'your account will be suspended', 'bank account verification',
        'important security upadate', 'win a prize', 'win a lottery']
 
content = "Read me! This is the please confirm your identity mail"

if any(phrase.lower() in content.lower() for phrase in Spam):
    print("SPAM")
elif any(phrase.lower() in content.lower() for phrase in Subject):
    print("Project")