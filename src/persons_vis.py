from lib.constants import *
from lib.logging import logging
import sys
import math

def write_header(title, nodes, edges):

    header = []

    header.append("<!DOCTYPE html>")
    header.append("<html>")
    header.append(" <head>")
    header.append('  <meta charset="UTF-8">')
    header.append(f"  <title>{title}</title>")
    header.append('  <link rel="stylesheet" href="./styles.css" type="text/css">')
    header.append('  <script type="text/javascript" src="./vis-network.min.js"></script>')
    header.append( ' <script type="text/javascript">')
    header.append('     var nodes = null;')
    header.append('     var edges = null;')
    header.append('     var network = null;')
    header.append('     function draw() {')
    header.append(get_graph_data(nodes, edges))
    header.append('        var container = document.getElementById("mynetwork");')
    header.append('        var data = {nodes: nodes, edges: edges};')
    header.append("        var options = { nodes: {shape: 'dot'}};")
    header.append('        network = new vis.Network(container, data, options);')
    header.append('} </script>')
    
    header.append(" </head>")

    return header


def write_footer():

    footer = []
    footer.append(" </body>")
    footer.append("</html>")

    return footer


def get_graph_data(nodes, edges):

    nodes_str = "nodes = [\n"
    for node in nodes:
        nodes_str += node + ",\n"
    nodes_str += "];\n"
        

    edges_str = "edges = [\n"
    for edge in edges:
        edges_str += edge + ",\n"
    edges_str += "];\n"
        

    # nodes = """
    #   nodes = [
    #     {id: 1,  value: 2,  label: 'Algie' },
    #     {id: 2,  value: 31, label: 'Alston'},
    #     {id: 3,  value: 12, label: 'Barney'},
    #     {id: 4,  value: 16, label: 'Coley' },
    #     {id: 5,  value: 17, label: 'Grant' },
    #     {id: 6,  value: 15, label: 'Langdon'},
    #     {id: 7,  value: 6,  label: 'Lee'},
    #     {id: 8,  value: 5,  label: 'Merlin'},
    #     {id: 9,  value: 30, label: 'Mick'},
    #     {id: 10, value: 18, label: 'Tod'},
    #   ]; """

    # edges = """
    #   edges = [
    #     {from: 2, to: 8, value: 3, title: '3 emails per week'},
    #     {from: 2, to: 9, value: 5, title: '5 emails per week'},
    #     {from: 2, to: 10,value: 1, title: '1 emails per week'},
    #     {from: 4, to: 6, value: 8, title: '8 emails per week'},
    #     {from: 5, to: 7, value: 2, title: '2 emails per week'},
    #     {from: 4, to: 5, value: 1, title: '1 emails per week'},
    #     {from: 9, to: 10,value: 2, title: '2 emails per week'},
    #     {from: 2, to: 3, value: 6, title: '6 emails per week'},
    #     {from: 3, to: 9, value: 4, title: '4 emails per week'},
    #     {from: 5, to: 3, value: 1, title: '1 emails per week'},
    #     {from: 2, to: 7, value: 4, title: '4 emails per week'}
    #   ]; """

    data = nodes_str + "\n" + edges_str
    return data


def main():


    TITLE = "GKG Persons Graph (Top 19 Entities)"
    OUTFILE = GRAPH_DIR + "GKG-graph.html"
    search_subtitle = "Filtered on: Organization = US Army  (5464 entries)"
    date_subtitle = "1-FEB-2020 through 16-FEB-2020"

    # load nodes and edges
    node_input_file = GRAPH_DIR + "PersonsNodesTopN.csv"
    edge_input_file = GRAPH_DIR + "PersonsEdgeListTopN.csv"

    # nodes
    with open(node_input_file) as file:
        lines = list(file)

    #  get node scale
    max_node_size = 0
    for line in lines[1:]:
        line = line.strip()
        items = line.split(',')
        node_val_float = float(items[2].strip())
        if node_val_float > max_node_size:
            max_node_size = node_val_float

    print("max node size: " + str(max_node_size))


    nodes = []
    NODE_SCALE = 50
    for line in lines[1:]:
        line = line.strip()
        items = line.split(',')
        node_id = items[0].strip()
        node_value = items[2].strip()
        node_value = round( (float(node_value) / max_node_size) * NODE_SCALE)
        node_label = items[1].strip()
        row = ("{id: " + node_id + ", value: " +
            str(node_value) + ", label: " + "'" + node_label + "'}")
        nodes.append(row)

    #print(str(nodes))

    # edges
    with open(edge_input_file) as file:
        lines = list(file)


    #  get edge scale
    max_edge_size = 0
    for line in lines[1:]:
        line = line.strip()
        items = line.split(',')
        edge_val_float = float(items[2].strip())
        if edge_val_float > max_edge_size:
            max_edge_size = edge_val_float

    print("max edge size: " + str(max_edge_size))

    
    edges = []
    EDGE_SCALE = 10
    for line in lines[1:]:
        line = line.strip()
        items = line.split(',')
        node_from = items[0].strip()
        node_to = items[1].strip()
        edge_value = items[2].strip()
        edge_value = round( (float(edge_value) / max_edge_size) * EDGE_SCALE)
        row = ("{from: " + node_from + ", to: " +
            node_to + ", value: " + str(edge_value) + ", title: " + 
            "'" +  str(edge_value) + "'}")
        edges.append(row)
   
    #print(str(edges))



    # HTML Start
    html = write_header(TITLE, nodes, edges)
    html.append('<body onload="draw()">')

    html.append(f'<h1> {TITLE}</h1>')
    html.append(f'<h2> {date_subtitle}</h2>')
    html.append(f'<h2> {search_subtitle}</h2>')
    html.append('<div id="mynetwork"></div>')


    # CLOSING HTML
    footer = write_footer()
    for line in footer:
        html.append(line)

    logging.info("writing " + OUTFILE)
    with open(OUTFILE, 'w') as f:
        for line in html:
            f.writelines(line + "\n")  

if __name__ == '__main__':
    main()
    print("DONE\n")