from IPython.display import IFrame
import json
import uuid
import os

#var nodes = [{"label": "Coca Cola", "id": 4014, "title": "{'name': 'Coca Cola'}", "group": "Manufacturer"}, 
#             {"label": "Coke Zero", "id": 4012, "title": "{'name': 'Coke Zero', 'calories': 0}", "group": "Drink"}, 
#             {"label": "Nicole",    "id": 4013, "title": "{'age': 24, 'name': 'Nicole'}", "group": "Person"}, {"label": "Mountain Dew", "id": 4011, "title": "{'name': 'Mountain Dew', 'calories': 9000}", "group": "Drink"}, {"label": "Drew", "id": 4010, "title": "{'age': 20, 'name': 'Drew'}", "group": "Person"}, {"label": "Pepsi", "id": 4015, "title": "{'name': 'Pepsi'}", "group": "Manufacturer"}];
#       var edges = [{"from": 4014, "label": "MAKES", "to": 4012}, {"from": 4013, "label": "LIKES", "to": 4011}, {"from": 4013, "label": "LIKES", "to": 4012}, {"from": 4010, "label": "LIKES", "to": 4011}, {"from": 4015, "label": "MAKES", "to": 4011}];



def vis_network(nodes, edges, physics=False):
    html = """
    <html>
    <head>
      <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
      <meta content="utf-8" http-equiv="encoding">    
      <script type="text/javascript" src="https://thedatasociety.github.io/resources/purl/lab-neo4j/graphdrawer/vis.js"></script>
      <link   type="text/css"       href="https://thedatasociety.github.io/resources/purl/lab-neo4j/graphdrawer/vis.css" rel="stylesheet" >
    </head>
    <body>

    <div id="{id}"></div>

    <script type="text/javascript">
      var nodes = {nodes};
      var edges = {edges};

      var container = document.getElementById("{id}");

      var data = {{
        nodes: nodes,
        edges: edges
      }};

      var options = {{
          nodes: {{
              shape: 'dot',
              size: 25,
              font: {{
                  size: 14
              }}
          }},
          edges: {{
              font: {{
                  size: 14,
                  align: 'middle'
              }},
              color: 'gray',
              arrows: {{
                  to: {{enabled: true, scaleFactor: 0.5}}
              }},
              smooth: {{enabled: false}}
          }},
          physics: {{
              enabled: {physics},
              stabilization: false,              
          }},
         layout: {{
	    randomSeed: 191006,
	    improvedLayout: false
         }}          
      }};

      var network = new vis.Network(container, data, options);

    </script>
    </body>
    </html>
    """

    unique_id = str(uuid.uuid4())
    html = html.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges), physics=json.dumps(physics))

    try:
        os.makedirs('graphs')
    except OSError as e:
        pass
    
    filename = "graphs/graph-{}.html".format(unique_id)

    file = open(filename, "w+")
    file.write(html)
    file.close()

    return IFrame(filename, width="100%", height="400")

def draw(nodes, edges,physics=False, limit=100):
    # The options argument should be a dictionary of node labels and property keys; it determines which property
    # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    # Omitting a node label from the options dict will leave the node unlabeled in the visualization.
    # Setting physics = True makes the nodes bounce around when you touch them!


    return vis_network(nodes, edges, physics=physics)

