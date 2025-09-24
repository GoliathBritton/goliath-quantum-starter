import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ message: 'DSP API Endpoint - Compatible with n8n and UiPath' });
}