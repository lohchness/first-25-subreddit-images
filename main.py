import praw, urllib.request, os, ssl
from prawcore.exceptions import NotFound

# This fixes SSL certificate verification errors, but in retrospect this is really just a monkeypatch. 
# Note to self: It is NOT recommended to write this line in any future scripts.
ssl._create_default_https_context = ssl._create_unverified_context

# App details from the throwaway reddit account
CLIENT_ID = "88bC6vdBK1qz9M9JbAeRRQ"
SECRET_KEY = "i7Wt88_bf9mf6woJRF6tzTF_iS20BQ"
POST_LIMIT = 25

# Username and password only meant for testing purposes.
reddit = praw.Reddit(client_id = CLIENT_ID, 
                    client_secret = SECRET_KEY, 
                    username = 'github_test_lock', 
                    password='github_test', 
                    user_agent = 'hot25img/1.0.0'
                    )

# Checks if the subreddit exists
def input_sub_name():
    subreddit = input("Enter the sub you want to scrape for pictures: ")
    exists = True
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
    except NotFound:
        print(f"r/{subreddit} not found, try again")
        exists = False
    main(subreddit) if exists else input_sub_name()

# Combs through first 25 posts of the hot section of the subreddit and retrieves the images
def main(sub_to_scrape):
    print(f"r/{sub_to_scrape} exists, starting downloading...")
    subreddit = reddit.subreddit(sub_to_scrape)
    hot_section = subreddit.hot(limit=POST_LIMIT)
    # List of posts that are stickied. Subreddits can only sticky up to 2 posts at a time.
    stickies = [reddit.subreddit(sub_to_scrape).sticky(i).id for i in range(1,4)]

    # Creates folder to save images in
    if not os.path.exists(f"pics/{sub_to_scrape}"):
        os.makedirs(f"pics/{sub_to_scrape}")

    # Iterate through hot section of subreddit
    valid_post_count = 0
    total_post_count = 0
    image_download_count = 0
    for submission in hot_section:
        # Filters sticky posts out
        if submission.id not in stickies:
            total_post_count += 1
            url = str(submission.url)

            # Name of the file is pretty much unique; it's hex so there's 16^6 permutations of IDs for each subreddit.
            # Check if link is valid image, not a selftext or external website link
            if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
                valid_post_count += 1
                image_download_count += 1
                urllib.request.urlretrieve(url, f"pics/{sub_to_scrape}/{submission.id}.jpg")

            # Iterates through Reddit galleries and downloads each image in there
            if "https://www.reddit.com/gallery/" in url:
                valid_post_count += 1
                gallery = []
                for i in submission.media_metadata.items():
                    img = i[1]['p'][0]['u']
                    img = img.split("?")[0].replace("preview", "i")
                    gallery.append(img)
                
                for img in gallery:
                    filename = img.removeprefix("https://i.redd.it/").removesuffix(".jpg")
                    urllib.request.urlretrieve(img, f"pics/{sub_to_scrape}/{filename}.jpg")
                    image_download_count += 1

    print(f"Done! {image_download_count} images downloaded from {valid_post_count} image posts. Images will be found at ./pics/{sub_to_scrape}.")

if __name__ == "__main__":
    input_sub_name()