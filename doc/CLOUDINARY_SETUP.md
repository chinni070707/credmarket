# Cloudinary Setup for Media Storage

## Problem
Profile pictures and other uploaded files return 404 errors in production because Render uses ephemeral filesystem (files are deleted on each deployment).

## Solution
Use Cloudinary for permanent media storage.

## Setup Steps

### 1. Create Cloudinary Account (Free)

1. Go to https://cloudinary.com/users/register_free
2. Sign up (free tier includes 25GB storage, 25GB bandwidth/month)
3. After signup, go to Dashboard: https://console.cloudinary.com/

### 2. Get Your Credentials

From the Cloudinary Dashboard, copy:
- **Cloud Name**: (e.g., `dmxyz123`)
- **API Key**: (e.g., `123456789012345`)
- **API Secret**: (e.g., `abcdefghijklmnopqrstuvwxyz`)

### 3. Add to Render Environment Variables

1. Go to Render Dashboard: https://dashboard.render.com
2. Select your `credmarket` web service
3. Go to **Environment** tab
4. Add these variables:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key  
CLOUDINARY_API_SECRET=your_api_secret
```

4. Click **Save Changes**

### 4. Redeploy

The service will automatically redeploy with new environment variables.

## How It Works

- **Before**: Files saved to `/media/` folder (deleted on redeploy)
- **After**: Files uploaded to Cloudinary CDN (permanent, globally distributed)

## Code Changes Made

1. **requirements.txt**: Added `django-cloudinary-storage>=0.3.0`
2. **settings.py**: 
   - Added `cloudinary_storage` to `INSTALLED_APPS`
   - Configured Cloudinary settings
   - Set `DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'`

## Testing

1. After setup, upload a new profile picture
2. Image URL will be: `https://res.cloudinary.com/your-cloud-name/image/upload/...`
3. Images persist across deployments

## Important Notes

- **Existing images**: Old images in `/media/` folder are lost (need to re-upload)
- **Free tier limits**: 25GB storage, 25GB bandwidth/month (plenty for most use cases)
- **URLs change**: Cloudinary URLs are different from `/media/` URLs
- **Automatic optimization**: Cloudinary automatically optimizes images

## Local Development

Cloudinary works in both local and production:
- If credentials are set → uses Cloudinary
- If not set → uses local `/media/` folder

## Troubleshooting

### Images still show 404
1. Check environment variables are set correctly
2. Verify Cloudinary credentials are valid
3. Redeploy the application
4. Re-upload the image

### Old images missing
- Old images in `/media/` were on ephemeral storage and are gone
- Users need to re-upload profile pictures
- This is a one-time migration issue

## Cloudinary Dashboard Features

- View all uploaded images
- Manage storage
- Monitor bandwidth usage
- Image transformations (resize, crop, etc.)
- CDN statistics

## Alternative: AWS S3

If you prefer AWS S3 instead of Cloudinary:
1. Install: `django-storages[s3]`
2. Configure: `DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'`
3. Add AWS credentials to environment

Cloudinary is simpler and has better free tier for small projects.
