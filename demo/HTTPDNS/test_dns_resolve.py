import os
import hmac
import hashlib
import base64
from urllib.parse import urlencode, urlparse
from http.client import HTTPSConnection, HTTPConnection

# 你的 AK 和 SK
AK = os.getenv("Access_key")
SK = os.getenv("Secret_key")


def test_dns_resolve(domains, client_ip, record_type=1):
    """
    测试 HTTPDNS 域名解析接口。

    Args:
        domains (str | list[str]): 待解析的域名，支持以列表传入后自动拼接为逗号分隔字符串。
        client_ip (str): 客户端 IP，服务端会基于此返回匹配的解析结果。
        record_type (int | None): 0-双栈，1-仅 IPv4，2-仅 IPv6，默认 1。None 时不携带 type 参数。
    """

    if isinstance(domains, (list, tuple)):
        domain_param = ",".join(domains)
    else:
        domain_param = domains

    method = "GET"
    host = "mls.cn-east-1.qiniumiku.com"
    path = "/"

    query_params = {
        "dns": "",
        "domain": domain_param,
        "ip": client_ip,
    }

    if record_type is not None:
        query_params["type"] = str(record_type)

    query_string = urlencode(query_params)
    url = f"http://{host}{path}?{query_string}"
    print(f"Sending request to: {url}")

    body = "{}"

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
        body=data if data else None,
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
    sample_domains = ["www.example.com", "www.baidu.com"]
    sample_ip = "221.180.215.6"

    print(f"Testing DNS resolve API with domains: {sample_domains} and client IP: {sample_ip}")
    response = test_dns_resolve(sample_domains, sample_ip, record_type=0)
    print(f"响应内容: {response}")
