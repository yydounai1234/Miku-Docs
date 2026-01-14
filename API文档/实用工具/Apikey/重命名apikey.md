# 描述
重命名 apikey

# 接口信息
- **请求方法**: `POST`
- **请求地址**: mls.cn-east-1.qiniumiku.com
- **请求路径**: /

# 请求参数
## Query 参数
| 参数名称 | 类型 | 必填 | 示例值 | 描述 |
|:---|:---:|:---:|:---|:---|
| apikeyRename | string | 必须 | - | 固定字段 |

## Header 参数
| 参数名称 | 类型 | 必填 | 示例值 | 描述 |
|:---|:---:|:---:|:---|:---|
| Host | string | 是 | mls.cn-east-1.qiniumiku.com | 请求的服务域名 |
| Authorization | string | 是 | `<QiniuToken>` | 管理凭证 QiniuToken，[生成规则](/mikustream/api/12893/mikustream-live-http-requests-authentication) |


## Body 参数 (application/json)
示例：
```json
{
    "id": "string",
    "name": "string"
}
```
## 参数
| 参数名称 | 类型 | 是否必需 | 说明 |
|:---|:---:|:---:|:---|
| id | string | 必须 | apikey id |
| name | string | 必须 | 重命名的 apikey 名 |


# 请求示例
```http
POST /?apikeyRename HTTP/1.1
Host: mls.cn-east-1.qiniumiku.com
Authorization: <QiniuToken>
Content-Type: application/json

{
  "id": "f756f547-7d1d-46d1-b042-df925c3255c0",
  "name": "miku-test"
}
```

# 返回响应
## 响应状态码
- **请查阅**: [这里](/mikustream/api/12894/mikustream-live-error-code)

## 响应示例
```json
{}
```