class Block {
  constructor(x, w, m, v, xc) {
    this.x = x;
    this.y = height - w;
    this.w = w;
    this.v = v;
    this.m = m;
    this.xConstraint = xc;
  }

  update() {
    this.x += this.v;
  }

  show() {
    const x = constrain(this.x, this.xConstraint, width);
    rect(x, this.y, this.w, this.w);
  }

  collide(block) {
    return !(this.x + this.w < block.x || this.x > block.x + block.w);
  }

  hitWall() {
    return this.x <= 0;
  }

  reverse() {
    this.v *= -1;
  }

  bounce(block) {
    let sumM = this.m + block.m;
    let newV = ((this.m - block.m) / sumM) * this.v;
    newV += ((2 * block.m) / sumM) * block.v;
    return newV;
  }
}
