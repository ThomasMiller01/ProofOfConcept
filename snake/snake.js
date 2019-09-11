class Snake {
  constructor(x, y, partWidth) {
    this.partWidth = partWidth;
    this.body = [new bodyPart(x, y)];
  }

  isAlive() {
    let isAlive = true;
    this.body.forEach(part => {
      if (
        part.x * this.partWidth >= width - this.partWidth ||
        part.x <= 0 ||
        part.y * this.partWidth >= height - this.partWidth ||
        part.y <= 0
      ) {
        isAlive = false;
      }
    });
    return isAlive;
  }

  update(dir) {
    switch (dir) {
      case "up":
        this.body.forEach(part => {
          part.update(part.x, part.y - 1);
        });
        break;

      case "right":
        this.body.forEach(part => {
          part.update(part.x + 1, part.y);
        });
        break;

      case "down":
        this.body.forEach(part => {
          part.update(part.x, part.y + 1);
        });
        break;

      case "left":
        this.body.forEach(part => {
          part.update(part.x - 1, part.y);
        });
        break;
    }
  }

  draw() {
    this.body.forEach(part => {
      part.draw(this.partWidth);
    });
  }
}

class bodyPart {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  update(x, y) {
    this.x = x;
    this.y = y;
  }

  draw(width) {
    rect(this.x * width, this.y * width, width, width);
  }
}
