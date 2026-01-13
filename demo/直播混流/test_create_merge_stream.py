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


def test_create_stream(bucket_name, merge_body):
    """
    测试创建合流接口

    Args:
        bucket_name (str): 空间名称，会拼入 host `<bucket>.mls.cn-east-1.qiniumiku.com`
        merge_body (dict): 合流请求体，需包含 id/duration/inputs/config/outputs 等字段
    """

    # 接口信息
    method = "POST"
    host = f"{bucket_name}.mls.cn-east-1.qiniumiku.com"
    path = "/?createmerge"
    url = f"http://{host}{path}"
    print(f"Sending request to: {url}")

    body = json.dumps(merge_body)

    # 生成签名
    signature = generate_signature(method, url, body, AK, SK)
    print(f"生成的签名: {signature}")

    # 发送HTTP请求
    response = send_http_request(url, method, body, signature, 30)
    return response


def generate_signature(method, url, body, ak, sk):
    parsed_url = urlparse(url)

    # 构建签名数据
    data = method + " " + parsed_url.path

    if parsed_url.query:
        data += "?" + parsed_url.query

    data += "\nHost: " + parsed_url.hostname
    data += "\nContent-Type: application/json"

    if body:
        data += "\n\n" + body
    print(data)
    # 使用HMAC-SHA1进行签名
    hmac_sha1 = hmac.new(sk.encode("utf-8"), data.encode("utf-8"), hashlib.sha1)
    hmac_result = hmac_sha1.digest()

    sign = "Qiniu " + ak + ":" + base64_url_safe_encode(hmac_result)
    return sign


def send_http_request(url, method, data, signature, timeout):
    parsed_url = urlparse(url)

    # 检查主机名是否存在
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
    # 构造示例请求体，按需替换 source/url/id 等参数
    merge_body = {
        "id": "merge-demo-001",
        "duration": 100000,
        "inputs": [
            {
                "chnl": 0,
                "source": "rtmp://pili-live-rtmp.xrtest.cloudvdn.com/xrtest/input1",
                "chromakey": "0x004D00:0.1:0.0",
            },
            {
                "chnl": 1,
                "source": "rtmp://pili-live-rtmp.xrtest.cloudvdn.com/xrtest/input2",
            },
        ],
        "config": {
            "layout": "203",
            "width": 1280,
            "height": 720,
            "fps": 25,
            "kbps": 2000,
        },
        "outputs": [
            {
                "type": "rtmp",
                "url": "rtmp://pili-publish.qnsdk.com/sdk-live/testmediamerge123",
            }
        ],
    }

    bucket_name = "sdk-miku-test"
    print(f"Testing create merge API with bucket: {bucket_name}")
    response = test_create_stream(bucket_name, merge_body)
    print(f"响应内容: {response}")
