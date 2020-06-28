import pandas as pd

df_filmes = pd.read_csv('core/dataset/movies.csv')
df_notas = pd.read_csv('core/dataset/ratings.csv').drop(columns=['timestamp'])

df_filmes['title'] = df_filmes['title'].str.upper()
df_filmes['genres'] = df_filmes['genres'].str.replace('\-','', regex=True)

def consulta(filme_input):
	result = df_filmes[df_filmes['title'].str.contains(filme_input.upper())]
	return result[['movieId','title']].values

def referencia(result):
	filme_base = df_filmes.query(f'movieId=={result}')
	indicacao = []
	filme_id = int(filme_base['movieId'])
	filme_genre = str(filme_base['genres'].values)
	ref = df_notas.query(f'movieId=={filme_id}').sort_values('rating', ascending=False)['userId'].head()
	
	for user in ref.values:
		indicacao.extend(df_notas.query(f'userId=={user}').sort_values('rating', ascending=False)['movieId'].head().values)

	if df_filmes[df_filmes.movieId.isin(indicacao)&df_filmes.genres.str.match(filme_genre)]['movieId'].count():
		return df_filmes[df_filmes.movieId.isin(indicacao)&df_filmes.genres.str.match(filme_genre)][['title','genres']]
	return df_filmes[df_filmes.movieId.isin(indicacao)].head(15)