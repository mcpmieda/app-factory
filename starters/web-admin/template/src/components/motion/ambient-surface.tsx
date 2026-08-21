import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

type AmbientSurfaceProps = ComponentProps<"div"> & {
  tone?: "hero" | "empty";
};

export function AmbientSurface({
  className,
  tone = "hero",
  ...props
}: AmbientSurfaceProps) {
  return (
    <div
      className={cn("ambient-surface", className)}
      data-motion-surface={tone}
      {...props}
    />
  );
}
