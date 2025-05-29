import { NextResponse } from 'next/server';
import axios from 'axios';

// Handle both GET and POST requests
export async function GET(request) {
  return handleQRGeneration(request);
}

export async function POST(request) {
  return handleQRGeneration(request);
}

async function handleQRGeneration(request) {
  const { searchParams } = new URL(request.url);
  const url = searchParams.get('url');
  
  console.log('Received URL:', url); // Debug log
  
  if (!url) {
    return NextResponse.json({ error: 'URL is required' }, { status: 400 });
  }

  try {
    // Try different backend endpoints.
    const backendUrls = [
      `http://qr-api-service.default.svc.cluster.local/generate-qr?url=${encodeURIComponent(url)}`,
      `http://qr-api-service/generate-qr?url=${encodeURIComponent(url)}`,
      `http://qr-api-service:80/generate-qr?url=${encodeURIComponent(url)}`
    ];

    let lastError;
    
    for (const backendUrl of backendUrls) {
      try {
        console.log('Trying backend URL:', backendUrl); // Debug log
        
        const response = await axios.post(backendUrl, {}, {
          timeout: 10000, // 10 second timeout
          headers: {
            'Content-Type': 'application/json'
          }
        });
        
        console.log('Backend response:', response.data); // Debug log
        return NextResponse.json(response.data);
        
      } catch (error) {
        console.error(`Failed with ${backendUrl}:`, error.message);
        lastError = error;
        continue;
      }
    }
    
    throw lastError;
    
  } catch (error) {
    console.error('Error generating QR Code:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      url: error.config?.url
    });
    
    return NextResponse.json({ 
      error: 'Failed to generate QR Code',
      details: error.message,
      backend_error: error.response?.data
    }, { status: 500 });
  }
}