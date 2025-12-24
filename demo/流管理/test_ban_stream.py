import hmac
import hashlib
import base64
import json
from urllib.parse import urlparse
from http.client import HTTPSConnection, HTTPConnection

# 你的 AK 和 SK
AK = "QxZugR8TAhI38AiJ_cptTl3RbzLyca3t-AAiH-Hh"
SK = "4yv8mE9kFeoE31PVlIjWvi3nfTytwT0JiAxWjCDa"


def test_ban_stream(bucket_name, stream_key, forbidden_till=0):
    """
    测试封禁流接口

    Args:
        bucket_name (str): 流所属的空间名称
        stream_key (str): 流名称
        forbidden_till (int | None): 禁播结束时间，Unix 秒级时间戳。
            0 表示永久封禁，-1 表示解除封禁，默认 0。
    """

    # 接口信息
    method = "POST"
    host = f"{bucket_name}.mls.cn-east-1.qiniumiku.com"
    path = f"/{stream_key}"
    # forbid 无值参数，bucket/streamKey 按文档放在查询串中
    url = f"http://{host}{path}?forbid&bucket={bucket_name}&streamKey={stream_key}"
    print(f"Sending request to: {url}")

    # 请求体
    body_dict = {}
    if forbidden_till is not None:
        body_dict["forbiddenTill"] = forbidden_till
    body = json.dumps(body_dict)

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
        body=data,
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
    # 测试封禁流，替换为实际空间名称和流名称
    bucket_name = "sdk-miku-test"
    stream_key = "yydounai-test"
    forbidden_till = 0  # 0 永久封禁，-1 解除封禁
    print(
        f"Testing ban stream API with bucket name: {bucket_name}, stream key: {stream_key}, forbiddenTill: {forbidden_till}"
    )
    response = test_ban_stream(bucket_name, stream_key, forbidden_till)
    print(f"响应内容: {response}")
