import string

def password_checker(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(char.isupper() for char in password):
        score +=1
    if any(char.islower() for char in password):
        score +=1
    if any(char.isdigit() for char in password):
        score +=1
    if any(char in string.punctuation for char in password):
        score +=1  
    
    return score 

def password_strength(score): 
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Moderate"
    elif score == 5:
        return "Strong"