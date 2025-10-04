#!/usr/bin/env python3
"""
Script to update README.md with latest blog posts and videos
"""

import feedparser
import requests
import os
import re
from datetime import datetime
from dateutil import parser as date_parser

# Configuration
MEDIUM_RSS_URL = "https://medium.com/feed/@mtwn105"
DEVTO_RSS_URL = "https://dev.to/feed/mtwn105"
BLOG_RSS_URL = "https://blog.amitwani.dev/rss.xml"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
YOUTUBE_CHANNEL_ID = os.getenv("CHANNEL_ID", "")
MAX_POSTS = 5

def fetch_medium_posts():
    """Fetch latest Medium posts"""
    try:
        feed = feedparser.parse(MEDIUM_RSS_URL)
        posts = []

        for entry in feed.entries[:MAX_POSTS]:
            title = entry.title
            link = entry.link
            # Parse date
            pub_date = date_parser.parse(entry.published)
            date_str = pub_date.strftime("%b %d, %Y")

            posts.append({
                'title': title,
                'link': link,
                'date': date_str
            })

        return posts
    except Exception as e:
        print(f"Error fetching Medium posts: {e}")
        return []

def fetch_devto_posts():
    """Fetch latest Dev.to posts"""
    try:
        feed = feedparser.parse(DEVTO_RSS_URL)
        posts = []

        for entry in feed.entries[:MAX_POSTS]:
            title = entry.title
            link = entry.link
            # Parse date
            pub_date = date_parser.parse(entry.published)
            date_str = pub_date.strftime("%b %d, %Y")

            posts.append({
                'title': title,
                'link': link,
                'date': date_str
            })

        return posts
    except Exception as e:
        print(f"Error fetching Dev.to posts: {e}")
        return []

def fetch_blog_posts():
    """Fetch latest blog posts from blog.amitwani.dev"""
    try:
        feed = feedparser.parse(BLOG_RSS_URL)
        posts = []

        for entry in feed.entries[:MAX_POSTS]:
            title = entry.title
            link = entry.link
            # Parse date
            pub_date = date_parser.parse(entry.published)
            date_str = pub_date.strftime("%b %d, %Y")

            posts.append({
                'title': title,
                'link': link,
                'date': date_str
            })

        return posts
    except Exception as e:
        print(f"Error fetching blog posts: {e}")
        return []

def fetch_youtube_videos():
    """Fetch latest YouTube videos"""
    try:
        if not YOUTUBE_API_KEY or not YOUTUBE_CHANNEL_ID:
            print("YouTube API key or Channel ID not found. Using RSS feed instead.")
            return fetch_youtube_videos_rss()

        url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={YOUTUBE_CHANNEL_ID}&part=snippet,id&order=date&maxResults={MAX_POSTS}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get('items', []):
            if item['id'].get('kind') == 'youtube#video':
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                # Parse date
                pub_date = date_parser.parse(item['snippet']['publishedAt'])
                date_str = pub_date.strftime("%b %d, %Y")

                videos.append({
                    'id': video_id,
                    'title': title,
                    'date': date_str
                })

        return videos
    except Exception as e:
        print(f"Error fetching YouTube videos via API: {e}")
        print("Falling back to RSS feed")
        return fetch_youtube_videos_rss()

def fetch_youtube_videos_rss():
    """Fetch latest YouTube videos using RSS feed (fallback)"""
    try:
        # Use channel ID if available, otherwise try to fetch from username
        channel_id = YOUTUBE_CHANNEL_ID if YOUTUBE_CHANNEL_ID else "UCl_1O6Y6LCkdYLm9EZEHdcg"

        # Try RSS feed with channel ID
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

        feed = feedparser.parse(rss_url)

        # If RSS feed is empty, try fetching by username
        if not feed.entries:
            print("Trying RSS feed with username...")
            rss_url = "https://www.youtube.com/feeds/videos.xml?user=AmitWani"
            feed = feedparser.parse(rss_url)

        videos = []

        for entry in feed.entries[:MAX_POSTS]:
            # Extract video ID from link
            video_id = entry.yt_videoid if hasattr(entry, 'yt_videoid') else entry.link.split('=')[-1]
            title = entry.title
            # Parse date
            pub_date = date_parser.parse(entry.published)
            date_str = pub_date.strftime("%b %d, %Y")

            videos.append({
                'id': video_id,
                'title': title,
                'date': date_str
            })

        return videos
    except Exception as e:
        print(f"Error fetching YouTube videos via RSS: {e}")
        return []

def generate_medium_content(posts):
    """Generate HTML content for Medium posts"""
    if not posts:
        return ""

    rows = []
    for post in posts:
        row = f'<tr><td>📚 <a href="{post["link"]}">{post["title"]}</a></td><td>{post["date"]}</td></tr>'
        rows.append(row)

    return "".join(rows)

