# Stream统计

## 接口名称
实时信息统计Stream统计

## 接口描述
获取指定流的实时统计信息

## 请求方法
GET

## 请求路径
```
GET /?statistic=realtime&stream&id=<streamId>
```

## 请求参数
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| id | string | 是 | 流ID |
| bucket | string | 是 | 空间名称 |

## 请求示例
```http
GET /?statistic=realtime&stream&id=test-stream-001&bucket=test-bucket HTTP/1.1
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
| data | object | 流实时统计信息 |
| data.streamId | string | 流ID |
| data.bucket | string | 空间名称 |
| data.status | string | 流状态 |
| data.viewers | integer | 当前观看人数 |
| data.bandwidth | integer | 当前带宽使用量（bps） |
| data.traffic | integer | 当前流量（字节） |
| data.resolution | string | 分辨率 |
| data.framerate | number | 帧率 |
| data.lastUpdateTime | string | 最后更新时间 |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success",
  "data": {
    "streamId": "test-stream-001",
    "bucket": "test-bucket",
    "status": "active",
    "viewers": 125,
    "bandwidth": 2500000,
    "traffic": 1073741824,
    "resolution": "1920x1080",
    "framerate": 30.0,
    "lastUpdateTime": "2023-01-01T10:30:00Z"
  }
}
```

## 错误码
| 错误码 | 说明 |
|-------|------|
| 400 | 请求参数错误 |
| 401 | 鉴权失败 |
| 404 | 流或空间不存在 |
| 500 | 服务端内部错误 |

## 鉴权方式
支持 QiniuToken、IAM 鉴权和 Apikey 鉴权，请参考[请求鉴权](../../../公共API规范/请求鉴权.md)文档。