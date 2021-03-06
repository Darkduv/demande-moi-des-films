# coding: utf-8

# All the recommandation logic and algorithms goes here

# from random import choice

from app.User import User


class Recommendation:

    def __init__(self, movielens):

        # Dictionary of movies
        # The structure of a movie is the following:
        #     * id (which is the movie number, you can access to the movie with "self.movies[movie_id]")
        #     * title
        #     * release_date (year when the movie first aired)
        #     * adventure (=1 if the movie is about an adventure, =0 otherwise)
        #     * drama (=1 if the movie is about a drama, =0 otherwise)
        #     * ... (the list of genres)
        self.movies = movielens.movies

        # List of ratings
        # The structure of a rating is the following:
        #     * movie (with the movie number)
        #     * user (with the user number)
        #     * is_appreciated (in the case of simplified rating, whether or not the user liked the movie)
        #     * score (in the case of rating, the score given by the user)
        self.ratings = movielens.simplified_ratings

        # This is the set of users in the training set
        self.test_users = {}

        # Launch the process of ratings
        self.process_ratings_to_users()

    # To process ratings, users associated to ratings are created and every rating is then stored in its user
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            movie = self.movies[rating.movie]
            if hasattr(rating, 'is_appreciated'):
                if rating.is_appreciated:
                    user.good_ratings.append(movie)
                else:
                    user.bad_ratings.append(movie)
            if hasattr(rating, 'score'):
                user.ratings[movie.id] = rating.score

    # Register a user if it does not exist and return it
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Display the recommendation for a user
    def make_recommendation(self, user):
        # movie = choice(list(self.movies.values())).title

        sim = self.compute_all_similarities(user)
        sim.sort(key=lambda x: x[0], reverse=True)
        sosie = sim[0][1]  # utilisateur avec le plus de similarité

        movies = [movie.title for movie in sosie.good_ratings]

        return "Vos recommandations : " + ", ".join(movies)

    # Compute the similarity between two users
    @staticmethod
    def get_similarity(user_a, user_b):
        scal = 0
        for a in user_a.good_ratings:
            scal += a in user_b.good_ratings
            scal -= a in user_b.bad_ratings
        for a in user_a.bad_ratings:
            scal -= a in user_b.good_ratings
            scal += a in user_b.bad_ratings
        return scal / (Recommendation.get_user_norm(user_a) * Recommendation.get_user_norm(user_b)) if scal != 0 else 0

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        return [(self.get_similarity(user, user2), user2) for user2 in self.test_users.values()]

    @staticmethod
    def get_best_movies_from_users(users):
        return []

    @staticmethod
    def get_user_appreciated_movies(user):
        return []

    @staticmethod
    def get_user_norm(user):
        return (len(user.good_ratings) + len(user.bad_ratings)) ** 0.5

    # Return a vector with the normalised ratings of a user
    @staticmethod
    def get_normalised_cluster_notations(user):
        return []
