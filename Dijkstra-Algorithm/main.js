let graph;
let finished_queue = [];
let calculation_queue = [];

let dists = {};
let parents = {};

let startNode = "A";
let endNode = "F";

let currentNode = startNode;

let _path = [];

let j = 0;

function setup() {
  createCanvas(800, 400);
  init_graph();
  draw_graph();
  init_dijkstra();
}

function draw() {
  if (j % 20 == 0) {
    draw_graph();

    if (calculation_queue.length == 0) {
      console.log("finished!!!");
      finishedPath();
      console.log(_path);
      console.log(parents);
      let lastNode = _path[0];
      _path.forEach(node => {
        stroke("yellow");
        fill("yellow");

        let pos1 = graph.nodePos.get(lastNode);
        let pos2 = graph.nodePos.get(node);
        ellipse(pos2.x, pos2.y, 20, 20);
        ellipse(pos1.x, pos1.y, 20, 20);
        line(pos1.x, pos1.y, pos2.x, pos2.y);
      });
      noLoop();
    } else {
      currentNode = getMin(calculation_queue);
      calculation_queue.splice(calculation_queue.indexOf(currentNode), 1);

      getNeighbours(currentNode).forEach(neighbour => {
        stroke("green");
        fill("green");
        ellipse(
          graph.nodePos.get(neighbour.name).x,
          graph.nodePos.get(neighbour.name).y,
          20,
          20
        );
        let pos1 = graph.nodePos.get(currentNode);
        let pos2 = graph.nodePos.get(neighbour.name);
        stroke("green");
        line(pos1.x, pos1.y, pos2.x, pos2.y);
        updateDist(neighbour);
      });

      stroke("blue");
      fill("blue");
      ellipse(
        graph.nodePos.get(currentNode).x,
        graph.nodePos.get(currentNode).y,
        20,
        20
      );

      stroke("yellow");
      fill("yellow");
      ellipse(
        graph.nodePos.get(startNode).x,
        graph.nodePos.get(startNode).y,
        20,
        20
      );
      ellipse(
        graph.nodePos.get(endNode).x,
        graph.nodePos.get(endNode).y,
        20,
        20
      );
    }
  }
  j++;
}

function finishedPath() {
  _path.push(parents[endNode]);
  let node = endNode;
  while (parents[node] != undefined) {
    u = parents[node];
    _path.push(u);
  }
  _path.reverse();
}

function updateDist(neighbour) {
  let dist = dists[currentNode] + neighbour.weight;
  if (dist < dists[neighbour.name]) {
    dists[neighbour.name] = dist;
    parents[neighbour.name] = currentNode;
  }
}

function getNeighbours(node) {
  console.log(node);
  let neighbours = [];
  for (let edge of graph.nodes.get(node)) {
    neighbours.push({ name: edge.name, weight: edge.weight });
  }
  return neighbours;
}

function getMin(keys) {
  let minKey = keys[0];
  let min = dists[minKey];
  keys.forEach(key => {
    if (min > dists[key] && calculation_queue.indexOf(key) != -1) {
      minKey = key;
      min = dists[minKey];
    }
  });
  return minKey;
}

function init_dijkstra() {
  let q = [];
  graph.nodes.forEach((value, key) => {
    let node = key;
    dists[node] = Infinity;
    parents[node] = null;
    if (node != startNode) {
      q.push(node);
    }
  });
  dists[startNode] = 0;
  calculation_queue = q;
}

function draw_graph() {
  background(0);
  stroke(255);
  fill(255);

  let get_node_keys = graph.nodes.keys();

  for (let node_key of get_node_keys) {
    let edge_nodes = graph.nodes.get(node_key);
    let pos = graph.nodePos.get(node_key);
    ellipse(pos.x, pos.y, 20, 20);
    textSize(20);
    text(node_key, pos.x - 5, pos.y - 15);
    for (let edge_node of edge_nodes) {
      let pos2 = graph.nodePos.get(edge_node.name);
      let center_pos = new Pos((pos.x + pos2.x) / 2, (pos.y + pos2.y) / 2);
      textSize(17);
      text(edge_node.weight, center_pos.x - 5, center_pos.y - 5);
      line(pos.x, pos.y, pos2.x, pos2.y);
    }
  }
}

function init_graph() {
  graph = new Graph();
  let vertices = [
    new Node("A", 50, height / 3),
    new Node("B", (width / 6) * 3, 50),
    new Node("C", (width / 6) * 2, height - 50),
    new Node("D", (width / 6) * 4, (height / 3) * 2),
    new Node("E", (width / 6) * 5, height - 50),
    new Node("F", width - 50, height / 3)
  ];

  for (let i = 0; i < vertices.length; i++) {
    graph.addVertex(vertices[i]);
  }

  graph.addEdge("A", "B", 6);
  graph.addEdge("A", "D", 8);
  graph.addEdge("A", "C", 2);
  graph.addEdge("B", "C", 3);
  graph.addEdge("B", "E", 5);
  graph.addEdge("B", "F", 9);
  graph.addEdge("C", "D", 4);
  graph.addEdge("C", "E", 9);
  graph.addEdge("D", "E", 5);
  graph.addEdge("D", "F", 7);
  graph.addEdge("E", "F", 2);
}
