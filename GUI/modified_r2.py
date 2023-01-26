def store_data_driver(*args):
    # entries are assumed to be ready in the driver
    names = args[0]
    date = args[1]
    validate_name(names)
    validate_date(date)


#  date format: YYYY-MM-DD
def validate_date(date):
    date = date.replace(" ", "")
    if len(date) != 10:
        return False
    if date[4] != '-' or date[7] != '-':
        return False
    # inject error here
    # fail: 20-01-2020 will pass the following loop
    for char in date:
        if char != '-' and char.isdigit() is False:
            return False

    # correct
    # for i in range(len(date)):
    #     if i is 4 or i is 7:
    #         continue
    #     if date[i].isdigit() is False:
    #         return False
    year = int(date[:4])
    if year > 2100 or year < 1900:
        return False
    month = int(date[5:7])
    # injected error for boundary values month <= 1
    if month > 12 or month < 1:
        return False
    day = int(date[8:])
    # if day < 1 or day > 31:
    #     return False

    if day < 1:
        return False

    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        if day > 31:
            return False
    elif month == 4 or month == 6 or month == 9 or month == 11:
        if day > 30:
            return False
    else:
        if day > 29:
            return False

    return True


def validate_name(names):
    names = names.strip()
    if names[-1] == ';':
        names = names[:-1]
    all_names = names.split(';')
    for i in range(len(all_names)):
        all_names[i] = all_names[i].strip()

    names_valid = False
    for name in all_names:
        if name != '':
            names_valid = True
            break
    if names_valid:
        return all_names
    return None


# if __name__ == "__main__":
#     print(validate_date('20x2-11-11'))