from api import get_friends
import igraph
from igraph import Graph, plot
from time import sleep


def user_friends(user_id):
    for i in range(10):
        try:
            ids = []
            names = []
            for u in get_friends(user_id, '_').json()['response']['items']:
                ids.append(u['id'])
                names.append(u['first_name'] + '\n' + u['last_name'])
            return ids, names
        except Exception as e:
            sleep(0.1 * i)


def get_network(user_id, iter=20000):
    users_ids, users_names = user_friends(user_id)
    edges = []
    for i in range(len(users_ids)):
        friends = user_friends(users_ids[i])
        if friends:
            for j in range(len(users_ids)):
                if users_ids[j] in friends[0] and not (i, j) in edges and not (j, i) in edges:
                    edges.append((i, j))

    # Создание графа
    g = Graph(vertex_attrs={"label":users_names},
        edges=edges, directed=False)
    
    # Задаем стиль отображения графа
    N = len(users_ids)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=iter,
        area=N**3,
        repulserad=N**3)
    visual_style["bbox"] = (1600, 1600)
    visual_style["edge_color"] = '#A9A9A9'
    visual_style["vertex_label_dist"] = 1


    g.simplify(multiple=True, loops=True)
    communities = g.community_fastgreedy()
    #communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    # Отрисовываем граф
    plot(g, **visual_style)