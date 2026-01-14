# 描述
apikey 列表

# 接口信息
- **请求方法**: `GET`
- **请求地址**: mls.cn-east-1.qiniumiku.com
- **请求路径**: /

# 请求参数
## Query 参数
| 参数名称 | 类型 | 必填 | 示例值 | 描述 |
|:---|:---:|:---:|:---|:---|
| apikeys | string | 必须 | - | 固定字段 |

## Header 参数
| 参数名称 | 类型 | 必填 | 示例值 | 描述 |
|:---|:---:|:---:|:---|:---|
| Host | string | 是 | mls.cn-east-1.qiniumiku.com | 请求的服务域名 |
| Authorization | string | 是 | `<QiniuToken>` | 管理凭证 QiniuToken，[生成规则](/mikustream/api/12893/mikustream-live-http-requests-authentication) |



# 请求示例
```http
GET /?apikeys HTTP/1.1
Host: mls.cn-east-1.qiniumiku.com
Authorization: <QiniuToken>
Content-Type: application/json

```

# 返回响应
## 响应状态码
- **请查阅**: [这里](/mikustream/api/12894/mikustream-live-error-code)

## 响应示例
```json
[
  {
      "id": "fed056ac-bafd-4927-b6a1-22d74ff779e7",
      "name": "虢强",
      "key": "mk-sads****************************************sadc",
      "createdAt": "2025-04-08 14:38:06"
  },
  {
      "id": "fed056ac-bafd-4927-b6a1-22d74ff77923x",
      "name": "肥勇",
      "key": "mk-aads***********************************dasc",
      "createdAt": "2024-12-10 09:13:16"
  },
  {
      "id": "fed056ac-bafd-4927-b6a1-22d74ff77921r",
      "name": "屠国强",
      "key": "mk-sscd*************************************das",
      "createdAt": "2024-10-01 21:24:19"
  }
]
```