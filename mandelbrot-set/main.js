let minValue = -2;
let maxValue = 2;

let scale = 1;

let maxIterations = 1000;
let escapeInterations = 16;

let w;
let h;

let j = 0;

function setup() {
  createCanvas(500, 500);
  pixelDensity(1);

  w = width;
  h = height;
}

function draw() {
  if (j % 75 == 0) {
    scale *= 2;

    loadPixels();
    for (let x = 0; x < w; x++) {
      for (let y = 0; y < h; y++) {
        // let a = map(x, 0, w, minValue / scale, maxValue / scale);
        // let b = map(y, 0, h, minValue / scale, maxValue / scale);

        let a = map(x, 0, w, minValue, maxValue);
        let b = map(y, 0, h, minValue, maxValue);

        let ca = a;
        let cb = b;

        let n = 0;

        while (n < maxIterations) {
          let aa = a * a - b * b;
          let bb = 2 * a * b;

          a = aa + ca;
          b = bb + cb;

          if (abs(a - b) > escapeInterations) {
            break;
          }

          n++;
        }

        // color
        let rgb = color3(n, a * a, b * b);

        var pix = (x + y * w) * 4;
        pixels[pix + 0] = rgb[0];
        pixels[pix + 1] = rgb[1];
        pixels[pix + 2] = rgb[2];
        pixels[pix + 3] = 255;
      }
    }
    updatePixels();
    noLoop();
  }
  j++;
}

function color1(n) {
  let bright = map(n, 0, maxIterations, 0, 1);
  bright = map(sqrt(bright), 0, 1, 0, 255);

  if (n == maxIterations) {
    bright = 0;
  }

  return [bright, bright, bright];
}

function color2(n) {
  let hue = (255 * n) / maxIterations;
  let saturation = 255;
  let value = n < maxIterations ? 255 : 0;

  let rgb = HSVtoRGB(hue, saturation, value);
  return [rgb.r, rgb.g, rgb.b];
}

function color3(i, r, c) {
  var di = i;
  var hue;

  zn = Math.sqrt(r + c);
  hue = di + 1.0 - Math.log(Math.log(Math.abs(maxIterations))) / Math.log(2.0); // 2 is escape radius
  hue = 0.95 + 20.0 * hue; // adjust to make it prettier
  // the hsv function expects values from 0 to 360
  while (hue > 360.0) hue -= 360.0;
  while (hue < 0.0) hue += 360.0;

  let rgb = HSVtoRGB(hue, 0.8, 1.0);
  return [rgb.r, rgb.b, rgb.b];
}
