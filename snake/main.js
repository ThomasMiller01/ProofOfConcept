let gridSize = 30;

let snake;

let dirDict = ["up", "right", "down", "left"];

let currentDir = dirDict[Math.floor(Math.random() * dirDict.length)];

let i = 0;

function setup() {
  createCanvas(800, 800);
  snake = new Snake(3, 6, width / gridSize);
}

function draw() {
  if (i % 20 == 0) {
    if (snake.isAlive()) {
      background("black");
      snake.update(currentDir);
      snake.draw();
    } else {
      noLoop();
    }
  }
  i++;
}

function keyPressed() {
  if (keyCode === UP_ARROW) {
    currentDir = dirDict[0];
  } else if (keyCode === RIGHT_ARROW) {
    currentDir = dirDict[1];
  } else if (keyCode === DOWN_ARROW) {
    currentDir = dirDict[2];
  } else if (keyCode === LEFT_ARROW) {
    currentDir = dirDict[3];
  }
}
