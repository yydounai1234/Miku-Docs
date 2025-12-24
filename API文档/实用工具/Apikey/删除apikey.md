# 删除 apikey

## 接口名称
删除 apikey

## 接口描述
删除指定的Apikey

## 请求方法
DELETE

## 请求路径
```
DELETE /?apikey=<apikey>
```

## 请求参数
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| apikey | string | 是 | 要删除的Apikey值 |

## 请求示例
```http
DELETE /?apikey=ak-1234567890abcdef HTTP/1.1
Host: <service-code>.<region-code>.qiniumiku.com
Authorization: <QiniuToken>
Content-Type: application/json
```

## 响应参数
| 参数名称 | 类型 | 说明 |
|---------|------|------|
| requestId | string | 请求ID |
| code | integer | 响应码 |
| message | string | 响应消息 |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success"
}
```

## 注意事项
- 删除Apikey是不可逆操作，请谨慎操作
- 删除后，使用该Apikey的所有应用将无法访问API

## 错误码
| 错误码 | 说明 |
|-------|------|
| 400 | 请求参数错误 |
| 401 | 鉴权失败 |
| 404 | Apikey不存在 |
| 500 | 服务端内部错误 |

## 鉴权方式
支持 QiniuToken、IAM 鉴权和 Apikey 鉴权，请参考[请求鉴权](../公共API规范/请求鉴权.md)文档。