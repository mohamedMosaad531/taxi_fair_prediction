import pickle

def get_model():    

    with open (r'D:\taki_fair_prediction\models\production_model.pkl','rb') as f:
        model=pickle.load(f)
    return model
