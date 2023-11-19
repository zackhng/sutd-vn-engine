"""Main entrypoint."""

import asyncio
import base64
import json
import logging
import tkinter as tk
from calendar import c
from tempfile import NamedTemporaryFile
from urllib import request

log = logging.getLogger(__name__)

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
    return asyncio.to_thread(request.urlopen, req)


async def get_image(prompt):
    """Get image from text."""
    obj = {"prompt": prompt}
    try:
        res = await post_json(url, obj)
    except asyncio.CancelledError:
        log.warning(f"cancelled: {prompt}")
        return None

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

    cur_req_task = None

    image_label = tk.Label(app)
    image_label.pack()

    prompt_input = tk.Text(app)
    prompt_input.pack()

    def _update_image(path):
        log.info(f"temp path: {path}")
        if path is None:
            return
        image = tk.PhotoImage(file=path)
        image_label.image = image
        image_label.configure(image=image)

    def _send_prompt():
        nonlocal cur_req_task
        if cur_req_task:
            cur_req_task.cancel()
            cur_req_task = None

        prompt = prompt_input.get("1.0", "end-1c")
        log.info(f"prompt: {prompt}")
        cur_req_task = asyncio.create_task(get_image(prompt))
        cur_req_task.add_done_callback(lambda f: _update_image(f.result()))

    confirm = tk.Button(app, command=_send_prompt, text="Generate")
    confirm.pack()

    while True:
        app.update()
        await asyncio.sleep(0.015)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
