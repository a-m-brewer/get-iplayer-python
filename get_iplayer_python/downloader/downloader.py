import requests

from get_iplayer_python.mpd_data_extractor import create_templates


def download(filename, template):
    with open(filename, "wb") as file:
        init_resp = requests.get("%s%s" % (template["base_url"], template["init_url"]), stream=True)
        for chunk in init_resp:
            file.write(chunk)

        frags = 0
        total_frag = len(template["fragments"])
        for frag in template["fragments"]:
            resp = requests.get("%s%s" % (template["base_url"], frag["path"]), stream=True)
            file.write(resp.content)
            # for chunk in resp:
            #     file.write(chunk)
            frags += 1
            print(f"frag: {frags}/{total_frag} downloaded")


if __name__ == '__main__':
    templates = create_templates()
    download("diplo-and-friends.mp4", templates[1])
