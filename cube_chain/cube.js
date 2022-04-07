class Cube {
  constructor(x, y, speed = 1, angle = 45, size = 25, color = "blue") {
    this.pos = createVector(x, y);
    this.speed = speed;
    this.size = size;
    this.color = color;

    let angleRadians = (angle * Math.PI) / 180;
    this.vel = createVector(Math.sin(angleRadians), -Math.cos(angleRadians));
    this.vel.setMag(this.speed);
    this.lastPos = this.pos.copy();
  }

  update() {
    this.lastPos = this.pos.copy();
    this.pos.add(this.vel);
  }

  show() {
    strokeWeight(0);
    fill(this.color);
    rect(this.pos.x, this.pos.y, this.size, this.size);
  }

  check(boundaries) {
    let n = null;

    if (this.pos.x + this.size >= boundaries[0]) {
      n = createVector(-1, 0);
    } else if (this.pos.x <= 0) {
      n = createVector(1, 0);
    } else if (this.pos.y + this.size >= boundaries[1]) {
      n = createVector(0, -1);
    } else if (this.pos.y <= 0) {
      n = createVector(0, 1);
    }

    if (n) {
      n.normalize();
      let reflectionVector = this.calculateReflectionVector(n);
      reflectionVector.setMag(this.speed);
      this.vel = reflectionVector;
    }
  }

  calculateReflectionVector(n) {
    let r = this.pos.copy();
    r.sub(this.lastPos);
    r.reflect(n);
    return r;
  }
}
