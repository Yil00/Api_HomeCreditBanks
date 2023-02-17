import unittest
import requests
############
###### Test Unitaire - API_P7_Dashboard
############
class TestApi(unittest.TestCase):
    ##### Source ####
    URL1 ="http://127.0.0.1:5003//predictScore?id_client=100001"
    URL2 ="http://127.0.0.1:5003//decision?id_client=100001"
    URL3 ="http://127.0.0.1:5003//Solvabilite?id_client=100001"
    URL4 ="http://127.0.0.1:5003//ClientID?id_client=100001"
    data = {'decision_text': 'accorder'}
    data2 = {'solvabilite_text': 'solvable'}
    data3 = {'identifiant_text': 100001}

    #Test - Prédiction - Score
    def test_1_get_all_todos(self):
        resp = requests.get(self.URL1)
        self.assertEqual(resp.status_code,200)
        self.assertEqual(len(resp.json()),1)
        print("Test 1 completed - Le score est bien prédit")
    #Test - Décision -
    def test_2_get_all_todo(self):
        resp = requests.get(self.URL2)
        self.assertEqual(resp.status_code,200)
        self.assertDictEqual(resp.json(),self.data)
        print("Test 2 completed - Décision validé")

    #Test - Solvabilité -
    def test_3_get_all_todo(self):
        resp = requests.get(self.URL3)
        self.assertEqual(resp.status_code,200)
        self.assertDictEqual(resp.json(),self.data2)
        print("Test 3 completed - Solvabilité prédit ")
    #Test - Identifiant -
    def test_4_get_all_todo(self):
        resp = requests.get(self.URL4)
        self.assertEqual(resp.status_code,200)
        self.assertDictEqual(resp.json(),self.data3)
        print("Test 4 completed - Identifiant afficher")


if __name__=="__main__":
    ###### Lancement des test #####
    tester = TestApi()
    print("Pour le client: num°ID = 100001")
    tester.test_1_get_all_todos()
    tester.test_2_get_all_todo()
    tester.test_3_get_all_todo()
    tester.test_4_get_all_todo()
