from autogpt.middlewares.request import Request
from autogpt.middlewares.request_graph import RequestGraph


def test_request_graph():
    single_node_graph = RequestGraph()
    request = Request("a", "simple")
    single_node_graph.add(request)
    assert len(single_node_graph.nodes) == 1
    assert single_node_graph.nodes[0].request == request
    assert single_node_graph.nodes[0].needs == []
