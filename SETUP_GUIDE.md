# Automated README Update Setup Guide 🚀

This guide will help you set up a GitHub Action that automatically updates your README with your latest content.

## 📋 What's Been Set Up

A GitHub Action that runs daily at **12:00 AM IST** (6:30 PM UTC) and automatically updates your README with:

- 📚 **Medium** - Your latest 5 articles
- 🚀 **Dev.to** - Your latest 5 posts
- ✍️ **blog.amitwani.dev** - Your latest 5 blog posts
- 📺 **YouTube** - Your latest 5 videos

## 💰 Cost: Completely FREE!

- ✅ GitHub Actions: Unlimited for public repos
- ✅ RSS Feeds: Free, no API keys needed
- ✅ YouTube API (optional): 10,000 free units/day (we use ~100)

## 🚀 Quick Start

### Option 1: Simple Setup (Recommended - No API Keys Needed!)

1. **Commit and push the changes:**

   ```bash
   git add .
   git commit -m "feat: Add automated README update workflow"
   git push
   ```

2. **Test manually (optional):**

   - Go to your repo on GitHub
   - Click **Actions** → **Update README with Latest Content** → **Run workflow**

3. **Done!** The workflow uses RSS feeds (completely free, no setup needed).

### Option 2: Enhanced YouTube Setup (Optional)

For better YouTube integration, you can optionally set up the YouTube API:

#### Get YouTube API Key:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy the API key

#### Get YouTube Channel ID:

- Go to your channel page
- Look at the URL: `https://www.youtube.com/@YourHandle`
- Use a tool like [Comment Picker](https://commentpicker.com/youtube-channel-id.php) to get your channel ID

#### Add Secrets to GitHub:

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add two secrets:
   - Name: `YOUTUBE_API_KEY`, Value: Your YouTube API key
   - Name: `YOUTUBE_CHANNEL_ID`, Value: Your YouTube channel ID

## 🧪 Testing Locally

Want to test before pushing to GitHub?

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script
python scripts/update_readme.py
```

This will update your README.md locally so you can preview the changes!

## ⚙️ How It Works

The script:

1. Fetches RSS feeds from Medium, Dev.to, your blog, and YouTube
2. Parses the latest 5 articles/videos from each source
3. Generates HTML content
4. Updates your README.md between these comment markers:
   - `<!-- MEDIUM-BLOG-LIST:START -->` ... `<!-- MEDIUM-BLOG-LIST:END -->`
   - `<!-- DEVTO-BLOG-LIST:START -->` ... `<!-- DEVTO-BLOG-LIST:END -->`
   - `<!-- BLOG-LIST:START -->` ... `<!-- BLOG-LIST:END -->`
   - `<!-- YOUTUBE-BLOG-LIST:START -->` ... `<!-- YOUTUBE-BLOG-LIST:END -->`
5. Commits and pushes the changes automatically

**⚠️ Important:** Don't remove these comment markers from your README!

## 🎨 Customization

### Change the schedule:

Edit `.github/workflows/update-readme.yml` and modify the cron expression:

```yaml
schedule:
  - cron: "30 18 * * *" # 12:00 AM IST (6:30 PM UTC)
```

Use [Crontab Guru](https://crontab.guru/) to create cron expressions. Remember: GitHub Actions use UTC timezone (IST is UTC+5:30).

### Change number of posts:

Edit `scripts/update_readme.py` and change:

```python
MAX_POSTS = 5  # Change this number
```

### Update RSS URLs:

Edit the URLs at the top of `scripts/update_readme.py`:

```python
MEDIUM_RSS_URL = "https://medium.com/feed/@mtwn105"
DEVTO_RSS_URL = "https://dev.to/feed/mtwn105"
BLOG_RSS_URL = "https://blog.amitwani.dev/rss.xml"
```

## 🔧 Troubleshooting

### Workflow not running?

- Check if the workflow file is in `.github/workflows/` directory
- Ensure the repository has Actions enabled (Settings → Actions → Allow all actions)
- Check the Actions tab for any errors

### Content not updating?

- Verify RSS feeds are accessible by visiting them in your browser
- Check if the HTML comment markers exist in README.md
- Look at the workflow logs in the Actions tab for errors

### YouTube not working?

- The script automatically falls back to RSS feeds if API is not configured
- If you set up the API, verify the secrets are correctly named: `YOUTUBE_API_KEY` and `YOUTUBE_CHANNEL_ID`
- Check that your YouTube Data API v3 is enabled in Google Cloud Console

### API rate limits?

- Medium, Dev.to, and blog RSS feeds: No rate limits
- YouTube API: 10,000 units/day (we use ~100/day)
- YouTube RSS fallback: No rate limits

## 📁 Files Structure

```
.
├── .github/
│   └── workflows/
│       └── update-readme.yml    # GitHub Action workflow
├── scripts/
│   └── update_readme.py         # Python script to fetch and update content
├── requirements.txt             # Python dependencies
├── .gitignore                   # Ignore Python cache files
└── README.md                    # Your profile README (will be auto-updated)
```

## 📦 Dependencies

The script uses these Python packages (all free and open source):

- `feedparser` - Parse RSS/Atom feeds
- `requests` - Make HTTP requests
- `python-dateutil` - Parse dates

## 🎯 Manual Trigger

You can manually run the workflow anytime:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Update README with Latest Content** workflow
4. Click **Run workflow** button

## 📝 License

Feel free to use and modify this setup for your own GitHub profile!

---

**Happy Coding!** 🎉
