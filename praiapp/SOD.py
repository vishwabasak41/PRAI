def objdetect(link):
    from keras.models import load_model
    model=load_model('objdetect.h5')
    from PIL import Image
    import urllib, cStringIO
    file = cStringIO.StringIO(urllib.urlopen(link).read())
    img = Image.open(file)
    from keras.preprocessing.image import load_img,img_to_array
    import numpy as np
    testset=load_img(file,target_size=(224,224))
    x = img_to_array(testset)
    x = np.expand_dims(x, axis=0)
    probabilities=model.predict(x)
    import pickle
    with open('category' + '.pkl', 'rb') as f:
        category= pickle.load(f)
    tempDict = {}
    count = 0
    for eachprob in probabilities[0]:
        tempDict[eachprob] = count
        count = count +1
    top = 0
    # sorting to get top 5 predictions
    topPredictions={}
    for eachkey in sorted(tempDict,reverse=True):
        Name = category[tempDict[eachkey]]
        Percentage = eachkey
        topPredictions[Name]=round(Percentage*100,3)
        if top == 7:
            break
        top = top +1

    del model
    return topPredictions

def preprocess(texts):
    print "inside preprocess"
    from nltk import WordNetLemmatizer
    import string
    wnl=WordNetLemmatizer()
    sentences=[]
    for text in texts:
        text=text.lower()
        toks='.'.join(text.split(' ')).split('.')
        toks=[tok for tok in toks if tok.find('@')==-1]
        toks=[tok for tok in toks if len(tok)>2]
        toks=[wnl.lemmatize(tok) for tok in toks]
        stopwords=open('stopwords.txt').read()
        stopwords=stopwords.split('\n')
        toks=[tok for tok in toks if tok not in stopwords]
        toks=' '.join(toks)
        sentences.append(toks)
    return sentences

def sentiment(text):
    print "inside sentiment"
    from sklearn.externals import joblib
    model=joblib.load('sentiment.pkl')
    print "model",model
    text=preprocess(text)
    senti=model.predict(text)
    del model
    return list(senti)

def analysed(comments,link=None):
    print "in func"
    senti=sentiment(comments)
    print "senti is",senti
    if link==None:
        print "in if"
        return senti
    else:
        objects=objdetect(link)
        return list(objects),senti

def dash(data):
    import numpy as np
    import matplotlib.pyplot as plt
    cols=['anger','boredom','empty','enthusiasm','fun','happiness','hate','love','neutral','relief','sadness','surprise','worry']
    import pickle
    import pandas as pd
    with open('category' + '.pkl', 'rb') as f:
        categories= pickle.load(f)
    categories=list(categories.values())+['TextPost']
    df=pd.DataFrame(index=categories,columns=cols,data=0)
    del categories
    keys=data.keys()
    for key in keys:
        if key=='NO_IMG':
            sent=analysed(data[key])
            df.loc['TextPost',sent]+=1
        else:
            obj,sent=analysed(data[key],key)
            df.loc[obj,sent]+=1
    df["sum"] = df.sum(axis=1)
    df.loc[:,"anger":"worry"] = df.loc[:,"anger":"worry"].div(df["sum"], axis=0)
    return_dict={}
    for col in cols:
        return_dict[col]=list(df[col].sort_values(ascending=False)[:2].index)
    plt.barh(cols,[np.sum(df[col]) for col in cols])
    plt.savefig('Dashboard.png')
    return_dict['File_Name']='Dashboard.png'
    return return_dict

