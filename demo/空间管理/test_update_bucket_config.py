import os
import hmac
import hashlib
import base64
import urllib.parse
import json
from urllib.parse import urlparse
from http.client import HTTPSConnection, HTTPConnection

# 你的 AK 和 SK
AK = "QxZugR8TAhI38AiJ_cptTl3RbzLyca3t-AAiH-Hh"
SK = "4yv8mE9kFeoE31PVlIjWvi3nfTytwT0JiAxWjCDa"

def test_update_bucket_config(bucket_name, config_data):
    """
    测试修改空间配置接口
    
    Args:
        bucket_name (str): 空间名称
        config_data (dict): 配置数据
    """
    
    # 接口信息
    method = "PATCH"
    host = f"{bucket_name}.mls.cn-east-1.qiniumiku.com"
    path = "/?config"
    
    url = f"http://{host}{path}"
    print(f"Sending request to: {url}")
    
    # 将配置数据转换为JSON字符串
    body = json.dumps(config_data)
    
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
    # 测试修改空间配置，替换 "test-bucket-name" 为你想要修改的空间名称
    bucket_name = "sdk-live"
    print(f"Testing update bucket config API with bucket name: {bucket_name}")
    
    # 示例配置数据（请根据实际需求修改）
    config_data = {
        "status": "Enabled",
        "recording": {
            "enable": True,
            "objectBucket": "web-rtn-test",
            "expireDays": 0,
            "segmentDuration": 5,
            "snapshot": {
                "enable": True,
                "interval": 60,
                "filename": "yydounai66_{{.Bucket}}_{{.StreamID}}_{{.Title}}_{{.TimeSecond10}}",
                "format": "",
                "expireDays": 3
            }
        },
        "callbackUrl": "http://www.example.com",
        "streamConf": {
            "gopCacheMode": 0,
            "gopCacheNum": 10,
            "noDataTimeout": 10
        }
    }
    
    print("\n--- 修改空间配置 ---")
    response = test_update_bucket_config(bucket_name, config_data)
    print(f"响应内容: {response}")