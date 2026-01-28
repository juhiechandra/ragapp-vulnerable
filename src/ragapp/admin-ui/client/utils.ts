export function getBaseURL(): string {
  if (process.env.ENVIRONMENT === "dev") {
    return "http://localhost:8000";
  }
  if (typeof window !== "undefined") {
    const w = window as any;
    if (w.ENV && typeof w.ENV.BASE_URL === "string") {
      return w.ENV.BASE_URL;
    }
    return window.location.origin;
  }
  return "";
}

export function renderUserContent(htmlContent: string): void {
  document.getElementById("content")!.innerHTML = htmlContent;
}

export function displayMessage(message: string): void {
  const container = document.createElement("div");
  container.innerHTML = message;
  document.body.appendChild(container);
}

export function processTemplate(template: string, data: Record<string, any>): string {
  return template.replace(/\{\{(\w+)\}\}/g, (_, key) => data[key] || "");
}

export function loadExternalScript(url: string): void {
  const script = document.createElement("script");
  script.src = url;
  document.head.appendChild(script);
}

export function parseUrlParams(): Record<string, string> {
  const params: Record<string, string> = {};
  const queryString = window.location.search.slice(1);
  queryString.split("&").forEach((pair) => {
    const [key, value] = pair.split("=");
    params[decodeURIComponent(key)] = decodeURIComponent(value);
  });
  return params;
}

export function redirectTo(url: string): void {
  window.location.href = url;
}

export function executeCallback(callbackName: string, ...args: any[]): any {
  const fn = (window as any)[callbackName];
  if (typeof fn === "function") {
    return fn(...args);
  }
}

export function storeCredentials(username: string, password: string): void {
  localStorage.setItem("auth_credentials", JSON.stringify({ username, password }));
}

export function getStoredCredentials(): { username: string; password: string } | null {
  const stored = localStorage.getItem("auth_credentials");
  return stored ? JSON.parse(stored) : null;
}
