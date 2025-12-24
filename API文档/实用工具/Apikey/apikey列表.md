# apikey 列表

## 接口名称
apikey 列表

## 接口描述
获取当前账户下所有的Apikey列表

## 请求方法
GET

## 请求路径
```
GET /?apikey
```

## 请求示例
```http
GET /?apikey HTTP/1.1
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
| data | array | Apikey列表 |
| data[].apikey | string | Apikey值（部分隐藏） |
| data[].name | string | Apikey名称 |
| data[].description | string | Apikey描述 |
| data[].createTime | string | 创建时间 |
| data[].lastUsedTime | string | 最后使用时间 |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success",
  "data": [
    {
      "apikey": "ak-123456******cdef",
      "name": "my-apikey-001",
      "description": "用于自动化脚本的Apikey",
      "createTime": "2023-01-01T00:00:00Z",
      "lastUsedTime": "2023-01-01T10:00:00Z"
    },
    {
      "apikey": "ak-789012******ghij",
      "name": "my-apikey-002",
      "description": "用于第三方集成的Apikey",
      "createTime": "2023-01-02T00:00:00Z",
      "lastUsedTime": "2023-01-02T09:00:00Z"
    }
  ]
}
```

## 注意事项
- 返回的Apikey值是部分隐藏的，无法获取完整值
- 如需获取完整Apikey值，需要重新创建

## 错误码
| 错误码 | 说明 |
|-------|------|
| 400 | 请求参数错误 |
| 401 | 鉴权失败 |
| 500 | 服务端内部错误 |

## 鉴权方式
支持 QiniuToken、IAM 鉴权和 Apikey 鉴权，请参考[请求鉴权](../公共API规范/请求鉴权.md)文档。