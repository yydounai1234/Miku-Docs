# 创建 apikey

## 接口名称
创建 apikey

## 接口描述
创建一个新的Apikey用于身份验证和授权

## 请求方法
POST

## 请求路径
```
POST /?apikey
```

## 请求Body
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| name | string | 是 | Apikey名称 |
| description | string | 否 | Apikey描述 |

## 请求示例
```http
POST /?apikey HTTP/1.1
Host: <service-code>.<region-code>.qiniumiku.com
Authorization: <QiniuToken>
Content-Type: application/json

{
  "name": "my-apikey-001",
  "description": "用于自动化脚本的Apikey"
}
```

## 响应参数
| 参数名称 | 类型 | 说明 |
|---------|------|------|
| requestId | string | 请求ID |
| code | integer | 响应码 |
| message | string | 响应消息 |
| data | object | Apikey信息 |
| data.apikey | string | Apikey值 |
| data.name | string | Apikey名称 |
| data.description | string | Apikey描述 |
| data.createTime | string | 创建时间 |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success",
  "data": {
    "apikey": "ak-1234567890abcdef",
    "name": "my-apikey-001",
    "description": "用于自动化脚本的Apikey",
    "createTime": "2023-01-01T00:00:00Z"
  }
}
```

## 注意事项
- Apikey一旦创建，仅在响应中返回一次，请妥善保存
- Apikey具有与创建者相同的权限
- 建议为不同的应用场景创建不同的Apikey

## 错误码
| 错误码 | 说明 |
|-------|------|
| 400 | 请求参数错误 |
| 401 | 鉴权失败 |
| 500 | 服务端内部错误 |

## 鉴权方式
支持 QiniuToken、IAM 鉴权和 Apikey 鉴权，请参考[请求鉴权](../公共API规范/请求鉴权.md)文档。