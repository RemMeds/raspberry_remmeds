import connection
import pill
import replace_data
#from unittest.mock import patch

class TestConnection():
    def test_select_id(self):
        data = connection.selectUserID()
        assert data == 8

    def test_check_comp(self):
        data = connection.checkComp()
        assert data == None


    def test_synchro_BDD(self):
        data = connection.synchroBDD("8")
        assert data == "Synchro"


    def test_Check_If_Exists(self):
        data = connection.checkIfExists("8", "rm_user", "us_id")
        assert data == False
"""
    def test_Same_Data(self):
        data = {}

        map = {}
        map['ID'] = "8"
        map['table'] = "rm_user"
        map['cdt'] = "us_id"

        data = connection.sameData(data, map)
        assert data == False
"""

class TestPill():
    def test_Led_Off(self):
        map = {}
        map["Comp"] = "1"
        data = pill.ledOff(map)
        assert data == None
"""
@patch('pill.ledOn.connection.addhisto')
@patch('pill.ledOn.mail.alertMissing')
class TestLedOn():
    def test_Led_On(self, mock_mail, mock_connection):
        list = {}
        list["Comp"] = "1"
        data = pill.ledOn(list)
        assert data == "totototo"
"""


class TestReplaceData():
    def test_replace_user_field(self):
        data = replace_data.replace("user_id", "rm_user")
        assert data == "us_id"

    def test_replace_repertory_field(self):
        data = replace_data.replace("note", "rm_repertory")
        assert data == "re_note"

    def test_replace_compartment_field(self):
        data = replace_data.replace("duration_number", "rm_compartment")
        assert data == "com_durationnumb"

    def test_replace_numerique(self):
        data = replace_data.replace("0", "num")
        assert data == "00"

    def test_comToPin(self):
        data = replace_data.comToPin("1")
        assert data == "18"

    def test_days(self):
        data = replace_data.days("0")
        assert data == "Lundi"