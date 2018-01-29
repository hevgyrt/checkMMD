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
        NOTE: valid_formats should be extended if need for other formats
    """
    valid_formats = ["%Y-%m-%d","%Y-%m-%dT%H","%Y-%m-%dT%H:%M",
                    "%Y-%m-%dT%H:%M:%S","%Y-%m-%dT%H:%M:%S.%fZ",
                    "%Y-%m-%dT%H:%M:%S.%f"]
    for f in valid_formats:
        try:
            if datetime.datetime.strptime(date,f):
                return True
        except:
            pass

    print str("Does you input data: %s \nfollow ISO 8601 standard?" %date +
              "\nIf YES, please edit the validDateFormat function in myCheckMMDFunctions.")
    return False
