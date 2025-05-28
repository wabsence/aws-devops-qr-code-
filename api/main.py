from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import boto3
import os
from io import BytesIO
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Loading Environment variable (AWS Access Key and Secret Key)
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allowing CORS for local testing
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debug: Check if environment variables are loaded
logger.info(f"AWS_ACCESS_KEY loaded: {'Yes' if os.getenv('AWS_ACCESS_KEY') else 'No'}")
logger.info(f"AWS_SECRET_KEY loaded: {'Yes' if os.getenv('AWS_SECRET_KEY') else 'No'}")

# AWS S3 Configuration
try:
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name='us-east-1'  # Add default region
    )
    logger.info("S3 client created successfully")
except Exception as e:
    logger.error(f"Failed to create S3 client: {str(e)}")

bucket_name = 'qrcode-storage-devops-bucket'  # Add your bucket name here

@app.post("/generate-qr/")
async def generate_qr(url: str):
    logger.info(f"Received request to generate QR for URL: {url}")
    
    try:
        # Generate QR Code
        logger.info("Generating QR code...")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        logger.info("QR code image generated successfully")
        
        # Save QR Code to BytesIO object
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        logger.info("QR code converted to BytesIO")

        # Generate file name for S3 (sanitize the filename)
        # sanitized_url = url.replace("://", "_").replace("/", "_").replace("?", "_").replace("&", "_")
        # file_name = f"qr_codes/{sanitized_url}.png"
        file_name = f"qr_codes/{url.split('//')[-1]}.png"
        logger.info(f"File name: {file_name}")

        # Upload to S3
        logger.info("Attempting to upload to S3...")
        s3.put_object(
            Bucket=bucket_name, 
            Key=file_name, 
            Body=img_byte_arr, 
            ContentType='image/png',
            ACL='public-read'
            
        
        )
        logger.info("Successfully uploaded to S3")
        
        # Generate the S3 URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        logger.info(f"Generated S3 URL: {s3_url}")
        
        return {"qr_code_url": s3_url}
        
    except Exception as e:
        logger.error(f"Error in generate_qr: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Add a health check endpoint
@app.get("/")
async def health_check():
    return {"status": "API is running"}

# Add an endpoint to test S3 connection
@app.get("/test-s3")
async def test_s3():
    try:
        # Try to list buckets to test connection
        response = s3.list_buckets()
        return {"status": "S3 connection successful", "buckets": [bucket['Name'] for bucket in response['Buckets']]}
    except Exception as e:
        logger.error(f"S3 connection test failed: {str(e)}")
        return {"status": "S3 connection failed", "error": str(e)}