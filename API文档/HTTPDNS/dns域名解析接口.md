# 描述
dns域名解析接口

# 接口信息
- **请求方法**: GET
- **请求地址**: `mls.cn-east-1.qiniumiku.com
- **请求路径**: /

# 请求参数
## Query 参数
| 参数名称 | 类型 | 必填 | 示例值 | 描述 |
|:---|:---:|:---:|:---|:---|
| dns | string | 必须 | 无 | 固定字段 |
| domain | string | 必须 | 无 | 请求解析的域名，多个域名使用","进行分割 |
| ip | string | 必须 | 无 | HTTPDNS 服务端可以基于客户端 IP 地址的地理位置和所属网络运营商返回匹配的解析结果 |
| type | integer | 可选 | 无 | 0-获取双栈地址，1-仅IPV4地址，2-仅IPV6地址，默认是1 |


## Header 参数
|   参数名	|    类型	   |必填	 |示例值	|描述|
|:--------- |-----------|:-----|:---------|:---|
| Host | string | 是 | mls.cn-east-1.qiniumiku.com | 请求的服务域名 |
| Authorization | string | 是 | `<QiniuToken>` | 管理凭证 QiniuToken，[生成规则](/mikustream/api/12893/mikustream-live-http-requests-authentication) |


## 请求示例
```http
GET /?dns=&domain=www.example.com&ip=221.180.215.6&type=0 HTTP/1.1
Host: mls.cn-east-1.qiniumiku.com
Authorization: <QiniuToken>
Content-Type: application/json

```

# 返回响应

## 响应状态码
- **请查阅**: [这里](/mikustream/api/12894/mikustream-live-error-code)

## 响应示例
```json
{
  "dns": [
      {
          "domain": "www.baidu.com",
          "ips": [
              "120.226.85.102",
              "120.226.85.103",
              "120.226.85.104",
              "120.226.85.105",
              "120.226.85.101"
          ],
          "ipsv6": [
              "2400:3200:1300:0:0:0:XX:XX"
          ],
          "ttl": 60
      }
  ],
  "connectId": "QXV0aG9yaXphdGlvbg"
}

```

## 响应参数
| 参数名称 | 类型 | 说明 | 是否必需 |
|:---------|:------|:------|:----------|
| dns | array [object]  | dns返回结果 | 必需 |
| connectId | string | 连接id，用于定位问题 | 必需 |
| code | string | 业务错误码，1000代表成功，其它均为失败 | 必需 |
| message | string | 错误码详细描述 | 可选 |
| userIp | string | 请求ip | 必需 |
| userLoc | string | 请求ip的地域信息 | 必需 |
| userIsp | string | 请求ip的运营商信息 | 必需 |

### <span id="dns">dns</span>
| 字段 | 类型 | 必填 | 取值范围 | 描述 |
|:---|:---:|:---:|:---:|:---|
| domain | string | 是 | - | 解析的域名 |
| ips | array[string] | 是 | - | IPV4解析列表 |
| ipsv6 | array[string] | 是 | - | IPV6解析列表 |
| ttl | integer | 是 | - | 该域名解析结果的TTL缓存时间，默认60s |

