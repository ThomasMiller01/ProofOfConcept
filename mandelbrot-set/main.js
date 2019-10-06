let minValue = -2;
let maxValue = 2;

let speed = 20;

let zoom = 100;

let xPos = -1.64999841099374081749002483162428393452822172335808534616943930976364725846655540417646727085571962736578151132907961927190726789896685696750162524460775546580822744596887978637416593715319388030232414667046419863755743802804780843375;
let yPos = -0.00000000000000165712469295418692325810961981279189026504290127375760405334498110850956047368308707050735960323397389547038231194872482690340369921750514146922400928554011996123112902000856666847088788158433995358406779259404221904755;

// let zoom = 1e2;

// let xPos = 0;
// let yPos = 0;

let maxIterations = 240;
let escapeInterations = 16;

let w;
let h;

function setup() {
  createCanvas(600, 600);
  pixelDensity(1);

  w = width;
  h = height;
}

function draw() {
  zoom += (zoom * 1.5) / speed;

  loadPixels();
  for (let x = 0; x < w; x++) {
    for (let y = 0; y < h; y++) {
      // let a = map(x, 0, w, minValue, maxValue) / zoom;
      // let b = map(y, 0, h, minValue, maxValue) / zoom;

      let cX = xPos + (x - (w >> 1)) / zoom;
      let cY = yPos + (y - (h >> 1)) / zoom;

      let a = cX;
      let b = cY;

      let ca = a;
      let cb = b;

      let n = 0;

      for (n = 0; n < maxIterations; n++) {
        let aa = a * a - b * b;
        let bb = 2 * a * b;

        a = aa + ca;
        b = bb + cb;

        if (abs(a - b) > escapeInterations) {
          break;
        }

        n++;
      }

      // --- coloring ---
      // let rgb = color_grey(n)
      let rgb = color_rgb(n);
      // let rgb = color_weird(n, a, b);

      var pix = (x + y * w) * 4;
      pixels[pix + 0] = rgb.r;
      pixels[pix + 1] = rgb.g;
      pixels[pix + 2] = rgb.b;
      pixels[pix + 3] = 255;
    }
  }
  updatePixels();
  // noLoop();
}
