# 日志搜索异常日志TopN

## 接口名称
日志搜索异常日志TopN

## 接口描述
搜索异常日志并返回TopN列表

## 请求方法
GET

## 请求路径
```
GET /?statistic=log&abnormal&topn
```

## 请求参数
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| startTime | string | 是 | 开始时间，ISO8601格式 |
| endTime | string | 是 | 结束时间，ISO8601格式 |
| bucket | string | 否 | 空间名称，不指定则查询所有空间 |
| domain | string | 否 | 域名，不指定则查询所有域名 |
| n | integer | 否 | 返回前N条记录，默认10，最大100 |

## 请求示例
```http
GET /?statistic=log&abnormal&topn&startTime=2023-01-01T00:00:00Z&endTime=2023-01-01T23:59:59Z&bucket=test-bucket&n=20 HTTP/1.1
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
| data | array | 异常日志TopN列表 |
| data[].logContent | string | 日志内容 |
| data[].count | integer | 出现次数 |
| data[].errorType | string | 错误类型 |
| data[].timestamp | string | 最后出现时间 |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success",
  "data": [
    {
      "logContent": "Connection timeout",
      "count": 150,
      "errorType": "network",
      "timestamp": "2023-01-01T10:30:00Z"
    },
    {
      "logContent": "Authentication failed",
      "count": 85,
      "errorType": "auth",
      "timestamp": "2023-01-01T09:15:00Z"
    }
  ]
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