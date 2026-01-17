import * as React from "react";

export function Select({ value, onValueChange, children }) {
  return (
    <select
      value={value}
      onChange={(e) => onValueChange(e.target.value)}
      className="w-full rounded-md border px-3 py-2 text-sm"
    >
      {children}
    </select>
  );
}

export function SelectItem({ value, children }) {
  return <option value={value}>{children}</option>;
}

/* Dummy exports to match imports (safe no-op) */
export function SelectTrigger({ children }) {
  return <>{children}</>;
}

export function SelectValue() {
  return null;
}

export function SelectContent({ children }) {
  return <>{children}</>;
}
