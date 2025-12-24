# 查询切分离线日志-RESTFul

## 接口名称
查询切分离线日志-RESTFul

## 接口描述
使用RESTFul风格接口查询切分后的离线日志

## 请求方法
GET

## 请求路径
```
GET /?statistic=log&offline&split&restful
```

## 请求参数
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| startTime | string | 是 | 开始时间，ISO8601格式 |
| endTime | string | 是 | 结束时间，ISO8601格式 |
| bucket | string | 否 | 空间名称，不指定则查询所有空间 |
| domain | string | 否 | 域名，不指定则查询所有域名 |
| level | string | 否 | 日志级别，如ERROR, WARN, INFO |
| limit | integer | 否 | 返回数量限制，默认20，最大100 |
| marker | string | 否 | 分页标记 |

## 请求示例
```http
GET /?statistic=log&offline&split&restful&startTime=2023-01-01T00:00:00Z&endTime=2023-01-01T23:59:59Z&bucket=test-bucket&level=ERROR&limit=10 HTTP/1.1
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
| data | array | 切分离线日志列表 |
| data[].logId | string | 日志ID |
| data[].timestamp | string | 日志时间 |
| data[].level | string | 日志级别 |
| data[].content | string | 日志内容 |
| data[].bucket | string | 空间名称 |
| data[].domain | string | 域名 |
| data[].splitInfo | object | 切分信息 |
| data[].splitInfo.segmentId | string | 分段ID |
| data[].splitInfo.segmentStart | string | 分段开始时间 |
| data[].splitInfo.segmentEnd | string | 分段结束时间 |
| marker | string | 分页标记，用于获取下一页数据 |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success",
  "data": [
    {
      "logId": "log-123456",
      "timestamp": "2023-01-01T10:30:00Z",
      "level": "ERROR",
      "content": "Connection timeout error occurred",
      "bucket": "test-bucket",
      "domain": "play.example.com",
      "splitInfo": {
        "segmentId": "seg-abc123",
        "segmentStart": "2023-01-01T10:00:00Z",
        "segmentEnd": "2023-01-01T10:30:00Z"
      }
    },
    {
      "logId": "log-789012",
      "timestamp": "2023-01-01T09:15:00Z",
      "level": "ERROR",
      "content": "Authentication failed",
      "bucket": "test-bucket",
      "domain": "publish.example.com",
      "splitInfo": {
        "segmentId": "seg-def456",
        "segmentStart": "2023-01-01T09:00:00Z",
        "segmentEnd": "2023-01-01T09:30:00Z"
      }
    }
  ],
  "marker": "eyJsb2dJZCI6ImxvZy03ODkwMTIifQ=="
}
```

## 错误码
| 错误码 | 说明 |
|-------|------|
| 400 | 请求参数错误 |
| 401 | 鉴权失败 |
| 500 | 服务端内部错误 |

## 鉴权方式
支持 QiniuToken、IAM 鉴权和 Apikey 鉴权，请参考[请求鉴权](../../公共API规范/请求鉴权.md)文档。