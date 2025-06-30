import requests
import os
import re

# তোমার GitHub ইউজারনেম লিখো
USERNAME = "suhel-software"

# README.md ফাইলের পাথ
README_PATH = "README.md"

# GitHub API URL: user repos
REPOS_API = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"

def get_language_stats():
    repos = requests.get(REPOS_API).json()
    language_totals = {}

    for repo in repos:
        # শুধুমাত্র পাবলিক রিপোজিটরি নেবে
        if repo.get("fork"):
            continue
        langs_url = repo.get("languages_url")
        if not langs_url:
            continue
        langs = requests.get(langs_url).json()
        for lang, count in langs.items():
            language_totals[lang] = language_totals.get(lang, 0) + count

    return language_totals

def generate_language_badges(language_totals):
    total = sum(language_totals.values())
    # percentage calculation + badge generation
    badges = []
    for lang, count in sorted(language_totals.items(), key=lambda x: x[1], reverse=True):
        percent = (count / total) * 100
        percent_str = f"{percent:.1f}"
        color = "blue"  # চাইলে কালার কাস্টমাইজ করো
        badge = f"![{lang}](https://img.shields.io/badge/{lang}-{percent_str}%25-{color})"
        badges.append(badge)
    return " ".join(badges)

def update_readme(badges):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # README তে বিশেষ ট্যাগ দিয়ে রাখবে যেখানে ল্যাঙ্গুয়েজ বেজ যোগ করবে
    pattern = r"(<!-- LANGUAGES_START -->)(.*?)(<!-- LANGUAGES_END -->)"
    replacement = f"<!-- LANGUAGES_START -->\n{badges}\n<!-- LANGUAGES_END -->"

    if re.search(pattern, content, flags=re.DOTALL):
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # যদি ট্যাগ না থাকে, শেষে যোগ করো
        new_content = content + "\n\n" + replacement

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    print("Fetching language stats from GitHub...")
    language_totals = get_language_stats()
    print("Generating badges...")
    badges = generate_language_badges(language_totals)
    print("Updating README.md...")
    update_readme(badges)
    print("Done!")

if __name__ == "__main__":
    main()
