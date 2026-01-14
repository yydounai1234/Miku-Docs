# 描述
创建 apikey

# 接口信息
- **请求方法**: `POST`
- **请求地址**: mls.cn-east-1.qiniumiku.com
- **请求路径**: /

# 请求参数
## Query 参数
| 参数名称 | 类型 | 必填 | 示例值 | 描述 |
|:---|:---:|:---:|:---|:---|
| apikey | string | 必须 | - | 固定字段 |

## Header 参数
| 参数名称 | 类型 | 必填 | 示例值 | 描述 |
|:---|:---:|:---:|:---|:---|
| Host | string | 是 | mls.cn-east-1.qiniumiku.com | 请求的服务域名 |
| Authorization | string | 是 | `<QiniuToken>` | 管理凭证 QiniuToken，[生成规则](/mikustream/api/12893/mikustream-live-http-requests-authentication) |


## Body 参数 (application/json)
示例：
```json
{
  "name": "string"
}
```
## 参数
| 参数名称 | 类型 | 是否必需 | 说明 |
|:---|:---:|:---:|:---|
| name | string | 必须 | 长度 1-20 之间 内容不做校验 |


# 请求示例
```http
GET /?apikey HTTP/1.1
Host: mls.cn-east-1.qiniumiku.com
Authorization: <QiniuToken>
Content-Type: application/json

{
    "name": "test"
}
```

# 返回响应
## 响应状态码
- **请查阅**: [这里](/mikustream/api/12894/mikustream-live-error-code)

## 响应示例
```json
{
    "id": "fed056ac-bafd-4927-b6a1-22d74ff779e7",
    "name": "滑敏",
    "key": "mk-659fcc74e251a87e7227a11b2e6d653757fc04715314b4f8ce3e384a956c69af",
    "createdAt": "2025-06-28 17:05:53"
}
```
## 响应参数
| 参数名称 | 类型 | 说明 | 是否必需 |
|:---------|:------|:------|:----------|
| id | string | id | 必需 |
| name | string | 名字 | 必需 |
| key | string | apikey | 必需 |
| createdAt | string | 创建时间 | 必需 |
