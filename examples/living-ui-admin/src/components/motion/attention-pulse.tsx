import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

type AttentionPulseProps = ComponentProps<"div"> & {
  active: boolean;
};

export function AttentionPulse({
  active,
  className,
  ...props
}: AttentionPulseProps) {
  return (
    <div
      className={cn("attention-pulse", className)}
      data-attention-active={active}
      {...props}
    />
  );
}
