import pickle
from sklearn.model_selection import GridSearchCV, cross_validate, cross_val_score, cross_val_predict
from sklearn.ensemble import RandomForestRegressor

filename = 'finalized_model.sav'

hp_model = pickle.load(open(filename, 'rb'))

def model_predict(cond, size, rooms, toilets, suits, parking, elevator, furnished, pool, new, district, neg_type, prop_type):
    X = [cond, size, rooms, toilets, suits, parking, elevator, furnished, pool, new, district, neg_type, prop_type]

    predicted_price = hp_model.predict(X)

    return predicted_price


def predict_house_price(update, context):
    parameters = list(" ".join(context.args).split(' '))
    final_price = model_predict(parameters)
    update.message.reply_text("O valor previsto para esse imovel é: " + str(final_price))
