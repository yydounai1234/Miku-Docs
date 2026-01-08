# -*- coding: utf-8 -*-
import os
import hmac
import hashlib
import base64
import json
from urllib.parse import urlparse
from http.client import HTTPSConnection, HTTPConnection

# 你的 AK 和 SK
AK = os.getenv("Access_key")
SK = os.getenv("Secret_key")


def test_add_transcoding_template(bucket_name, template_body):
    """
    新增实时流转码模板。

    Args:
        bucket_name (str): 空间名称，用于拼接 host（示例使用 cn-east-1 区域）
        template_body (dict): 模板内容，字段参考“新增实时流转码模板”文档
    """

    method = "POST"
    host = f"{bucket_name}.mls.cn-east-1.qiniumiku.com"
    path = "/?template=transcode"
    url = f"http://{host}{path}"
    print(f"Sending request to: {url}")

    body = json.dumps(template_body)

    signature = generate_signature(method, url, body, AK, SK)
    print(f"生成的签名: {signature}")

    response = send_http_request(url, method, body, signature, 30)
    return response


def generate_signature(method, url, body, ak, sk):
    parsed_url = urlparse(url)

    data = method + " " + parsed_url.path

    if parsed_url.query:
        data += "?" + parsed_url.query

    data += "\nHost: " + parsed_url.hostname
    data += "\nContent-Type: application/json"

    if body:
        data += "\n\n" + body
    print(data)

    hmac_sha1 = hmac.new(sk.encode("utf-8"), data.encode("utf-8"), hashlib.sha1)
    hmac_result = hmac_sha1.digest()

    sign = "Qiniu " + ak + ":" + base64_url_safe_encode(hmac_result)
    return sign


def send_http_request(url, method, data, signature, timeout):
    parsed_url = urlparse(url)

    if not parsed_url.hostname:
        raise ValueError("Invalid URL: missing hostname")

    if parsed_url.scheme == "https":
        conn = HTTPSConnection(parsed_url.hostname, parsed_url.port or 443, timeout=timeout)
    else:
        conn = HTTPConnection(parsed_url.hostname, parsed_url.port or 80, timeout=timeout)

    headers = {
        "Content-Type": "application/json",
        "Authorization": signature,
    }

    conn.request(
        method,
        parsed_url.path + ("?" + parsed_url.query if parsed_url.query else ""),
        body=data if data else "{}",
        headers=headers,
    )

    response = conn.getresponse()
    response_body = response.read().decode("utf-8")

    conn.close()

    return f"HTTP {response.status}: {response_body}"


def base64_url_safe_encode(data):
    encoded = base64.b64encode(data).decode("utf-8")
    encoded = encoded.replace("+", "-").replace("/", "_")
    return encoded


if __name__ == "__main__":
    bucket_name = "sdk-miku-test"

    # 示例请求体，可按需调整字段
    template_body = {
        "name": "720p-template",
        "description": "720p转码模板",
        "video": {
            "codec": "h264",
            "width": 1280,
            "height": 720,
            "bitrate": 1500000,
            "framerate": 30,
        },
        "audio": {"codec": "aac", "bitrate": 128000, "samplerate": 44100},
        "format": "hls",
    }

    print("--- 新增实时流转码模板 ---")
    response = test_add_transcoding_template(bucket_name, template_body)
    print(f"响应内容: {response}")
