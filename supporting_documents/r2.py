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

    for char in date:
        if char != '-' and char.isdigit() is False:
            return False

    year = int(date[:4])
    if year > 2100 or year < 1900:
        return False
    month = int(date[5:7])

    if month > 12 or month <= 1:
        return False
    day = int(date[8:])
    if day < 1 or day > 31:
        return False

    return True


def validate_name(names):
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
