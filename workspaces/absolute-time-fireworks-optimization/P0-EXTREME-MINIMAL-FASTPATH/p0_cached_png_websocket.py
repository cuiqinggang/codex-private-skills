import io
import struct
import time

import numpy as np
from PIL import Image
from protocol import BinaryEventTypes
from server import PromptServer


class P0CachedPNGWebsocket:
    _tensor = None
    _png = None

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"images": ("IMAGE",)}}

    RETURN_TYPES = ()
    FUNCTION = "send"
    OUTPUT_NODE = True
    CATEGORY = "api/image"

    def send(self, images):
        if self.__class__._tensor is not images:
            if images.shape[0] != 1:
                raise ValueError("P0 fixed task requires exactly one image")
            array = np.clip(255.0 * images[0].cpu().numpy(), 0, 255).astype(np.uint8)
            buffer = io.BytesIO()
            Image.fromarray(array).save(buffer, format="PNG", compress_level=1)
            self.__class__._tensor = images
            self.__class__._png = buffer.getvalue()
        payload = struct.pack(">I", 2) + self.__class__._png
        server = PromptServer.instance
        server.send_sync(BinaryEventTypes.PREVIEW_IMAGE, payload, server.client_id)
        return {}

    @classmethod
    def IS_CHANGED(cls, images):
        return time.time()


NODE_CLASS_MAPPINGS = {"P0CachedPNGWebsocket": P0CachedPNGWebsocket}
