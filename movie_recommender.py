import pandas as pd
import ast
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def clean_data():
    metadata = pd.read_csv('movies_metadata.csv', low_memory=False)
    metadata.head()
    metadata.isnull().sum()
    metadata = metadata.dropna(subset=['imdb_id', 'poster_path'])
    metadata = metadata.drop(['belongs_to_collection', 'homepage', 'popularity', 'tagline', 'status'], axis=1)
    metadata = metadata.drop(
        ['runtime', 'release_date', 'original_language', 'production_countries', 'production_companies',
         'spoken_languages', 'video'], axis=1)
    metadata['genres'] = metadata['genres'].apply(lambda x: ast.literal_eval(x))
    metadata['genres'] = metadata['genres'].apply(lambda x: ', '.join([d['name'] for d in x]))
    metadata['imdbURL'] = 'https://www.imdb.com/title/' + metadata['imdb_id'] + '/'
    metadata['tmdbURL'] = 'https://www.themoviedb.org/movie/' + metadata['id']
    metadata['ImageURL'] = 'https://image.tmdb.org/t/p/w92' + metadata['poster_path']
    metadata.isnull().sum()
    metadata.to_csv('metadata_prep.csv')


def get_recommendations(title, df, indices, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices]


def return_cosine_sim():
    metadata = pd.read_csv('metadata_prep.csv')
    tfidf = TfidfVectorizer(stop_words='english')
    metadata['overview'] = metadata['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(metadata['overview'])
    print(tfidf_matrix.shape)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()
    return cosine_sim, metadata, indices


# cosine_sim, metadata, indices = return_cosine_sim()
# a = get_recommendations('Toy Story 2', metadata, indices, cosine_sim)
# result = metadata.loc[a.index]['imdbURL']
#
# print(result)
