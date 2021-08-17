import pickle

filename = 'finalized_model.sav'

hp_model = pickle.load(open(filename, 'rb'))

def predict_price(cond, size, rooms, toilets, suits, parking, elevator, furnished, pool, new, district, neg_type, prop_type):
    X = [cond, size, rooms, toilets, suits, parking, elevator, furnished, pool, new, district, neg_type, prop_type]

    predicted_price = hp_model.predict(X)

    return predicted_price


def predict_price(update, context):
    parameters = [].join(context.args)
    final_price = predict_price(parameters)
    update.message.reply_text("O valor previsto para esse imovel é: " + str(final_price))
