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
