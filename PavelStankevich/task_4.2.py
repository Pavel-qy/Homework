# Task 4.2
def is_palindrome(string):
    '''Check if a string is a palindrome or not.
    Return True or False'''
    string = string.lower()
    punctuation_marks = " ,.?!;:–—"
    
    for c in punctuation_marks:
        string = string.replace(c, "")
    
    for i in range(len(string) // 2):
        if string[i] != string[-i - 1]:
            return False
                
    return True

print(is_palindrome("A man, a plan, a canal – Panama"))
print(is_palindrome("Eva, can I see bees in a cave?"))
print(is_palindrome("Able was I, ere I saw Elba."))
