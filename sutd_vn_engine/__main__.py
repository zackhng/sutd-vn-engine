"""Main entrypoint."""

import asyncio
import base64
import json
import tkinter as tk
from tempfile import NamedTemporaryFile
from urllib import request

url = "http://robowsl.home.arpa:6000/sdapi/v1/txt2img"


def post_json(url, obj):
    """Post object to url as json."""
    data = json.dumps(obj).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Content-Length": len(data),
        },
    )
    return request.urlopen(req)


def get_image(prompt):
    """Get image from text."""
    obj = {"prompt": prompt}
    res = post_json(url, obj)

    data = json.loads(res.read())
    b64_img = data["images"][0]
    raw_img = base64.decodebytes(b64_img.encode("utf-8"))
    with NamedTemporaryFile(delete=False, suffix=".png") as f:
        f.write(raw_img)
        return f.name


async def main():
    """Main entrypoint."""
    app = tk.Tk()
    app.title("SUTD Visual Novel")

    image_label = tk.Label(app)
    image_label.pack()

    prompt_input = tk.Text(app)
    prompt_input.pack()

    def _update_image():
        prompt = prompt_input.get("1.0", "end-1c")
        print("prompt:", prompt)
        path = get_image(prompt)
        print("temp path:", path)
        image = tk.PhotoImage(file=path)
        image_label.image = image
        image_label.configure(image=image)

    confirm = tk.Button(app, command=_update_image, text="Generate")
    confirm.pack()

    while True:
        app.update()
        await asyncio.sleep(0.015)


if __name__ == "__main__":
    asyncio.run(main())
