

def replace(str, table):
    #User
    if(table == "rm_user"):
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
    if(table == "rm_repertory"):
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
    if(table == "rm_compartment"):
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