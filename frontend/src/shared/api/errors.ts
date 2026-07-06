export async function responseErrorMessage(response: Response) {
  try {
    const payload = (await response.json()) as { detail?: unknown; message?: unknown };
    const detail = payload.detail ?? payload.message;
    if (typeof detail === "string" && detail.trim()) return detail;
    if (Array.isArray(detail) && detail.length > 0) {
      return detail
        .map((item) => {
          if (typeof item === "string") return item;
          if (item && typeof item === "object" && "msg" in item) {
            return String((item as { msg: unknown }).msg);
          }
          return String(item);
        })
        .join("；");
    }
  } catch {
    // Fall through to the HTTP status when the server returns non-JSON content.
  }
  return `请求失败：${response.status}`;
}
