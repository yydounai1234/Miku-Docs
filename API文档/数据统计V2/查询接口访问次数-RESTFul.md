# 查询接口访问次数-RESTFul

## 接口名称
查询接口访问次数-RESTFul

## 接口描述
查询指定时间范围内各接口的访问次数统计

## 请求方法
GET

## 请求路径
```
GET /?statistic=api&access&restful
```

## 请求参数
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| startTime | string | 是 | 开始时间，ISO8601格式 |
| endTime | string | 是 | 结束时间，ISO8601格式 |
| bucket | string | 否 | 空间名称，不指定则查询所有空间 |
| limit | integer | 否 | 返回数量限制，默认20，最大100 |

## 请求示例
```http
GET /?statistic=api&access&restful&startTime=2023-01-01T00:00:00Z&endTime=2023-01-01T23:59:59Z&bucket=test-bucket&limit=10 HTTP/1.1
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
| data | array | 接口访问统计列表 |
| data[].apiName | string | 接口名称 |
| data[].method | string | 请求方法 |
| data[].count | integer | 访问次数 |
| data[].avgResponseTime | number | 平均响应时间（毫秒） |
| data[].errorCount | integer | 错误次数 |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success",
  "data": [
    {
      "apiName": "获取流信息",
      "method": "GET",
      "count": 5000,
      "avgResponseTime": 45.5,
      "errorCount": 50
    },
    {
      "apiName": "创建流",
      "method": "POST",
      "count": 1200,
      "avgResponseTime": 120.3,
      "errorCount": 12
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