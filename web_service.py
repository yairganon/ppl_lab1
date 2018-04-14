import math
from flask import Flask
from flask import jsonify
from flask import request

from backend import get_all_ratings, get_movie

app = Flask(__name__)


@app.route('/rec', methods=['GET'])
def get_user_recommendation():
    return user_recommendation(lambda param: request.args.get(param))


@app.route('/rec', methods=['POST'])
def post_user_recommendation():
    return user_recommendation(lambda param: request.form[param])


def user_recommendation(get_data):
    current_user = get_data("userid")
    k = int(get_data("k"))
    data = get_all_ratings()
    users_id = set([row[0] for row in data if row[0] != current_user])
    k_users = [row[0] for row in sorted([(user_id, user_sim(current_user, user_id, data)) for user_id in users_id],
                                        key=lambda o: o[1],
                                        reverse=True)[:k]]
    movies_id = []
    for user_id in k_users:
        for movie_id in sorted_user_ratings(user_id, data):
            if movie_id not in movies_id:
                movies_id.append(movie_id)
                break
    return jsonify([get_movie(movie_id)[1] for movie_id in movies_id])


def user_sim(u, n, data):
    u_data = [(row[1], float(row[2])) for row in data if row[0] == u]
    n_data = [(row[1], float(row[2])) for row in data if row[0] == n]
    u_data_movies = [row[0] for row in u_data]
    n_data_movies = [row[0] for row in n_data]
    common_movies = [movie for movie in u_data_movies if movie in n_data_movies]
    common_ratings = [(user_rating(movie, u_data), user_rating(movie, n_data)) for movie in common_movies]
    if common_ratings:
        ru = sum([data[1] for data in u_data]) / len(u_data)
        rn = sum([data[1] for data in n_data]) / len(n_data)
        counter = sum([(CR[0] - ru) * (CR[1] - rn) for CR in common_ratings])
        f_u = sum([(CR[0] - ru) ** 2 for CR in common_ratings])
        f_n = sum([(CR[1] - rn) ** 2 for CR in common_ratings])
        denominator = ((math.sqrt(f_u if f_u != 0 else 0.1)) *
                       (math.sqrt(f_n if f_n != 0 else 0.1)))
        return counter / denominator
    else:
        return -1


def user_rating(movie, data):
    return next(user_data[1] for user_data in data if user_data[0] == movie)


def sorted_user_ratings(user_id, data):
    return [row[0] for row in
            sorted([(row[1], row[2]) for row in data if row[0] == user_id], key=lambda o: o[1], reverse=True)]


if __name__ == '__main__':
    app.run()
