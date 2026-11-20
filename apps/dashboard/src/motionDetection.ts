export type MotionRegion = {
  x: number;
  y: number;
  width: number;
  height: number;
  changedPixels: number;
};

const PIXEL_DIFFERENCE_THRESHOLD = 28;
const MAX_CHANGED_FRACTION = 0.65;
const MAX_REGIONS = 6;

export function findMotionRegions(
  current: Uint8ClampedArray,
  previous: Uint8ClampedArray,
  width: number,
  height: number,
): MotionRegion[] {
  if (!Number.isInteger(width) || !Number.isInteger(height) || width < 1 || height < 1) {
    throw new RangeError("Frame dimensions must be positive integers.");
  }

  const pixelCount = width * height;
  if (current.length !== pixelCount * 4 || previous.length !== pixelCount * 4) {
    throw new RangeError("Frame data length does not match the specified dimensions.");
  }

  const mask = new Uint8Array(pixelCount);
  let changedPixelCount = 0;

  for (let pixel = 0; pixel < pixelCount; pixel += 1) {
    const channel = pixel * 4;
    const currentLuma =
      (current[channel] * 77 + current[channel + 1] * 150 + current[channel + 2] * 29) >> 8;
    const previousLuma =
      (previous[channel] * 77 + previous[channel + 1] * 150 + previous[channel + 2] * 29) >> 8;

    if (Math.abs(currentLuma - previousLuma) >= PIXEL_DIFFERENCE_THRESHOLD) {
      mask[pixel] = 1;
      changedPixelCount += 1;
    }
  }

  if (changedPixelCount / pixelCount > MAX_CHANGED_FRACTION) return [];

  const visited = new Uint8Array(pixelCount);
  const queue = new Int32Array(pixelCount);
  const minRegionPixels = Math.max(14, Math.round(pixelCount * 0.001));
  const regions: MotionRegion[] = [];

  for (let start = 0; start < pixelCount; start += 1) {
    if (!mask[start] || visited[start]) continue;

    let head = 0;
    let tail = 0;
    let minX = width;
    let minY = height;
    let maxX = -1;
    let maxY = -1;
    queue[tail] = start;
    tail += 1;
    visited[start] = 1;

    while (head < tail) {
      const pixel = queue[head];
      head += 1;
      const x = pixel % width;
      const y = Math.floor(pixel / width);
      minX = Math.min(minX, x);
      minY = Math.min(minY, y);
      maxX = Math.max(maxX, x);
      maxY = Math.max(maxY, y);

      for (let offsetY = -1; offsetY <= 1; offsetY += 1) {
        for (let offsetX = -1; offsetX <= 1; offsetX += 1) {
          const neighborX = x + offsetX;
          const neighborY = y + offsetY;
          if (
            (offsetX === 0 && offsetY === 0) ||
            neighborX < 0 ||
            neighborX >= width ||
            neighborY < 0 ||
            neighborY >= height
          ) {
            continue;
          }

          const neighbor = neighborY * width + neighborX;
          if (mask[neighbor] && !visited[neighbor]) {
            visited[neighbor] = 1;
            queue[tail] = neighbor;
            tail += 1;
          }
        }
      }
    }

    const regionWidth = maxX - minX + 1;
    const regionHeight = maxY - minY + 1;
    if (
      tail >= minRegionPixels &&
      regionWidth >= 3 &&
      regionHeight >= 3
    ) {
      regions.push({
        x: minX,
        y: minY,
        width: regionWidth,
        height: regionHeight,
        changedPixels: tail,
      });
    }
  }

  return regions.sort((left, right) => right.changedPixels - left.changedPixels).slice(0, MAX_REGIONS);
}
