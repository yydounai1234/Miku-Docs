import hmac
import hashlib
import base64
import json
from urllib.parse import urlparse
from http.client import HTTPSConnection, HTTPConnection

# 你的 AK 和 SK
AK = "QxZugR8TAhI38AiJ_cptTl3RbzLyca3t-AAiH-Hh"
SK = "4yv8mE9kFeoE31PVlIjWvi3nfTytwT0JiAxWjCDa"


def test_create_pub_task(task_body, use_oversea=False):
    """
    测试创建 pub 转推任务接口

    Args:
        task_body (dict): 任务请求体，需包含 name/sourceUrls/runType/forwardUrls 等字段
        use_oversea (bool): 是否使用海外域名 pili-hw-pub.qiniuapi.com
    """

    # 接口信息
    method = "POST"
    host = "pub-manager.mikudns.com"
    path = "/tasks"
    url = f"https://{host}{path}"
    print(f"Sending request to: {url}")

    body = json.dumps(task_body)

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
    # 构造最小示例体，按需补充参数
    task_body = {
        "name": "task-002",
        "desc": "demo task",
        "sourceUrls": [
            {
                "url": "http://miku-test-play.qnsdk.com/sdk-miku-test/yydounai-test44.flv",
                "isp": "",
                "seek": 0,
                "videoType": 1,
                "rtspType": 0,
            }
        ],
        "runType": "seek",
        "forwardUrls": [
            {
                "url": "rtmp://miku-test-publish.qnsdk.com/sdk-miku-test/yydounai-test55",
                "isp": "",
            }
        ],
        "filter": {"ips": [], "area": "", "isp": ""},
        "loopTimes": 0,
        "retryTime": 60,
        "deliverStartTime": 1784947040000,
        "deliverStopTime": 1796390400000,
        "sustain": False,
        "preload": {"enable": True, "preloadTime": 1766390400000},
        "statusCallback": {
            "type": "JSON",
            "url": "https://callback.example.com",
            "vars": {
                "taskid": "$(taskID)",
                "status": "$(status)",
                "startTime": "$(startTime)",
                "stopTime": "$(stopTime)",
            },
        },
    }

    print("Testing create pub task API...")
    response = test_create_pub_task(task_body, use_oversea=False)
    print(f"响应内容: {response}")
