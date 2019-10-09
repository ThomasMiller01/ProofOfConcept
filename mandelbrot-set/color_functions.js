// grey
function color_grey(n) {
  let bright = map(n, 0, maxIterations, 0, 1);
  bright = map(sqrt(bright), 0, 1, 0, 255);

  if (n == maxIterations) {
    bright = 0;
  }

  return { r: bright, g: bright, b: bright };
}

// rgb
function color_rgb(n) {
  let hue = (255 * n) / maxIterations;
  let saturation = 255;
  let value = n < maxIterations ? 255 : 0;

  let rgb = HSVtoRGB(hue, saturation, value);
  return rgb;
}

// weird
function color_weird(n, aa, bb) {
  if (n == maxIterations) {
    return { r: 0, g: 0, b: 0 };
  }
  let di = n;
  zn = Math.sqrt(abs(aa + bb));
  hue = di + 1.0 - Math.log(Math.log(Math.abs(zn))) / Math.log(2.0);
  hue = 0.95 + 20.0 * hue;
  if (hue == NaN) {
    console.log("hue", hue);
  }

  let rgb = HSVtoRGB(hue, 0.8, 1.0);
  return rgb;
}

// weird 2
function color_weird2(n, a) {
  let nsmooth = n + 1 - log(Math.log2(abs(a)));
  let hue = (255 * nsmooth) / maxIterations;
  let saturation = 255;
  let value = nsmooth < maxIterations ? 255 : 0;

  let rgb = HSVtoRGB(hue, saturation, value);
  return rgb;
}

// test
function color_test(n) {
  let nsmooth1 = n + 1 - Math.log(Math.log(maxIterations)) / Math.log(2);
  let nsmooth2 = n + 2 - Math.log(Math.log(maxIterations)) / Math.log(2);

  let hue1 = (255 * nsmooth1) / maxIterations;
  let saturation1 = 255;
  let value1 = nsmooth1 < maxIterations ? 255 : 0;

  let rgb1 = HSVtoRGB(hue1, saturation1, value1);

  let hue2 = (255 * nsmooth2) / maxIterations;
  let saturation2 = 255;
  let value2 = nsmooth2 < maxIterations ? 255 : 0;

  let rgb2 = HSVtoRGB(hue2, saturation2, value2);

  let rgb = {};

  let t = map(n, 0, maxIterations, 0, 1);

  rgb["r"] = rgb1.r + (rgb2.r - rgb1.r) * t;
  rgb["g"] = rgb1.g + (rgb2.g - rgb1.g) * t;
  rgb["b"] = rgb1.b + (rgb2.b - rgb1.b) * t;

  return rgb;
}
