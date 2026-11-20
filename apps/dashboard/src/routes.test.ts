import { describe, expect, it } from "vitest";
import { alertIdFromHash, routeFromHash } from "./routes";

describe("dashboard hash routes", () => {
  it("uses the alerts route for a directly opened alert detail", () => {
    expect(routeFromHash("#/alerts/alert-123")).toBe("alerts");
  });

  it("extracts the alert identifier from a detail URL", () => {
    expect(alertIdFromHash("#/alerts/alert-123")).toBe("alert-123");
  });

  it("returns no alert identifier for the inbox route", () => {
    expect(alertIdFromHash("#/alerts")).toBeUndefined();
  });

  it("falls back to live for an unknown route", () => {
    expect(routeFromHash("#/not-a-route")).toBe("live");
  });
});
