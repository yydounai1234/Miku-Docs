# API规范

遵循 RESTful API 设计规范，使用名词表示操作的对象
* `https://<service-code>.<region-code>.qiniumiku.com` 表示公共接入点，用于列举空间
* `https://<bucket>.<service-code>.<region-code>.qiniumiku.com` 表示空间
* `https://<bucket>.<service-code>.<region-code>.qiniumiku.com/<key>` 表示空间中的对象

使用 HTTP Request Method 与 资源(Resource) 配合，表示具体操作，常用的 HTTP Request Method 列表:
* `GET` 获取资源
* `POST` 创建资源
* `PUT` 全量更新资源（AWS 基本采用 PUT，表示创建资源）
* `PATCH` 部分更新资源
* `DELETE` 删除资源
* `HEAD` 获取资源元数据
* `OPTIONS` preflight 请求，需要响应正确的 access-control 信息

以 `domain` 作为一类资源(Resource)举例：
* `GET /?domain` 表示获取空间的域名列表
* `POST /?domain` 表示绑定域名
* `DELETE /?domain&name=<domain>` 表示解绑域名