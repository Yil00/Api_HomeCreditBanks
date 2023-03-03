import pandas as pd
import numpy as np
import pickle
import pytest

from app import predictScore,predictDecision,predictSolvabilite


########################
# Lecture des fichiers #
########################
def lecture_X_test_original():
    X_test_original = pd.read_csv("Data/X_test_original.csv")
    X_test_original = X_test_original.rename(columns=str.lower)
    return X_test_original

def lecture_X_test_clean():
    X_test_clean = pd.read_csv("Data/X_test_clean.csv")
    return X_test_clean
#################################################
#-----              TEST API            --------
#################################################

def test_predictScore():
    #Listes des id clients 
    Id_client = list(lecture_X_test_original()['sk_id_curr'])
    ID = Id_client[0]
    assert len(str(ID)) == 6 #Id de longueur 6 (à 6 chiffres )
    ScorePredict = predictScore(ID)
    #ScorePredict.add(ID = 100001)
    assert ScorePredict > 0 #Score forcément positif


def test_predictSolvabilite():
    #Listes des id clients 
    Id_client = list(lecture_X_test_original()['sk_id_curr'])
    ID = Id_client[1]
    assert len(str(ID)) == 6 #Id de longueur 6 (à 6 chiffres )
    #Solvabilite attendu : Id = "100005"
    SolvabilitePredict = predictSolvabilite(ID)
    #ScorePredict.add(ID = 100005)
    assert SolvabilitePredict == "non solvable" #Réponse attendu
    #Cas ou le client est sovlable: 
    ID = Id_client[0]
    SolvabilitePredict2 = predictSolvabilite(ID)
    assert SolvabilitePredict2 == "solvable"


def test_predictDecision():
    #Listes des id clients 
    Id_client = list(lecture_X_test_original()['sk_id_curr'])
    ID = Id_client[1]
    assert len(str(ID)) == 6 #Id de longueur 6 (à 6 chiffres )
    #Decision attendu : Id = "100005"
    DecisionPredict = predictDecision(ID)
    #ScorePredict.add(ID = 100005)
    assert DecisionPredict == "refuser" #Réponse attendu
    #Cas ou le crédit est accorder: 
    ID = Id_client[0]
    DecisionPredict2 = predictDecision(ID)
    assert DecisionPredict2 == "accorder"
    
    
    