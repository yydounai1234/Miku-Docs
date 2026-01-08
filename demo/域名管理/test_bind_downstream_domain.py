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

def test_bind_downstream_domain(bucket_name, domain, domain_type=None):
    """
    测试绑定下行域名接口
    
    Args:
        bucket_name (str): 空间名称
        domain (str): 要绑定的域名
        domain_type (str): 域名类型（可选）
    """
    
    # 接口信息
    method = "POST"
    host = f"{bucket_name}.mls.cn-east-1.qiniumiku.com"
    path = "/?domain"
    
    url = f"http://{host}{path}"
    print(f"Sending request to: {url}")
    
    # 构造请求体
    body_data = {
        "domain": domain
    }
    if domain_type:
        body_data["type"] = domain_type
    body = json.dumps(body_data)
    
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
    # 测试绑定下行域名，替换为实际的空间名称和域名信息
    bucket_name = "test-bucket-name"
    domain = "test-bucket-play.qnsdk.com"
    domain_type = "liveRtmp"  # 可选: liveRtmp, liveHls, liveDash, liveFlv, whep, live, liveSrt
    
    print(f"Testing bind downstream domain API with bucket name: {bucket_name}")
    print(f"Domain: {domain}, Type: {domain_type}")
    
    response = test_bind_downstream_domain(bucket_name, domain, domain_type)
    print(f"响应内容: {response}")