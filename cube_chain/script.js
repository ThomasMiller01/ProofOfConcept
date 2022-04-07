let cubes = [];
let colors = [
  "#0404F7",
  "#0D3AF7",
  "#1483FC",
  "#1CCCFC",
  "#25FFFF",
  "#5AFFBF",
  "#8EFF87",
  "#C6FF45",
  "#FFFF0B",
  "#F2C109",
  "#EA7907",
  "#E23204",
  "#D70403",
];
let boundaries = [400, 400];

let size = 25;
let baseSpeed = 0.5;
let speedDifference = 0.2;

let startAngle = 45;

function setup() {
  createCanvas(boundaries[0], boundaries[1]);

  for (let i = 0; i < 13; i++) {
    cubes.push(
      new Cube(
        100,
        1,
        (i + 1) * speedDifference + baseSpeed,
        startAngle,
        size,
        colors[i % colors.length]
      )
    );
  }
}

function draw() {
  background(200);

  for (let i = 0; i < cubes.length; i++) {
    let cube = cubes[i];

    if (i < cubes.length - 1) {
      let cubeA = cubes[i];
      let cubeB = cubes[i + 1];
      stroke(50);
      strokeWeight(2);
      line(
        cubeA.pos.x + size / 2,
        cubeA.pos.y + size / 2,
        cubeB.pos.x + size / 2,
        cubeB.pos.y + size / 2
      );
    }

    cube.check(boundaries);
    cube.update();
    cube.show();
  }
}
