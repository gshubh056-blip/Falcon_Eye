export const routes = [
  ["live", "Live"],
  ["alerts", "Alerts"],
  ["cameras", "Cameras"],
  ["events", "Events"],
  ["database", "Database"],
  ["health", "Health"],
  ["settings", "Settings"],
] as const;

export function routeFromHash(hash: string): string {
  const route = hash.replace(/^#\//, "").split("/")[0];
  return routes.some(([key]) => key === route) ? route : "live";
}

export function alertIdFromHash(hash: string): string | undefined {
  const [route, alertId] = hash.replace(/^#\//, "").split("/");
  return route === "alerts" && alertId ? alertId : undefined;
}
