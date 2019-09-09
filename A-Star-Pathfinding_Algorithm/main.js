let grid = face;

let nodeGrid = [];

let openSet = [];
let closedSet = [];

let startPos = [0, 0];
let startNode;
let endPos = [14, 14];
let endNode;

let _path = [];

let found = false;

function setup() {
  createCanvas(610, 610);
  for (let y = 0; y < grid.length; y++) {
    nodeGrid.push([]);
    for (let x = 0; x < grid[0].length; x++) {
      let currentNode = new Node(
        { x: x, y: y },
        grid[y][x] == 0 ? true : false
      );
      nodeGrid[y].push(currentNode);
      if (currentNode.x == startPos[0] && currentNode.y == startPos[1]) {
        currentNode.g = 0;
        currentNode.h = 0;
      }
      openSet.push(currentNode);
    }
  }
  startNode = nodeGrid[startPos[1]][startPos[0]];
  endNode = nodeGrid[endPos[1]][endPos[0]];
}

function draw() {
  background(255);
  for (let y = 0; y < nodeGrid.length; y++) {
    for (let x = 0; x < nodeGrid[0].length; x++) {
      nodeGrid[y][x].draw("normal");
    }
  }
  closedSet.forEach(node => {
    node.draw("visited");
  });
  if (openSet.length != 0 || found) {
    let currentNode = openSet[0];
    for (let i = 0; i < openSet.length; i++) {
      if (
        openSet[i].f() < currentNode.f() ||
        (openSet[i] == currentNode.f() && openSet[i].h < currentNode.h)
      ) {
        currentNode = openSet[i];
      }
    }
    currentNode.draw("current");
    openSet.splice(openSet.indexOf(currentNode), 1);
    closedSet.push(currentNode);
    if (currentNode == endNode) {
      found = true;
    } else {
      let neighbours = getNeighbours(currentNode);
      neighbours.forEach(neighbour => {
        if (neighbour.walkable && !closedSet.includes(neighbour)) {
          neighbour.g = currentNode.g + getDist(currentNode, neighbour);
          neighbour.h = getDist(neighbour, endNode);
          neighbour.parent = currentNode;

          if (openSet.includes(neighbour)) {
            if (neighbour.h <= currentNode.g) {
              openSet.push(neighbour);
            }
          }
        }
      });
    }
  }
  if (found) {
    retracePath(startNode, endNode);
    _path.forEach(node => {
      node.draw("path");
    });
    noLoop();
  }
}

function retracePath(startNode, endNode) {
  let currentNode = endNode;
  while (currentNode != startNode) {
    _path.push(currentNode);
    currentNode = currentNode.parent;
  }
  _path.push(startNode);
  _path.reverse();
}

function getDist(nodeA, nodeB) {
  let distX = Math.abs(nodeA.x - nodeB.x);
  let distY = Math.abs(nodeA.y - nodeB.y);

  if (distX > distY) {
    return 14 * distY + 10 * (distX - distY);
  } else {
    return 14 * distX + 10 * (distY - distX);
  }
}

function getNeighbours(node) {
  let neighbours = [];
  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      if (x == 0 && y == 0) {
        continue;
      }
      let checkX = node.x + x;
      let checkY = node.y + y;

      if (
        checkX >= 0 &&
        checkX < nodeGrid[0].length &&
        checkY >= 0 &&
        checkY < nodeGrid.length
      ) {
        neighbours.push(nodeGrid[checkY][checkX]);
      }
    }
  }
  return neighbours;
}
