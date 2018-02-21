from flask import render_template, request, jsonify
from flaskexample import app
from sklearn.externals import joblib
import pandas as pd 
import plotly
import json
#import plotly.plotly as py
#import plotly.graph_objs as go
### Offline plotly use: 
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.graph_objs import *
init_notebook_mode()

model = joblib.load("C2.pkl")


@app.route('/')
@app.route('/index')
def index():

	df = pd.read_csv('/Users/sunal/Desktop/webapp2/flaskexample/data/sandy.csv')
	labels = df['Category'].unique()
	values = list()
	for i in labels:
		res = df[df['Category'] == i].count()
		values.append(res['ID'])

	needs = df['Resource_or_Need'].unique()
	counts = list()
	for i in needs:
		res = df[df['Resource_or_Need'] == i].count()
		counts.append(res['ID'])


	# graph = dict(
 #        data=[Bar(### for online use go.Bar instead
 #            x=labels,
 #            y=values
 #        )],
 #        layout=dict(
 #            title='Bar Plot of Categories',
 #            yaxis=dict(
 #                title="Count"
 #            ),
 #            xaxis=dict(
 #                title="Categories"
 #            )
 #        )
 #    )
	# graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

	graphs = [dict(
        data=[Bar(### for online use go.Bar instead
            x=labels,
            y=values
        )],
        layout=dict(
            title='Bar Plot of Categories',
            yaxis=dict(
                title="Count"
            ),
            xaxis=dict(
                title="Categories"
            )
        )
    ),
	dict(data=[
    {
      "pull": 0,
      "domain": {
        "y": [
          0,
          1
        ],
        "x": [
          0,
          1
        ]
      },
      "labels": needs,
      "values": counts,
      "hoverinfo": "all",
      "showlegend": False,
      "marker": {
        "colors": [
          "#7fc97f",
          "#f0027f"
        ]
      },
      "textinfo": "label+value",
      "hole": 0,
      "type": "pie",
      "name": "Col2"
    }
  ],
  layout = dict(
    width = 800,
    autosize = False,
    height = 500,
    title =  "Need or Resource"
  )
    )
    ]



	ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
	graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)


	return render_template('master.html', ids = ids, graphJSON = graphJSON)


@app.route('/go')
def go():
    query = request.args.get('query', '') #key-value pairs 

    result_class = model.predict(pd.Series(query))
    recommend = list()
    water_recommendations = 'Water Supply'
    if result_class == 'Water':
    	recommend.append(water_recommendations)
    	
    return render_template(
        'go.html',
        query = query,
        cat = result_class,
        recommend = recommend
    )
