import { describe, expect, it } from "vitest";
import { findMotionRegions } from "./motionDetection";

const width = 32;
const height = 24;

function frame(fill = 0): Uint8ClampedArray {
  const data = new Uint8ClampedArray(width * height * 4);
  for (let pixel = 0; pixel < width * height; pixel += 1) {
    const channel = pixel * 4;
    data[channel] = fill;
    data[channel + 1] = fill;
    data[channel + 2] = fill;
    data[channel + 3] = 255;
  }
  return data;
}

function paintBlock(data: Uint8ClampedArray, x: number, y: number, blockWidth: number, blockHeight: number) {
  for (let row = y; row < y + blockHeight; row += 1) {
    for (let column = x; column < x + blockWidth; column += 1) {
      const channel = (row * width + column) * 4;
      data[channel] = 255;
      data[channel + 1] = 255;
      data[channel + 2] = 255;
    }
  }
}

describe("local motion regions", () => {
  it("returns no regions for an unchanged frame", () => {
    const image = frame();
    expect(findMotionRegions(image, image, width, height)).toEqual([]);
  });

  it("returns a region around a sufficiently large changed area", () => {
    const previous = frame();
    const current = frame();
    paintBlock(current, 8, 6, 8, 7);

    expect(findMotionRegions(current, previous, width, height)).toEqual([
      { x: 8, y: 6, width: 8, height: 7, changedPixels: 56 },
    ]);
  });

  it("ignores isolated sensor noise and whole-frame lighting changes", () => {
    const previous = frame();
    const noise = frame();
    paintBlock(noise, 4, 4, 1, 1);
    expect(findMotionRegions(noise, previous, width, height)).toEqual([]);
    expect(findMotionRegions(frame(255), previous, width, height)).toEqual([]);
  });

  it("rejects malformed frame dimensions", () => {
    expect(() => findMotionRegions(new Uint8ClampedArray(4), new Uint8ClampedArray(4), 2, 2))
      .toThrow(RangeError);
  });
});
