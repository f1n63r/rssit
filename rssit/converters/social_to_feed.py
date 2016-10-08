# -*- coding: utf-8 -*-


import rssit.util


def process(result, config):
    feed = {}

    for key in result.keys():
        if key != "entries":
            feed[key] = rssit.util.simple_copy(result[key])

    feed["entries"] = []

    for entry in result["entries"]:
        caption = entry["caption"]

        if not caption:
            caption = "(n/a)"

        basecontent = rssit.util.link_urls(caption.replace("\n", "<br />\n"))
        basetitle = caption.replace("\n", " ")

        if entry["author"] != result["author"]:
            content = "<p><em>%s</em></p><p>%s</p>" % (
                entry["author"],
                basecontent
            )

            title = "%s: %s" % (
                entry["author"],
                basetitle
            )
        else:
            content = "<p>%s</p>" % basecontent
            title = basetitle

        if entry["videos"]:
            for video in entry["videos"]:
                if "image" in video and video["image"]:
                    content += "<p><em>Click to watch video</em></p>"

                    content += "<a href='%s'><img src='%s'/></a>" % (
                        video["video"],
                        video["image"]
                    )
                else:
                    content += "<p><em><a href='%s'>Video</a></em></p>" % video["video"]

        if entry["images"]:
            for image in entry["images"]:
                content += "<p><img src='%s'/></p>" % image

        feed["entries"].append({
            "url": entry["url"],
            "title": title,
            "author": entry["author"],
            "date": entry["date"],
            "content": content
        })

    return feed


infos = [{
    "input": "social",
    "output": "feed",
    "process": process
}]