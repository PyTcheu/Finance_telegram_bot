import pickle
import pandas as pd

from sklearn.model_selection import GridSearchCV, cross_validate, cross_val_score, cross_val_predict
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('sao-paulo-properties-april-2019.csv')
df = df.iloc[:,:14]

cols = ['District', 'Negotiation Type', 'Property Type']


filename = 'finalized_model.sav'

hp_model = pickle.load(open(filename, 'rb'))

def model_predict(param_list):
    
    X = pd.DataFrame(get_dummies(param_list, df))
    print(X)
    predicted_price = hp_model.predict(X)

    return predicted_price


def predict_house_price(update, context):
    parameters = " ".join(context.args).split(' ')
    print(parameters)
    final_price = model_predict(parameters)
    update.message.reply_text("O valor previsto para esse imovel é: " + str(final_price))


def get_dummies(data, df):
    df_a = pd.DataFrame(data[:10])
    df_dummies = pd.get_dummies(cols)
    dummies_frame = pd.get_dummies(df.iloc[:,11:14])
    df_dummies = df_dummies.reindex(columns = dummies_frame.columns, fill_value=0)
    
    df_final = pd.concat([df_a, df_dummies], axis=1)
    return df_final