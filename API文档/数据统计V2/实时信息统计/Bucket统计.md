# Bucket统计

## 接口名称
实时信息统计Bucket统计

## 接口描述
获取指定空间的实时统计信息

## 请求方法
GET

## 请求路径
```
GET /?statistic=realtime&bucket=<bucket>
```

## 请求参数
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| bucket | string | 是 | 空间名称 |

## 请求示例
```http
GET /?statistic=realtime&bucket=test-bucket HTTP/1.1
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
| data | object | 空间实时统计信息 |
| data.bucket | string | 空间名称 |
| data.activeStreams | integer | 活跃流数量 |
| data.totalViewers | integer | 总观看人数 |
| data.currentBandwidth | integer | 当前总带宽使用量（bps） |
| data.currentTraffic | integer | 当前总流量（字节） |
| data.lastUpdateTime | string | 最后更新时间 |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success",
  "data": {
    "bucket": "test-bucket",
    "activeStreams": 15,
    "totalViewers": 1250,
    "currentBandwidth": 25000000,
    "currentTraffic": 10737418240,
    "lastUpdateTime": "2023-01-01T10:30:00Z"
  }
}
```

## 错误码
| 错误码 | 说明 |
|-------|------|
| 400 | 请求参数错误 |
| 401 | 鉴权失败 |
| 404 | 空间不存在 |
| 500 | 服务端内部错误 |

## 鉴权方式
支持 QiniuToken、IAM 鉴权和 Apikey 鉴权，请参考[请求鉴权](../../../公共API规范/请求鉴权.md)文档。