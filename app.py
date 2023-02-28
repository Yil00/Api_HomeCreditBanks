# Import all packages and libraries
import pandas as pd
import numpy as np
from flask import Flask, render_template, request,jsonify

import pickle

app = Flask(__name__)

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
# Lecture du modèle de prédiction et des scores #
#################################################
model_LGBM = pickle.load(open("model_LGBM.pkl", "rb"))
#######################################################
# Fonction Primaire : Score prédict|Decision|Solvabilité|ID
########################################################
def predictScore(ID):
    all_id_client = list(lecture_X_test_original()['sk_id_curr'])
    # Prédiction de la classe 0 ou 1
    y_pred_lgbm = model_LGBM.predict(lecture_X_test_clean().drop(labels="sk_id_curr", axis=1))
    # Prédiction du % de risque    
    y_pred_lgbm_proba = model_LGBM.predict_proba(lecture_X_test_clean().drop(labels="sk_id_curr", axis=1)) 

    # Récupération du score du client et ID(sous df) 
    y_pred_lgbm_proba_df = pd.DataFrame(y_pred_lgbm_proba, columns=['proba_classe_0', 'proba_classe_1'])
    y_pred_lgbm_proba_df = pd.concat([y_pred_lgbm_proba_df['proba_classe_1'],
                                lecture_X_test_clean()['sk_id_curr']], axis=1)
   # Vérification que l'ID client saisi est valide
    if ID not in all_id_client:
        prediction="NA"
    else :
        number=""
        score = y_pred_lgbm_proba_df[y_pred_lgbm_proba_df['sk_id_curr']==ID]
        prediction = round(score.proba_classe_1.iloc[0]*100, 1)
    
    # Retour de la réponse sous la forme d'un objet JSON
    return prediction


def predictSolvabilite(ID):
    # Récupération des identifiants des clients dans les données de test
    all_id_client = list(lecture_X_test_original()['sk_id_curr'])

    y_pred_lgbm = model_LGBM.predict(lecture_X_test_clean().drop(labels="sk_id_curr", axis=1))    # Prédiction de la classe 0 ou 1
    y_pred_lgbm_proba = model_LGBM.predict_proba(lecture_X_test_clean().drop(labels="sk_id_curr", axis=1)) # Prédiction du % de risque

    # Récupération du score du client
    y_pred_lgbm_proba_df = pd.DataFrame(y_pred_lgbm_proba, columns=['proba_classe_0', 'proba_classe_1'])
    y_pred_lgbm_proba_df = pd.concat([y_pred_lgbm_proba_df['proba_classe_1'],
                                    lecture_X_test_clean()['sk_id_curr']], axis=1)
    
    y_pred_lgbm_df = pd.DataFrame(y_pred_lgbm, columns=['prediction'])
    y_pred_lgbm_df = pd.concat([y_pred_lgbm_df, lecture_X_test_clean()['sk_id_curr']], axis=1)
    y_pred_lgbm_df['client'] = np.where(y_pred_lgbm_df.prediction == 1, "non solvable", "solvable")
    y_pred_lgbm_df['decision'] = np.where(y_pred_lgbm_df.prediction == 1, "refuser", "accorder")

    # Vérification de la validité de l'identifiant
    if ID not in all_id_client:
        solvabilite="NA"
    else :
        number=""
        # Récupération de la prédiction de décision pour le client
        solvabilite = y_pred_lgbm_df.loc[y_pred_lgbm_df['sk_id_curr']==ID, "client"].values
        solvabilite = solvabilite[0]

    return solvabilite

def predictDecision(ID):
    
    # Récupération de tous les identifiants de clients dans le fichier X_test_original.csv
    all_id_client = list(lecture_X_test_original()['sk_id_curr'])

    y_pred_lgbm = model_LGBM.predict(lecture_X_test_clean().drop(labels="sk_id_curr", axis=1))    # Prédiction de la classe 0 ou 1
    y_pred_lgbm_proba = model_LGBM.predict_proba(lecture_X_test_clean().drop(labels="sk_id_curr", axis=1)) # Prédiction du % de risque

    # Récupération du score du client
    y_pred_lgbm_proba_df = pd.DataFrame(y_pred_lgbm_proba, columns=['proba_classe_0', 'proba_classe_1'])
    y_pred_lgbm_proba_df = pd.concat([y_pred_lgbm_proba_df['proba_classe_1'],
                                    lecture_X_test_clean()['sk_id_curr']], axis=1)
    
    y_pred_lgbm_df = pd.DataFrame(y_pred_lgbm, columns=['prediction'])
    y_pred_lgbm_df = pd.concat([y_pred_lgbm_df, lecture_X_test_clean()['sk_id_curr']], axis=1)
    y_pred_lgbm_df['client'] = np.where(y_pred_lgbm_df.prediction == 1, "non solvable", "solvable")
    y_pred_lgbm_df['decision'] = np.where(y_pred_lgbm_df.prediction == 1, "refuser", "accorder")

    if ID not in all_id_client:
        decision="NA"
    else :
        number=""
        decision = y_pred_lgbm_df.loc[y_pred_lgbm_df['sk_id_curr']==ID, "decision"].values
        decision = decision[0]

    return decision


