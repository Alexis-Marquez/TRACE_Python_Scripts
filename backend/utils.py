# wrapper to get URL from a vertex
def getURL(vertex: tuple[str, str]) -> str:
    if not isinstance(vertex, tuple) or len(vertex) != 2:
        raise ValueError(f"Vertex {vertex} is not properly formatted! Format should be a tuple of the form: (url, path)")
    return vertex[0]

# wrapper to get Path from a vertex
def getIP(vertex: tuple[str, str]) -> str:
    if not isinstance(vertex, tuple) or len(vertex) != 2:
        raise ValueError(f"Vertex {vertex} is not properly formatted! Format should be a tuple of the form: (url, path)")
    return vertex[1]
