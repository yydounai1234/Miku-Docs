# 查询播放质量分析-RESTFul

## 接口名称
查询播放质量分析-RESTFul

## 接口描述
分析指定时间范围内直播流的播放质量

## 请求方法
GET

## 请求路径
```
GET /?statistic=quality&direction=play&startTime=<startTime>&endTime=<endTime>
```

## 请求参数
| 参数名称 | 类型 | 是否必填 | 说明 |
|---------|------|---------|------|
| startTime | string | 是 | 开始时间，ISO8601格式 |
| endTime | string | 是 | 结束时间，ISO8601格式 |
| bucket | string | 否 | 空间名称，不指定则查询所有空间 |
| streamId | string | 否 | 流ID，不指定则查询所有流 |
| domain | string | 否 | 域名，不指定则查询所有域名 |

## 请求示例
```http
GET /?statistic=quality&direction=play&startTime=2023-01-01T00:00:00Z&endTime=2023-01-01T23:59:59Z&bucket=test-bucket HTTP/1.1
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
| data | object | 质量分析结果 |
| data.totalViewers | integer | 总观看人数 |
| data.qualityStats | object | 质量统计 |
| data.qualityStats.excellent | integer | 优秀质量观看数 |
| data.qualityStats.good | integer | 良好质量观看数 |
| data.qualityStats.fair | integer | 一般质量观看数 |
| data.qualityStats.poor | integer | 较差质量观看数 |
| data.qualityStats.bad | integer | 很差质量观看数 |
| data.qualityDetails | array | 质量详情 |
| data.qualityDetails[].streamId | string | 流ID |
| data.qualityDetails[].bucket | string | 空间名称 |
| data.qualityDetails[].avgQualityScore | number | 平均质量评分（0-100） |
| data.qualityDetails[].avgLoadingTime | number | 平均加载时间（毫秒） |
| data.qualityDetails[].avgStutterRate | number | 平均卡顿率（%） |
| data.qualityDetails[].avgBitrate | integer | 平均码率（bps） |
| data.qualityDetails[].errorRate | number | 错误率（%） |

## 响应示例
```json
{
  "requestId": "558f0655-f373-48e6-93fb-7c91020462e0",
  "code": 200,
  "message": "success",
  "data": {
    "totalViewers": 2500,
    "qualityStats": {
      "excellent": 2000,
      "good": 400,
      "fair": 80,
      "poor": 20,
      "bad": 0
    },
    "qualityDetails": [
      {
        "streamId": "test-stream-001",
        "bucket": "test-bucket",
        "avgQualityScore": 92.5,
        "avgLoadingTime": 850,
        "avgStutterRate": 0.5,
        "avgBitrate": 1800000,
        "errorRate": 0.1
      },
      {
        "streamId": "test-stream-002",
        "bucket": "test-bucket",
        "avgQualityScore": 85.2,
        "avgLoadingTime": 1200,
        "avgStutterRate": 1.2,
        "avgBitrate": 1200000,
        "errorRate": 0.3
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