###################################################
#               - API DASHBOARD-
###################################################
# Route de l'API pour prédire le score d'un client donné
@app.route("/predictScore", methods = ['GET'])
def predict01():
    # Récupération de tous les identifiants de clients dans le fichier X_test_original.csv
    all_id_client = list(lecture_X_test_original()['sk_id_curr'])
    # Récupération de l'identifiant client envoyé dans la requête GET
    ID = request.args['id_client']
    ID = int(ID)

   # Vérification que l'ID client saisi est valide
    if ID not in all_id_client:
        prediction="NA"
    else :
        predictScore(ID=ID)
    
    # Retour de la réponse sous la forme d'un objet JSON
    return jsonify(Prediction = predictScore(ID=ID))      #prediction)
   

# Définition des routes de l'API pour chaque prédiction
@app.route("/Solvabilite", methods = ['GET'])
def predict1():
    # Récupération des identifiants des clients dans les données de test
    all_id_client = list(lecture_X_test_original()['sk_id_curr'])
    # Récupération de l'identifiant du client envoyé par l'utilisateur
    ID = request.args['id_client']
    ID = int(ID)

    # Vérification de la validité de l'identifiant
    if ID not in all_id_client:
        solvabilite="NA"
    else :
        predictSolvabilite(ID=ID)

    return jsonify( solvabilite_text=predictSolvabilite(ID=ID))

@app.route("/decision", methods = ['GET'])
def predict2():
    
    all_id_client = list(lecture_X_test_original()['sk_id_curr'])

    ID = request.args['id_client']
    ID = int(ID)

    if ID not in all_id_client:
        decision="NA"
    else :
        predictDecision(ID=ID)

    return jsonify( decision_text=predictDecision(ID=ID))

# @app.route("/ClientID", methods = ['GET'])
# def predict3():
#     # Liste des identifiants de tous les clients dans le dataset
#     all_id_client = list(lecture_X_test_original()['sk_id_curr'])
#     # Récupération de l'ID du client dans l'URL
#     ID = request.args['id_client']
#     ID = int(ID)
# 
#  
#     y_pred_lgbm = model_LGBM.predict(lecture_X_test_clean().drop(labels="sk_id_curr", axis=1))    # Prédiction de la classe 0 ou 1
#     y_pred_lgbm_proba = model_LGBM.predict_proba(lecture_X_test_clean().drop(labels="sk_id_curr", axis=1)) # Prédiction du % de risque
# 
#     # Récupération du score du client
#     y_pred_lgbm_proba_df = pd.DataFrame(y_pred_lgbm_proba, columns=['proba_classe_0', 'proba_classe_1'])
#     y_pred_lgbm_proba_df = pd.concat([y_pred_lgbm_proba_df['proba_classe_1'],
#                                     lecture_X_test_clean()['sk_id_curr']], axis=1)
#     
#     y_pred_lgbm_df = pd.DataFrame(y_pred_lgbm, columns=['prediction'])
#     y_pred_lgbm_df = pd.concat([y_pred_lgbm_df, lecture_X_test_clean()['sk_id_curr']], axis=1)
#     y_pred_lgbm_df['client'] = np.where(y_pred_lgbm_df.prediction == 1, "non solvable", "solvable")
#     y_pred_lgbm_df['decision'] = np.where(y_pred_lgbm_df.prediction == 1, "refuser", "accorder")
# 
# 
# 
#     # Vérification que l'ID est présent dans la liste des clients du dataset
#     if ID not in all_id_client:
#         # Si l'ID n'est pas valide, renvoie une réponse avec des valeurs "NA"
#         number="L'identifiant que vous avez saisi n'est pas valide !"
#         prediction="NA"
#         solvabilite="NA"
#         decision="NA"
#     else :
#         # Si l'ID est valide, récupère la prédiction de décision pour ce client
#         number=""
#         score = y_pred_lgbm_proba_df[y_pred_lgbm_proba_df['sk_id_curr']==ID]
#         prediction = round(score.proba_classe_1.iloc[0]*100, 1)
#         solvabilite = y_pred_lgbm_df.loc[y_pred_lgbm_df['sk_id_curr']==ID, "client"].values
#         solvabilite = solvabilite[0]
#         decision = y_pred_lgbm_df.loc[y_pred_lgbm_df['sk_id_curr']==ID, "decision"].values
#         decision = decision[0]
#     # Retourne une réponse JSON avec la prédiction de décision
#     return jsonify(identifiant_text=ID)

host = '0.0.0.0'
port = 5003
#local host : http://127.0.0.1:5003
#host=host,port=port
if __name__ == "__main__":
     app.run(debug=False)