# 🚀 Deployment Guide - Step by Step

## ✅ Step 1: GitHub Setup (COMPLETED)
Your code is now on GitHub at: `https://github.com/Mohammed-Saqhib/-Image-Caption-Ai-2.0`

---

## 📦 Step 2: Deploy Frontend to Vercel

### 2.1 Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your GitHub account

### 2.2 Import Your Project
1. After logging in, click **"Add New..."** → **"Project"**
2. You'll see a list of your GitHub repositories
3. Find **"-Image-Caption-Ai-2.0"** and click **"Import"**

### 2.3 Configure Project Settings
When the configuration screen appears:

**Framework Preset:** React (Auto-detected)

**Root Directory:** Click "Edit" and set to: `frontend`

**Build Command:** 
```
npm run build
```

**Output Directory:** 
```
build
```

**Install Command:**
```
npm install
```

### 2.4 Environment Variables
Click **"Environment Variables"** and add:

| Name | Value |
|------|-------|
| `REACT_APP_API_URL` | (Leave empty for now - we'll update this after deploying backend) |

### 2.5 Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes for the build to complete
3. You'll get a URL like: `https://your-project.vercel.app`
4. **Save this URL** - you'll need it later!

---

## 🤗 Step 3: Deploy Backend to Hugging Face Spaces

### 3.1 Create Hugging Face Account
1. Go to [huggingface.co](https://huggingface.co)
2. Click "Sign Up"
3. Complete registration

### 3.2 Create a New Space
1. After logging in, click your profile picture → **"New Space"**
2. Fill in the details:
   - **Space name:** `ai-image-analysis-backend` (or your preferred name)
   - **License:** MIT
   - **Select the SDK:** Choose **"Docker"**
   - **Space hardware:** Choose **"CPU basic (free)"** for now
   - **Visibility:** Public (or Private if you prefer)
3. Click **"Create Space"**

### 3.3 Prepare Backend Files for Hugging Face

You need to create a few files in your backend directory. I'll create them for you.

**Wait for the next steps...**

---

## 🔗 Step 4: Connect Frontend to Backend

After both are deployed:

1. Go to your Vercel project dashboard
2. Go to **Settings** → **Environment Variables**
3. Update `REACT_APP_API_URL` with your Hugging Face Space URL:
   - Format: `https://your-username-ai-image-analysis-backend.hf.space`
4. Go to **Deployments** tab
5. Click the three dots on the latest deployment → **"Redeploy"**
6. Select **"Use existing Build Cache"**
7. Click **"Redeploy"**

---

## ✅ Verification

After deployment:

1. Visit your Vercel URL
2. Login with: username: `admin`, password: `12345`
3. Test all features:
   - Upload an image
   - Try OCR
   - Generate caption
   - Translate text
   - Generate speech

---

## 🎯 Quick Commands Reference

### Local Development
```bash
# Frontend
cd frontend
npm start

# Backend
cd backend
python3 -m uvicorn main:app --reload
```

### Production URLs
- **Frontend:** `https://your-project.vercel.app`
- **Backend:** `https://your-username-backend-space.hf.space`

---

## 🆘 Troubleshooting

### Frontend Issues
- If build fails, check that `frontend` is set as root directory
- Clear build cache and redeploy
- Check browser console for API errors

### Backend Issues
- Check Hugging Face Space logs
- Ensure all dependencies are in requirements.txt
- Verify environment variables are set correctly

### CORS Issues
- Backend is configured to allow all origins
- If issues persist, check middleware.py

---

## 📞 Support

If you encounter any issues:
1. Check the logs in Vercel/Hugging Face dashboards
2. Verify environment variables are set correctly
3. Ensure GitHub repository is up to date

---

**Next Step:** Let me create the necessary files for Hugging Face deployment...
