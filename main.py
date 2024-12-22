import struct
from typing import Any

def decode(encoded: bytes) -> Any:
    """Decodes custom binary format into the Python value."""
    if len(encoded) == 0:
        return None
    
    type_byte = encoded[0]
    index = 1
    
    if type_byte == 0x00:
        # Null
        return None
    elif type_byte == 0x03:
        # Dictionary: number of items first
        num_items = encoded[index]
        index += 1
        decoded_dict = {}
        for _ in range(num_items):
            key = decode(encoded[index:])
            index += len(key)
            value = decode(encoded[index:])
            index += len(value)
            decoded_dict[key] = value
        return decoded_dict
    elif type_byte == 0x06:
        # String (octets): length byte first
        length = encoded[index]
        index += 1
        return encoded[index:index + length].decode('utf-8')
    elif type_byte == 0x07:
        # Integer (little-endian, 8 bytes)
        return struct.unpack("<Q", encoded[index:index + 8])[0]
    else:
        raise ValueError(f"Unsupported type byte: {type_byte}")

# Example usage
encoded_data = b'\x03\x04\x6E\x75\x6C\x6C\x00\x06\x6F\x63\x74\x65\x74\x73\x03\x01\x02\x03\x07\x69\x6E\x74\x65\x67\x65\x72\x39\x30'
decoded_value = decode(encoded_data)
print(decoded_value)
{
    "null": None,
    "octets": bytes([1, 2, 3]),
    "integer": 12345
}
[
    0x03,  # Dictionary with 3 items
    0x04, 0x6E, 0x75, 0x6C, 0x6C,  # "null"
    0x00,  # Empty sequence
    0x06, 0x6F, 0x63, 0x74, 0x65, 0x74, 0x73,  # "octets"
    0x03, 0x01, 0x02, 0x03,  # Byte sequence length 3
    0x07, 0x69, 0x6E, 0x74, 0x65, 0x67, 0x65, 0x72,  # "integer"
    0x39, 0x30  # 12345 in little-endian
]
{
    "outer": {
        "inner": [1, 2, 3],
        "value": 42
    }
  [
    0x01,  # Dictionary with 1 item
    0x05, 0x6F, 0x75, 0x74, 0x65, 0x72,  # "outer"
    0x02,  # Dictionary with 2 items
    0x05, 0x69, 0x6E, 0x6E, 0x65, 0x72,  # "inner"
    0x03, 0x01, 0x02, 0x03,  # Array [1, 2, 3]
    0x05, 0x76, 0x61, 0x6C, 0x75, 0x65,  # "value"
    0x2A  # 42
]
18446744073709551615  # 2^64 - 1
[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

}

