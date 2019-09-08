class Graph {
  constructor(noOfVertices) {
    this.noOfVertices = noOfVertices;
    this.nodePos = new Map();
    this.nodes = new Map();
  }

  addVertex(node) {
    this.nodePos.set(node.name, new Pos(node.x, node.y));
    this.nodes.set(node.name, []);
  }

  addEdge(startNode, endNode, weight) {
    this.nodes.get(startNode).push(new Edge(endNode, weight));
    this.nodes.get(endNode).push(new Edge(startNode, weight));
  }
}

class Node {
  constructor(name, x, y) {
    this.name = name;
    this.x = x;
    this.y = y;
    this.dist = null;
    this.parent = null;
  }
}

class Edge {
  constructor(name, weight) {
    this.name = name;
    this.weight = weight;
  }
}

class Pos {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}
