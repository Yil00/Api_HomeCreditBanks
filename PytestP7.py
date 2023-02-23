import requests
import pytest

class TestApi:
    # Source
    URL1 ="http://127.0.0.1:5003/predictScore?id_client=100001"
    URL2 ="http://127.0.0.1:5003/decision?id_client=100001"
    URL3 ="http://127.0.0.1:5003/Solvabilite?id_client=100001"
    URL4 ="http://127.0.0.1:5003/ClientID?id_client=100001"
    data = {'decision_text': 'accorder'}
    data2 = {'solvabilite_text': 'solvable'}
    data3 = {'identifiant_text': 100001}

    # Test - Prédiction - Score
    def test_prediction(self):
        resp = requests.get(self.URL1)
        assert resp.status_code == 200
        assert len(resp.json()) == 1
        #print("Test 1 completed - Le score est bien prédit")

    # Test - Décision
    def test_decision(self):
        resp = requests.get(self.URL2)
        assert resp.status_code == 200
        assert resp.json() == self.data
        #print("Test 2 completed - Décision validé")

    # Test - Solvabilité
    def test_solvabilite(self):
        resp = requests.get(self.URL3)
        assert resp.status_code == 200
        assert resp.json() == self.data2
        #print("Test 3 completed - Solvabilité prédit ")

    # Test - Identifiant
    def test_id(self):
        resp = requests.get(self.URL4)
        assert resp.status_code == 200
        assert resp.json() == self.data3
        #print("Test 4 completed - Identifiant afficher")

