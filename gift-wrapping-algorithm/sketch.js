let points = [];
let completeShape = [];

let startPoint = null;

let currentPoint = null;
let nextPoint = null;

let index = 0;
let nextIndex = 0;

function setup() {
  createCanvas(800, 800);

  let buffer = 20;

  for (let i = 0; i < 10; i++) {
    let p = createVector(
      random(buffer, width - buffer),
      random(buffer, height - buffer)
    );
    points.push(p);
  }

  points.sort((a, b) => a.x - b.x);

  startPoint = points[0];
  completeShape.push(startPoint);
  currentPoint = startPoint;
  nextPoint = points[1];
  index = 2;
}

function draw() {
  background(0);
  stroke(255);
  strokeWeight(8);
  for (let p of points) {
    point(p.x, p.y);
  }

  stroke(0, 0, 255);
  fill(0, 0, 255, 50);
  beginShape();
  for (let p of completeShape) {
    vertex(p.x, p.y);
  }
  endShape(CLOSE);

  stroke(0, 255, 0);
  strokeWeight(32);
  point(startPoint.x, startPoint.y);

  stroke(0, 255, 0);
  strokeWeight(32);
  point(currentPoint.x, currentPoint.y);

  stroke(0, 255, 0);
  strokeWeight(2);
  line(currentPoint.x, currentPoint.y, nextPoint.x, nextPoint.y);

  let checkingPoint = points[index];
  stroke(255);
  line(currentPoint.x, currentPoint.y, checkingPoint.x, checkingPoint.y);

  let a = p5.Vector.sub(nextPoint, currentPoint);
  let b = p5.Vector.sub(checkingPoint, currentPoint);
  const crossP = a.cross(b);

  if (crossP.z < 0) {
    nextPoint = checkingPoint;
    nextIndex = index;
  }

  index++;

  if (index == points.length) {
    if (nextPoint == startPoint) {
      console.log("done :)");
      noLoop();
    } else {
      completeShape.push(nextPoint);
      currentPoint = nextPoint;
      index = 0;
      nextPoint = startPoint;
    }
  }
}