def generate_devto_content(posts):
    """Generate HTML content for Dev.to posts"""
    if not posts:
        return ""

    rows = []
    for post in posts:
        row = f'<tr><td>🚀 <a href="{post["link"]}">{post["title"]}</a></td><td>{post["date"]}</td></tr>'
        rows.append(row)

    return "".join(rows)

def generate_blog_content(posts):
    """Generate HTML content for blog posts"""
    if not posts:
        return ""

    rows = []
    for post in posts:
        row = f'<tr><td>✍️ <a href="{post["link"]}">{post["title"]}</a></td><td>{post["date"]}</td></tr>'
        rows.append(row)

    return "".join(rows)

def generate_youtube_content(videos):
    """Generate HTML content for YouTube videos"""
    if not videos:
        return ""

    rows = []
    for video in videos:
        row = f'<tr><td><a href="https://www.youtube.com/watch?v={video["id"]}"><img width="140px" src="https://img.youtube.com/vi/{video["id"]}/hqdefault.jpg"></a></td><td><a href="https://www.youtube.com/watch?v={video["id"]}">{video["title"]}</a><br/>{video["date"]}</td></tr>'
        rows.append(row)

    return "".join(rows)

def update_readme(medium_content, devto_content, blog_content, youtube_content):
    """Update README.md with new content"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()

        # Update Medium section
        medium_pattern = r'<!-- MEDIUM-BLOG-LIST:START -->.*?<!-- MEDIUM-BLOG-LIST:END -->'
        medium_replacement = f'<!-- MEDIUM-BLOG-LIST:START -->{medium_content}<!-- MEDIUM-BLOG-LIST:END -->'
        readme = re.sub(medium_pattern, medium_replacement, readme, flags=re.DOTALL)

        # Update Dev.to section
        devto_pattern = r'<!-- DEVTO-BLOG-LIST:START -->.*?<!-- DEVTO-BLOG-LIST:END -->'
        devto_replacement = f'<!-- DEVTO-BLOG-LIST:START -->{devto_content}<!-- DEVTO-BLOG-LIST:END -->'
        readme = re.sub(devto_pattern, devto_replacement, readme, flags=re.DOTALL)

        # Update or add Blog section
        blog_pattern = r'<!-- BLOG-LIST:START -->.*?<!-- BLOG-LIST:END -->'
        blog_replacement = f'<!-- BLOG-LIST:START -->{blog_content}<!-- BLOG-LIST:END -->'
        if '<!-- BLOG-LIST:START -->' in readme:
            readme = re.sub(blog_pattern, blog_replacement, readme, flags=re.DOTALL)
        else:
            # Add blog section after Dev.to section
            devto_section_end = readme.find('<!-- DEVTO-BLOG-LIST:END -->')
            if devto_section_end != -1:
                # Find the end of the table
                table_end = readme.find('</table>', devto_section_end)
                if table_end != -1:
                    blog_section = f'\n\n### 📝 **Personal Blog** - [blog.amitwani.dev](https://blog.amitwani.dev)\n\n<table>\n  <tr><th>Title</th><th>Date</th></tr>\n  {blog_replacement}\n\n</table>'
                    readme = readme[:table_end + 8] + blog_section + readme[table_end + 8:]

        # Update YouTube section
        youtube_pattern = r'<!-- YOUTUBE-BLOG-LIST:START -->.*?<!-- YOUTUBE-BLOG-LIST:END -->'
        youtube_replacement = f'<!-- YOUTUBE-BLOG-LIST:START -->{youtube_content}<!-- YOUTUBE-BLOG-LIST:END -->'
        readme = re.sub(youtube_pattern, youtube_replacement, readme, flags=re.DOTALL)

        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme)

        print("README.md updated successfully!")

    except Exception as e:
        print(f"Error updating README: {e}")

def main():
    """Main function"""
    print("Fetching latest content...")

    # Fetch content
    medium_posts = fetch_medium_posts()
    print(f"Fetched {len(medium_posts)} Medium posts")

    devto_posts = fetch_devto_posts()
    print(f"Fetched {len(devto_posts)} Dev.to posts")

    blog_posts = fetch_blog_posts()
    print(f"Fetched {len(blog_posts)} blog posts")

    youtube_videos = fetch_youtube_videos()
    print(f"Fetched {len(youtube_videos)} YouTube videos")

    # Generate content
    medium_content = generate_medium_content(medium_posts)
    devto_content = generate_devto_content(devto_posts)
    blog_content = generate_blog_content(blog_posts)
    youtube_content = generate_youtube_content(youtube_videos)

    # Update README
    update_readme(medium_content, devto_content, blog_content, youtube_content)

if __name__ == "__main__":
    main()

