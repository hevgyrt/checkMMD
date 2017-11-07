import datetime

def multipleLanguages(languages):
    """ Function to check if array contains several languages
        Inputdata:
            - @languages : list of xml attribute values
    """
    if len(languages) > 1:
        for i in range(1,len(languages)):
            if languages[i-1] == languages[i]:
                return False
    return True

def validKeywords(keywords, validKeywords):
    """ Inputdata: @keywords = list, @validKeywords = list"""
    for keyword in keywords:
        if not len([word for word in validKeywords if keyword.lower() == word.lower()]) > 0:
            print "\t Invalid keyword: " + keyword
            return False
    return True

def validText(text, invalidCharacters):
    """ Inputdata:
        @text = string,
        @invalidCharacters = string with invalid characters
    """
    invalid = set(invalidCharacters)
    if not any((char in invalid) for char in text):
        return True
    return False

def containString(keywords, validKeywords):
    """ Function to check if string contains valid part
        Inputdata:
            - @keywords : list of xml element text values
            - @validKeywords : list of xml element text values
    """
    contained = []
    for keyword in keywords:
        tmp_boolean = False
        for validKeyword in validKeywords:
            if validKeyword in keyword:
                tmp_boolean = True
        contained.append(tmp_boolean)
    if all(element == True for element in contained):
        return True
    else:
        return False

def validDateFormat(date):
    """ Function to check if date has valid format after ISO 8601 standard
    """
    try:
        datetime.datetime.strptime(date,"%Y-%m-%d")
        return True
    except ValueError:
        print "The date format does not follow ISO 8601 standard, thus invalid."
        return False
