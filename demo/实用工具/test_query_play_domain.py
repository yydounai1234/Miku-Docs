import os
import hmac
import hashlib
import base64
import json
from urllib.parse import urlencode, urlparse
from http.client import HTTPSConnection, HTTPConnection

# 你的 AK 和 SK
AK = os.getenv("Access_key")
SK = os.getenv("Secret_key")


def test_query_play_domain(bucket_name, stream_key, domain, expire_time=300):
    """
    播放地址拼接，返回拉流 URL。

    Args:
        bucket_name (str): 空间名称，用于拼 host `<bucket>.mls.cn-east-1.qiniumiku.com`
        stream_key (str): 流名称，对应路径 `/<streamKey>`
        domain (str): 拉流域名
        expire_time (int): 过期秒数，默认 300，0 表示不过期
    """

    method = "POST"
    host = f"{bucket_name}.mls.cn-east-1.qiniumiku.com"
    path = f"/{stream_key}"

    url = f"http://{host}{path}?playUrl"
    print(f"Sending request to: {url}")

    body = json.dumps({"expireTime": expire_time, "domain": domain})

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
    stream_key = "yydounai33"
    play_domain = "miku-test-play.qnsdk.com"

    print(f"Testing play URL generation for stream: {stream_key}")
    response = test_query_play_domain(
        bucket_name=bucket_name,
        stream_key=stream_key,
        domain=play_domain,
        expire_time=30,
    )
    print(f"响应内容: {response}")
