# 查询HTTP状态码次数、占比-RESTFul

## 接口名称
查询HTTP状态码次数、占比-RESTFul

## 接口描述
查询指定时间范围内HTTP状态码的次数和占比统计

## 请求方法
GET

## 请求路径
```
GET /?statistic=http&status&restful
```

## 请求参数
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| startTime | string | 是 | 开始时间，ISO8601格式 |
| endTime | string | 是 | 结束时间，ISO8601格式 |
| bucket | string | 否 | 空间名称，不指定则查询所有空间 |
| domain | string | 否 | 域名，不指定则查询所有域名 |

## 请求示例
```http
GET /?statistic=http&status&restful&startTime=2023-01-01T00:00:00Z&endTime=2023-01-01T23:59:59Z&bucket=test-bucket HTTP/1.1
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
| data | object | HTTP状态码统计信息 |
| data.totalRequests | integer | 总请求数 |
| data.statusStats | array | 状态码统计列表 |
| data.statusStats[].code | integer | HTTP状态码 |
| data.statusStats[].count | integer | 请求数量 |
| data.statusStats[].percentage | number | 占比（%） |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success",
  "data": {
    "totalRequests": 100000,
    "statusStats": [
      {
        "code": 200,
        "count": 95000,
        "percentage": 95.0
      },
      {
        "code": 404,
        "count": 3000,
        "percentage": 3.0
      },
      {
        "code": 500,
        "count": 2000,
        "percentage": 2.0
      }
    ]
  }
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