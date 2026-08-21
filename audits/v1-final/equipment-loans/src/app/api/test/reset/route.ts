import { NextResponse } from "next/server";

import { resetDemoData } from "@/features/loans/repository";

export async function POST() {
  if (process.env.NODE_ENV === "production") {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  resetDemoData();
  return NextResponse.json({ reset: true });
}
