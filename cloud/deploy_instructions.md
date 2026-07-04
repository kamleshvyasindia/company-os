# Step-by-Step Guide: Deploying the Cloud Slack Bot (Option 2)

This guide walks you through deploying your 24/7 Slack bot. The bot will run on **Render** (free hosting) and connect directly to your private GitHub repository and Google's **Gemini AI** to answer your questions on Slack.

---

## Part 1: Gather Your Credentials
You will need three keys to deploy the bot:

1. **SLACK_BOT_TOKEN**: Your Slack bot token starting with `xoxb-` (which we set up in Option A).
2. **GITHUB_PAT** (GitHub Personal Access Token):
   - Go to GitHub ➔ click your Profile Pic ➔ **Settings** ➔ **Developer Settings** ➔ **Personal access tokens** ➔ **Tokens (classic)**.
   - Click **Generate new token (classic)**.
   - Name it `Deloitte Brain Cloud` and check the **`repo`** scope box (allows it to read your private repository).
   - Generate and copy the token (starts with `ghp_`).
3. **GEMINI_API_KEY** (Google AI API Key):
   - Go to the [Google AI Studio](https://aistudio.google.com/).
   - Click **Get API Key** and generate a new key. Copy it.

---

## Part 2: Deploy to Render (Free Tier)
We will deploy the bot using **Render**:

1. Go to **[Render.com](https://render.com/)** and log in using your **GitHub account**.
2. Click the blue **New +** button ➔ select **Web Service**.
3. Under *Connect a repository*, choose your **`company-os`** repository.
4. Fill in the configuration:
   - **Name**: `deloitte-education-brain`
   - **Environment**: `Python`
   - **Region**: Select any (e.g., *Oregon* or *Singapore*)
   - **Branch**: `master`
   - **Build Command**: `pip install -r cloud/requirements.txt`
   - **Start Command**: `uvicorn cloud.app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Select **Free**
5. Click **Advanced** at the bottom ➔ click **Add Environment Variable** and add these four keys:
   - `SLACK_BOT_TOKEN` = *(Your token starting with `xoxb-`)*
   - `GITHUB_PAT` = *(Your GitHub token starting with `ghp_`)*
   - `GEMINI_API_KEY` = *(Your Google Gemini key)*
   - `GITHUB_REPO` = `kamleshvyasindia/company-os`
6. Click **Create Web Service**. 
7. Render will build and deploy your service (takes about 2 minutes). Once done, it will give you a public URL at the top of the page (e.g., `https://deloitte-education-brain.onrender.com`). Copy this URL.

---

## Part 3: Connect Slack Webhook
1. Go back to your Slack App Settings: **[api.slack.com/apps/A0BETDFDAR1](https://api.slack.com/apps/A0BETDFDAR1)**.
2. In the left sidebar, click **Event Subscriptions** ➔ click the toggle to turn it **On**.
3. In the **Request URL** field, paste your Render URL and append `/api/slack` to the end of it.
   - Example: `https://deloitte-education-brain.onrender.com/api/slack`
4. Slack will send a test handshake request. Once verified, it will show a green **Verified** checkmark.
5. Scroll down to **Subscribe to bot events**, click **Add Bot User Event**, and select:
   - **`app_mention`** (responds when you @mention it)
   - **`message.im`** (responds to direct messages)
6. Click **Save Changes** at the bottom.
7. Click the reinstall prompt in the yellow banner to apply these webhooks to your Slack workspace.

***

### 🎉 You are Done!
You can now open Slack on your mobile phone or laptop (even when your laptop is closed/off) and direct-message your bot:
> *what is our estimated NSR for July?*
The bot will query your latest GitHub data and respond immediately!
