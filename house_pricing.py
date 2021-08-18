import pickle
import pandas as pd

from sklearn.model_selection import GridSearchCV, cross_validate, cross_val_score, cross_val_predict
from sklearn.ensemble import RandomForestRegressor

raw_data = pd.read_csv('sao-paulo-properties-april-2019.csv')
raw_data = raw_data.iloc[:,:14]
cols = raw_data.iloc[:,1:14].columns

filename = 'finalized_model.sav'

hp_model = pickle.load(open(filename, 'rb'))

def model_predict(param_list):
    
    X = pd.DataFrame(get_dummies(param_list, raw_data))
    predicted_price = hp_model.predict(X)

    return predicted_price


def predict_house_price(update, context):
    parameters = " ".join(context.args).split(' ')
    print(parameters)
    final_price = model_predict(parameters)
    update.message.reply_text("O valor previsto para esse imovel é: " + str(final_price))


def get_dummies(data, df):

    data = pd.DataFrame(data, cols).T
    df_a = data.iloc[:,:10]

    df = df.iloc[:,1:14]

    dummies_frame = pd.get_dummies(df)

    df_b = pd.get_dummies(data)
    df_b = df_b.reindex(columns = dummies_frame.columns, fill_value=0).iloc[:,10:]
    
    df_final = pd.concat([df_a, df_b], axis=1)
    return df_final[0]