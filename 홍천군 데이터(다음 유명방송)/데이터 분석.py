# 모델 실행 및 플롯 생성
pred = model.predict(np.c_[xx.ravel(), yy.ravel()])
pred = pred.reshape(xx.shape)

fig = px.scatter_3d(df, x='sepal_width', y='sepal_length', z='petal_width')
fig.update_traces(marker=dict(size=5))
camera = dict(eye=dict(x=2.5, y=-2.5, z=1.))
fig.update_layout(width=1000, height=600, margin_l=0, margin_r=0, margin_t=0, margin_b=0, template='plotly_dark', scene_camera=camera)
fig.add_traces(go.Surface(x=xrange, y=yrange, z=pred, name="pred_surface"))
fig.show()

import networkx as nx

#객체 생성
g1 = nx.Graph()

#노드 추가
g1.add_node("a")
g1.add_node(1)
g1.add_node(2)
g1.add_node(3)

g1.add_nodes_from([11, 22])

#노드 제거
g1.remove_node(3)

#엣지 추가
g1.add_edge(1, "a")
g1.add_edge(1, 2)
g1.add_edge(1, 22)

g1.add_edges_from([(1, 2), (1, 11)])

#엣지 제거
g1.remove_edge(1, 22)

#그래프 그리기
nx.draw(g1, with_labels = True, font_weigth = "bold")

#degree 크기에 따른 node size 설정
d = dict(g1.degree)
nx.draw(g1, nodelist = d.keys(), node_size = [v * 100 for v in d.values()], with_labels = True, font_weigth = "bold")

#노드 현황
g1.nodes

#엣지 현황
g1.edges

#degree
g1.degree

#인접
g1.adj

#노드의 개수
g1.number_of_nodes()

#엣지의 개수
g1.number_of_edges()

#요약
print(nx.info(g1))

#객체 생성
g2 = nx.DiGraph()

g2.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])

nx.draw(g2, with_labels = True, font_weigth = "bold")

g2.degree

g2.in_degree

g2.out_degree

g3 = nx.DiGraph() 

g3.add_weighted_edges_from([(1, 2, 3), (2, 3, 4)])
g3.add_edge(1, 3, weight = 6)

pos = nx.spring_layout(g3)
nx.draw(g3, pos = pos, with_labels = True)

labels = nx.get_edge_attributes(g3,'weight')
nx.draw_networkx_edge_labels(g3, pos, edge_labels = labels);