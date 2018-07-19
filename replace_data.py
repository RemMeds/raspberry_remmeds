

def replace(str, data):
    #User
    if(data == "rm_user"):
        if str == "user_id":
            return "us_id"
        elif str == "pref_bedtime":
            return "us_prefbedtime"
        elif str == "pref_breakfast":
            return "us_prefbreakfast"
        elif str == "firstname":
            return "us_firstname"
        elif str == "mail":
            return "us_mail"
        elif str == "pref_lunch":
            return "us_preflunch"
        elif str == "lastname":
            return "us_lastname"
        elif str == "pref_dinner":
            return "us_prefdinner"
        elif str == "password":
            return "us_mdp"

    #rm_repertory
    if(data == "rm_repertory"):
        if str == "note":
            return "re_note"
        elif str == "phonenumber":
            return "re_phonenumber"
        elif str == "chx_sms":
            return "re_chxSMS"
        elif str == "firstname":
            return "re_firstname"
        elif str == "mail":
            return "re_mail"
        elif str == "lastname":
            return "re_lastname"
        elif str == "chx_mail":
            return "re_chxMail"
        elif str == "contact_id":
            return "re_id"

    #rm_compartment
    if(data == "rm_compartment"):
        if str == "duration_number":
            return "com_durationnumb"
        elif str == "check_perso_hour":
            return "com_check_perso_hour"
        elif str == "drug_name":
            return "com_name"
        elif str == "frequency":
            return "com_frequency"
        elif str == "compartment_num":
            return "com_num"
        elif str == "list_pref":
            return "com_list_pref"
        elif str == "perso_hour":
            return "com_hour"
        elif str == "duration_text":
            return "com_durationtext"
        elif str == "user_id":
            return "us_id"
        elif str == "compartment_id":
            return "com_id"
        elif str == "days":
            return "com_days"
        elif str == "note":
            return "com_note"

    if(data == "num"):
        if str == "0":
            return "00"
        elif str == "1":
            return "01"
        elif str == "2":
            return "02"
        elif str == "3":
            return "03"
        elif str == "4":
            return "04"
        elif str == "5":
            return "05"
        elif str == "6":
            return "06"
        elif str == "7":
            return "07"
        elif str == "8":
            return "08"
        elif str == "9":
            return "09"
        else:
            return str

def comToPin(comp):
    if comp == "1":
        return "18"
    if comp == "2":
        return "23"
    if comp == "3":
        return ""
    if comp == "4":
        return ""
    if comp == "5":
        return ""
    if comp == "6":
        return ""
    if comp == "7":
        return ""
    if comp == "8":
        return ""

def days(day):
    if day == "0":
        return "Lundi"
    elif day == "1":
        return "Mardi"
    elif day == "2":
        return "Mercredi"
    elif day == "3":
        return "Jeudi"
    elif day == "4":
        return "Vendredi"
    elif day == "5":
        return "Samedi"
    elif day == "6":
        return "Dimanche"
