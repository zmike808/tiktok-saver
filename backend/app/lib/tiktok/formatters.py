def format_post_json(post: dict):
    post_type = post.get("_type", None)
    if post_type != "video":
        return None

    if "music" in post["formats"][0]["url"]:
        return None

    is_watermarked = False
    highest_quality = list(filter(lambda item: "h264" in item["vcodec"], post["formats"]))
    no_watermark_videos = list(filter(lambda item: "direct video" in item["format"].lower(), highest_quality))

    video_format = no_watermark_videos[0]
    if not video_format:
        watermark_videos = list(filter(lambda item: "download video" in item["format"].lower(), highest_quality))
        video_format = watermark_videos[0]
        is_watermarked = True

    if not video_format:
        video_format = post["formats"][0]

    if not video_format:
        return None

    video_filename = post.get("filename", "tiktok_video.mp4")
    video_duration = post.get("duration", "")
    video_link = video_format.get("url", "")
    video_thumbnail = post.get("thumbnail", "")

    video = {
        "filename": video_filename,
        "duration": video_duration,
        "is_watermarked": is_watermarked,
        "video_link": video_link,
        "thumbnail": video_thumbnail,
    }

    return video


def format_video_info(data: dict):
    video_info = format_post_json(data)
    return video_info
