from flask import Flask, render_template, redirect, request, url_for
from core import analyzer

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():
	if request.method == 'POST':
		try:
			if request.form['filme_base']:
				filme_base = request.form['filme_base']
				return redirect(url_for('consulta',filme = filme_base))
		except Exception as e:
			print(e)
			pass
	return render_template('index.html')

@app.route('/consulta', methods = ['GET','POST'])
def consulta():
	result = analyzer.consulta(request.args['filme'])
	if request.method == 'POST':
		try:
			if request.form['filme']:
				referencia = request.form['filme']
				return redirect(url_for('result', ref = referencia))
		except Exception as e:
			raise e
	return render_template('consulta.html',filmes = result)

@app.route('/result', methods = ['GET','POST'])
def result():
	ref = request.args['ref']
	dicas = analyzer.referencia(ref)
	return render_template('dicas.html', dicas = dicas.values)

if __name__=='__main__':
	app.run(debug=False)