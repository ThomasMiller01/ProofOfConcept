class Node {
  constructor(pos, walkable) {
    this.x = pos.x;
    this.y = pos.y;
    this.walkable = walkable;
    this.width = 40;
    this.g = Infinity;
    this.h = Infinity;
    this.parent = null;
  }

  f() {
    return this.g + this.h;
  }

  draw(state) {
    switch (state) {
      case "normal":
        if (this.walkable) {
          stroke("black");
          fill("white");
        } else {
          stroke("black");
          fill("red");
        }
        break;
      case "current":
        stroke("black");
        fill("blue");
        break;
      case "visited":
        stroke("black");
        fill("grey");
        break;
      case "path":
        stroke("black");
        fill("yellow");
        break;
      default:
        break;
    }
    rect(this.x * this.width, this.y * this.width, this.width, this.width);
    fill("black");
    text(
      this.f() != Infinity ? this.f() : "-",
      this.x * this.width + 3,
      this.y * this.width + 13
    );
    text(
      this.g != Infinity ? this.g : "-",
      this.x * this.width + 3,
      this.y * this.width + this.width - 3
    );
    text(
      this.h != Infinity ? this.h : "-",
      this.x * this.width + this.width - 12,
      this.y * this.width + this.width - 3
    );
  }
}
