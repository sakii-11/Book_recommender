from flask import Flask, render_template,request
import pickle
import numpy as np
import random

application = Flask(__name__)

popular_df = pickle.load(open('pop.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

@application.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['No_ratings'].values),
                           rating=list(popular_df['Avg_ratings'].values)
                           )

@application.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@application.route('/recommend_books' , methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1],
                           reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data = data)


@application.route('/Basedontwo' , methods =['GET', 'POST'])
def Basedonfive_ui():
    return render_template('Basedontwo.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['No_ratings'].values),
                           rating=list(popular_df['Avg_ratings'].values)
                           )

@application.route('/recommend_two_books' , methods =['POST'])
def recommend_two():
    selected_options = request.form.getlist('selected_options')
    a= selected_options[0]
    index = np.where(pt.index == a)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1],
                           reverse=True)[1:5]
    data1 = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data1.append(item)

    b= selected_options[1]
    index = np.where(pt.index == b)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1],
                           reverse=True)[1:5]
    data2 = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data2.append(item)
    intersec= list(filter(lambda x: x in data2, data1))
    if(len(intersec)!=0):
        data = intersec
        return render_template('Basedontwo.html', data = data)
    else:
        data1 += (data2)
        rand = random.sample(data1, 4)
        data = rand
        return render_template('Basedontwo.html', data = data)



if __name__ == '__main__':
    application.run(debug =True)