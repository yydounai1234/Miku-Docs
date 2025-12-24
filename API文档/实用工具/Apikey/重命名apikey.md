# 重命名 apikey

## 接口名称
重命名 apikey

## 接口描述
修改指定Apikey的名称和描述

## 请求方法
PUT

## 请求路径
```
PUT /?apikey=<apikey>
```

## 请求参数
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| apikey | string | 是 | 要修改的Apikey值 |

## 请求Body
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| name | string | 否 | 新的Apikey名称 |
| description | string | 否 | 新的Apikey描述 |

## 请求示例
```http
PUT /?apikey=ak-1234567890abcdef HTTP/1.1
Host: <service-code>.<region-code>.qiniumiku.com
Authorization: <QiniuToken>
Content-Type: application/json

{
  "name": "updated-apikey-name",
  "description": "更新后的Apikey描述"
}
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
- 可以只修改名称或只修改描述
- Apikey值无法修改，如需更换请删除后重新创建

## 错误码
| 错误码 | 说明 |
|-------|------|
| 400 | 请求参数错误 |
| 401 | 鉴权失败 |
| 404 | Apikey不存在 |
| 500 | 服务端内部错误 |

## 鉴权方式
支持 QiniuToken、IAM 鉴权和 Apikey 鉴权，请参考[请求鉴权](../公共API规范/请求鉴权.md)文档。