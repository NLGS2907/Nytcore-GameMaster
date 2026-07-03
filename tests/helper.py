from io import BytesIO


def dummy_bmp(width: int, height: int) -> BytesIO:
    """Makes a dummy BMP image of the given width and height."""

    # BMP rows must align to a 4-byte storage boundary
    row_bytes = (width * 3 + 3) & ~3
    pixel_payload = b"\x00" * (row_bytes * height)
    
    # Extract little-endian 4-byte dimensions
    w_bytes = width.to_bytes(4, byteorder='little')
    h_bytes = height.to_bytes(4, byteorder='little')
    
    # Combine stripped headers and calculated pixel data inside the constructor
    return BytesIO(
        (
            b"BM\x00\x00\x00\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00"
            b"%b"  # 4 bytes for Width
            b"%b"  # 4 bytes for Height
            b"\x01\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"%b"  # Dynamically sized pixel data block
        ) % (w_bytes, h_bytes, pixel_payload)
    )