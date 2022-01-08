# subreddit-image-scraper
Python Reddit API Wrapper (PRAW) to grab images from the hot section of a given subreddit. Great for cat pics.

This script includes throwaway account details that is prone to possible change. If the script does not work let me know, and I'll update the details in the script, or you can change the variables yourself to fit your own Reddit account and application.

The script requires you to install PRAW, urllib3, and ssl.

# Usage

Run the script using Python 3, and type in a subreddit name. If the subreddit does not exist, try another name. If it does, the script will comb through the first 25 submissions and retrieves images from them into the ./pics/{SUBREDDIT_NAME} folder. This does not retrieve videos, gifs, or images from an external website.

Filenames are based off of the submission ID. These are pretty much guaranteed to be unique, as there are 16^6 (16,777,216) possible permutations of IDs for every subreddit. Images from Reddit galleries will have longer IDs.

Intended for personal use only.

# Video Example

https://youtu.be/1ozKxjI2L5I
