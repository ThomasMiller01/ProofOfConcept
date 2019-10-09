// grey
function color_grey(n) {
  let bright = map(n, 0, maxIterations, 0, 1);
  bright = map(sqrt(bright), 0, 1, 0, 255);

  if (n == maxIterations) {
    bright = 0;
  }

  return { r: bright, g: bright, b: bright, a: 255 };
}

// rgb
function color_rgb(n) {
  let hue = (255 * n) / maxIterations;
  let saturation = 255;
  let value = n < maxIterations ? 255 : 0;

  let rgb = HSVtoRGB1(hue, saturation, value);
  rgb["a"] = 255;
  return rgb;
}

// rgb smooth
function color_rgb_smooth(n, aa, bb) {
  if (n == maxIterations) {
    return { r: 0, g: 0, b: 0, a: 255 };
  }

  let nSmooth = 1 + n - Math.log(Math.log(Math.sqrt(aa + bb))) / Math.log(2.0);
  let rgb = HSVtoRGB2((360.0 * nSmooth) / maxIterations, 1.0, 1.0);
  rgb["a"] = 255;
  return rgb;
}

// weird
function color_weird(n, aa, bb) {
  if (n == maxIterations) {
    return { r: 0, g: 0, b: 0, a: 255 };
  }
  let di = n;
  zn = Math.sqrt(abs(aa + bb));
  hue = di + 1.0 - Math.log(Math.log(Math.abs(zn))) / Math.log(2.0);
  hue = 0.95 + 20.0 * hue;
  if (hue == NaN) {
    console.log("hue", hue);
  }

  let rgb = HSVtoRGB1(hue, 0.8, 1.0);
  rgb["a"] = 255;
  return rgb;
}

// weird 2
function color_weird2(n, a) {
  let nsmooth = n + 1 - log(Math.log2(abs(a)));
  let hue = (255 * nsmooth) / maxIterations;
  let saturation = 255;
  let value = nsmooth < maxIterations ? 255 : 0;

  let rgb = HSVtoRGB1(hue, saturation, value);
  rgb["a"] = 255;
  return rgb;
}

// weird 3
function color_weird3(n, aa, bb) {
  if (n == maxIterations) {
    return { r: 0, g: 0, b: 0, a: 255 };
  }

  let nSmooth = 1 + n - Math.log(Math.log(Math.sqrt(aa + bb))) / Math.log(2.0);
  let rgb = HSVtoRGB1((360.0 * nSmooth) / maxIterations, 1.0, 1.0);
  rgb["a"] = 255;
  return rgb;
}

// test
function color_test(n) {
  let nNormalized = (n / maxIterations) * 100;

  let rgb = hslToRgb(0, 1.0, nNormalized);
  rgb["a"] = 255;
  return rgb;
}
