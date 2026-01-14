# 描述
删除 apikey

# 接口信息
- **请求方法**: `DELETE`
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
  "id": "8225e0a6-6e33-13ae-b071-5375a54d5870"
}
```
## 参数
| 参数名称 | 类型 | 是否必需 | 说明 |
|:---|:---:|:---:|:---|
| id | string | 必须 | apikey id |


# 请求示例
```http
DELETE /?apikey HTTP/1.1
Host: mls.cn-east-1.qiniumiku.com
Authorization: <QiniuToken>
Content-Type: application/json

{
  "id": "8225e0a6-6e33-13ae-b071-5375a54d5870"
}
```

# 返回响应
## 响应状态码
- **请查阅**: [这里](/mikustream/api/12894/mikustream-live-error-code)

## 响应示例
```json
{}
```