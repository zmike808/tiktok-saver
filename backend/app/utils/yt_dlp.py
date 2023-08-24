# To use these options you must check : https://github.com/yt-dlp/yt-dlp
USE_COOKIES = False
COOKIES_PATH = "cookies.txt"
COOKIES_BROWSER = "chrome"


def get_command(url: str) -> str:
    return (
        f"yt-dlp {url} --cookies {COOKIES_PATH} --no-download --dump-json -q --cookies-from-browser {COOKIES_BROWSER}"
        if USE_COOKIES
        else f"yt-dlp {url} --no-download --dump-json -q"
    )
