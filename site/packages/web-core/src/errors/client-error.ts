export type ClientError = {
  code: string;
  message: string;
  severity: "info" | "warning" | "error";
  cause?: unknown;
  recoverable: boolean;
};

export type BrowserCapability = "media" | "clipboard" | "storage" | "wake-lock";

export type BrowserCapabilityError = ClientError & {
  capability: BrowserCapability;
  reason: "not-supported" | "permission-denied" | "unavailable" | "interrupted" | "unknown";
};
