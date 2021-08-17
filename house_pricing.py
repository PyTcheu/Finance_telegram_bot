import pickle
import pandas as pd

from sklearn.model_selection import GridSearchCV, cross_validate, cross_val_score, cross_val_predict
from sklearn.ensemble import RandomForestRegressor

cols = ['Condo', 'Size', 'Rooms', 'Toilets', 'Suites', 'Parking',
       'Elevator', 'Furnished', 'Swimming Pool', 'New', 'District',
       'Negotiation Type', 'Property Type']


filename = 'finalized_model.sav'

hp_model = pickle.load(open(filename, 'rb'))

def model_predict(param_list):
    X = pd.DataFrame(param_list, columns=cols)

    X = X.reindex(labels = cols, axis = 1, fill_value = 0).drop(columns = ['Price'])
    predicted_price = hp_model.predict(X)

    return predicted_price


def predict_house_price(update, context):
    parameters = " ".join(context.args).split(' ')
    print(parameters)
    final_price = model_predict(parameters)
    update.message.reply_text("O valor previsto para esse imovel é: " + str(final_price))
