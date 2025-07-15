
---

### 📄 reddit_user_persona.py

```python
import os
import re
from urllib.parse import urlparse
from collections import defaultdict
from dotenv import load_dotenv
import praw

# Load environment variables
load_dotenv()

# Reddit OAuth
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT", "reddit-user-persona/0.1")
)

def extract_username(url):
    path = urlparse(url).path
    m = re.match(r'/user/([^/]+)/?', path)
    return m.group(1) if m else None

def fetch_content(username, limit=100):
    user = reddit.redditor(username)
    comments = list(user.comments.new(limit=limit))
    posts = list(user.submissions.new(limit=limit))
    return comments, posts

def analyze_persona(comments, posts):
    persona = defaultdict(lambda: {"trait": "", "citations": []})
    items = [(c.body, f"Comment in r/{c.subreddit} – https://reddit.com{c.permalink}") for c in comments] + \
            [(p.title + " " + (p.selftext or ""), f"Post in r/{p.subreddit} – https://reddit.com{p.permalink}") for p in posts]

    for text, cite in items:
        t = text.lower()
        if any(x in t for x in ["i'm a student", "in college", "university", "studying"]):
            persona['Education'] = {"trait": "Student or university educated", "citations": [cite]}
        if any(x in t for x in ["i work as", "i’m a", "i am a", "at work"]):
            persona['Occupation'] = {"trait": "Mentions profession", "citations": [cite]}
        if any(x in t for x in ["my wife", "my husband", "boyfriend", "girlfriend", "single", "divorced"]):
            persona['Relationship'] = {"trait": "Mentions relationship status", "citations": [cite]}
        if any(x in t for x in ["i love", "i enjoy", "favorite", "i like", "hobby"]):
            persona['Interests'] = {"trait": "Mentions hobbies or interests", "citations": [cite]}
        if any(x in t for x in ["politics", "government", "election", "vote"]):
            persona['Politics'] = {"trait": "Discusses political topics", "citations": [cite]}
        if any(x in t for x in ["mental health", "therapy", "depression", "anxiety"]):
            persona['Mental Health'] = {"trait": "Mentions mental health", "citations": [cite]}
    return persona

def write_persona(username, persona):
    fname = f"{username}_persona.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"USER PERSONA: u/{username}\n")
        f.write("="*40 + "\n\n")
        for cat, data in persona.items():
            f.write(f"{cat}:\n")
            f.write(f"  Trait: {data['trait']}\n")
            f.write("  Citations:\n")
            for c in data['citations']:
                f.write(f"    - {c}\n")
            f.write("\n")
    print(f"Persona saved to: {fname}")

def main():
    url = input("Enter Reddit profile URL: ").strip()
    u = extract_username(url)
    if not u:
        print("⚠️ Invalid URL")
        return
    print(f"Fetching for u/{u} ...")
    comments, posts = fetch_content(u)
    persona = analyze_persona(comments, posts)
    write_persona(u, persona)

if __name__ == "__main__":
    main()
