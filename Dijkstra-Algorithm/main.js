let graph;
let finished_queue = [];
let calculation_queue = [];

let currentNode;
let currentNeighbours = [];

let lastNode;

function setup() {
  createCanvas(800, 400);
  init_graph();
  draw_graph();
  djikstra("A", "F");
}

function djikstra(start, end) {
  let vertice_keys = graph.nodes.keys();
  for (let vertice_key of vertice_keys) {
    let neighbours = [];
    for (let edge of graph.nodes.get(vertice_key)) {
      neighbours.push({ name: edge.name, weight: edge.weight });
    }
    let amount = Infinity;
    if (vertice_key === start) {
      amount = 0;
    }
    calculation_queue.push({
      name: vertice_key,
      neighbours: neighbours,
      cost: {
        amount: amount,
        name: ""
      }
    });
  }
  calculation_queue.sort(compareNodes);
  currentNode = start;
  currentNeighbours = calculation_queue.find(findNode)["neighbours"];
  calculate_cost();
  do {
    currentNode = calculation_queue[0].name;
    currentNeighbours = calculation_queue.find(findNode)["neighbours"];
    calculate_cost();
  } while (calculation_queue.length != 0);
  let _path = [];
  let tmp_node = finished_queue[getNodeIndex(finished_queue, { name: end })];
  _path.push(tmp_node.name);
  let next = tmp_node["cost"]["name"];
  while (next !== "") {
    let node = finished_queue[getNodeIndex(finished_queue, { name: next })];
    _path.push(node["name"]);
    next = node["cost"]["name"];
  }
  console.log("_path", _path);
}

function calculate_cost() {
  let index;
  currentNeighbours.forEach(neighbour => {
    if (neighbour.name !== lastNode) {
      index = getNodeIndex(calculation_queue, neighbour);
      if (index !== null) {
        let node = calculation_queue[index];
        let currentNodeObj =
          calculation_queue[
            getNodeIndex(calculation_queue, { name: currentNode })
          ];
        let cost;
        let cost_amount_tmp =
          currentNodeObj["cost"]["amount"] + neighbour["weight"];
        if (node["cost"]["amount"] < cost_amount_tmp) {
          cost = {
            amount: node["cost"]["amount"],
            name: currentNodeObj["cost"]["name"]
          };
        } else {
          cost = {
            amount: cost_amount_tmp,
            name: currentNode
          };
        }
        let new_neighbour = {
          name: node["name"],
          neighbours: node["neighbours"],
          cost: cost
        };
        calculation_queue[index] = new_neighbour;
      } else {
        console.log("null");
      }
    }
  });
  let currentNodeIndex = getNodeIndex(calculation_queue, { name: currentNode });
  finished_queue.push(calculation_queue[currentNodeIndex]);
  calculation_queue.splice(currentNodeIndex, 1);
  lastNode = currentNode;
}

function getNodeIndex(list, node) {
  let index = null;
  list.forEach(_node => {
    if (_node.name === node.name) {
      index = list.indexOf(_node);
      return;
    }
  });
  return index;
}

function findNode(node) {
  if (node.name === currentNode) {
    return true;
  }
  return false;
}

function compareNodes(node1, node2) {
  if (node1["cost"]["amount"] > node2["cost"]["amount"]) return 1;
  if (node1["cost"]["amount"] < node2["cost"]["amount"]) return -1;
  if (node1["cost"]["amount"] === node2["cost"]["amount"]) return 0;
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
