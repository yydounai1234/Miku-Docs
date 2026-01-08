import os
import hmac
import hashlib
import base64
import urllib.parse
import json
from urllib.parse import urlparse
from http.client import HTTPSConnection, HTTPConnection

# 你的 AK 和 SK
AK = os.getenv("Access_key")
SK = os.getenv("Secret_key")

def test_get_bucket_config(bucket_name, with_config=False):
    """
    测试获取空间配置接口
    
    Args:
        bucket_name (str): 空间名称
        with_config (bool): 是否添加config参数
    """
    
    # 接口信息
    method = "GET"
    host = f"{bucket_name}.mls.cn-east-1.qiniumiku.com"
    path = "/"
    
    # 添加config查询参数（如果需要）
    if with_config:
        path += "?config"
    
    url = f"http://{host}{path}"
    print(f"Sending request to: {url}")
    
    # 使用空的JSON body
    body = "{}"
    
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
    hmac_sha1 = hmac.new(sk.encode('utf-8'), data.encode('utf-8'), hashlib.sha1)
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
        "Authorization": signature
    }
    
    conn.request(method, parsed_url.path + ("?" + parsed_url.query if parsed_url.query else ""), 
                 body=data, headers=headers)
    
    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    
    conn.close()
    
    return f"HTTP {response.status}: {response_body}"

def base64_url_safe_encode(data):
    encoded = base64.b64encode(data).decode('utf-8')
    encoded = encoded.replace('+', '-').replace('/', '_')
    return encoded

if __name__ == "__main__":
    # 测试获取空间配置，替换 "test-bucket-name" 为你想要查询的空间名称
    bucket_name = "test-bucket-name"
    print(f"Testing get bucket config API with bucket name: {bucket_name}")
    
    # 不带config参数的请求
    print("\n--- 不带config参数 ---")
    response1 = test_get_bucket_config(bucket_name, with_config=False)
    print(f"响应内容: {response1}")
    
    # 带config参数的请求
    print("\n--- 带config参数 ---")
    response2 = test_get_bucket_config(bucket_name, with_config=True)
    print(f"响应内容: {response2}")