import os
import hmac
import hashlib
import base64
from urllib.parse import urlencode, urlparse
from http.client import HTTPSConnection, HTTPConnection

# 你的 AK 和 SK
AK = os.getenv("Access_key")
SK = os.getenv("Secret_key")


def test_get_stream_history_activity(
    start,
    end,
    region="cn-east-1",
    domain=None,
    bucket=None,
    stream_name=None,
    limit=None,
    offset=None,
    order_by=None,
):
    """
    测试流历史推流记录接口。

    Args:
        start (str): 查询开始时间，支持毫秒/秒级时间戳、日期时间或日期格式
        end (str): 查询结束时间，支持毫秒/秒级时间戳、日期时间或日期格式
        region (str): 区域，默认 cn-east-1
        domain (str | None): 推流域名，domain/bucket 二选一
        bucket (str | None): 空间名称，domain/bucket 二选一
        stream_name (str | None): 流名
        limit (int | None): 每页返回条数
        offset (int | None): 分页偏移量
        order_by (str | None): 排序方式，可选 publish_time_asc/publish_time_desc/
            stream_name_asc/stream_name_desc
    """

    if not domain and not bucket:
        raise ValueError("domain 和 bucket 需至少提供一个")

    valid_order_by = {
        "publish_time_asc",
        "publish_time_desc",
        "stream_name_asc",
        "stream_name_desc",
    }
    if order_by is not None and order_by not in valid_order_by:
        raise ValueError(f"order_by 必须是以下值之一: {', '.join(sorted(valid_order_by))}")

    method = "GET"
    host = "mls.cn-east-1.qiniumiku.com"
    path = f"/"

    query_params = {
        "start": str(start),
        "end": str(end),
    }
    if domain is not None:
        query_params["domain"] = domain
    if bucket is not None:
        query_params["bucket"] = bucket
    if stream_name is not None:
        query_params["streamName"] = stream_name
    if limit is not None:
        query_params["limit"] = str(limit)
    if offset is not None:
        query_params["offset"] = str(offset)
    if order_by is not None:
        query_params["orderBy"] = order_by

    query_string = urlencode(query_params)
    url = f"http://{host}{path}?historyactivity&{query_string}"
    print(f"Sending request to: {url}")

    # 无请求体
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
    # 替换为真实的时间、空间/域名等查询条件
    start_time = "20060102"
    end_time = "20060103"
    bucket_name = "sdk-live"

    print("Testing stream history activity API...")
    response = test_get_stream_history_activity(
        start=start_time,
        end=end_time,
        bucket=bucket_name,
    )
    print(f"响应内容: {response}")
