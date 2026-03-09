---
name: miku
description: 将自然语言需求映射到七牛云 Miku 快直播 API action 并按结构化参数安全执行。用户用中文描述创建、查询、更新、删除七牛 Miku 快直播资源（空间、流、域名、证书、录制、转码模板、转推任务、统计、API Key）时使用；尤其当用户说“帮我获取到直播空间列表/直播空间有哪些/查询空间列表”时，必须自动映射到 `bucket-management/list_buckets` 并返回空间列表信息。
---

# Miku API 执行规范

适用于七牛云 Miku 快直播（Qiniu Miku Live）接口调用。

## 调度规则

1. 先匹配“高频意图直达规则”；未命中再查“接口清单”。
2. 按该 action 的 `input_schema`/`input_params` 校验参数。
3. 通过统一入口调用。

## 接口调用契约（JSON Schema）

### 输入字段表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `action` | `string` | 条件必填 | 精确 action（如 `bucket-management/list_buckets`） |
| `intent` | `string` | 条件必填 | 自然语言意图；未提供 `action` 时用于自动匹配 |
| `params_json` | `object` | 条件必填 | 目标函数参数对象；有参数时传入 |
| `params_file` | `string` | 条件必填 | 参数 JSON 文件路径 |
| `ak` | `string` | 否 | `Access_key`，传入则覆盖环境变量 |
| `sk` | `string` | 否 | `Secret_key`，传入则覆盖环境变量 |
| `config` | `string` | 否 | 配置文件路径 |
| `dry_run` | `boolean` | 否 | 默认 `false`；仅解析和校验，不发真实请求 |
| `topk` | `integer` | 否 | 默认 `5`，最小 `1`；`intent` 模式候选数量 |

输入约束：
- `action` 与 `intent` 二选一，至少提供一个。
- 有参数时：`params_json` 与 `params_file` 二选一，至少提供一个。
- 无参数时：`params_json`、`params_file` 可都不传。
- 不允许额外字段（`additionalProperties=false`）。

### 输出字段表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `resolved_action` | `string` | 是 | 实际执行的 action |
| `required_params` | `array<string>` | 否 | 请求 body 必填参数列表（仅 body，可理解为 `required_body_params`） |
| `optional_params` | `array<string>` | 否 | 请求 body 可选参数列表（仅 body） |
| `required_query_params` | `array<string>` | 否 | URL query 必填参数列表 |
| `optional_query_params` | `array<string>` | 否 | URL query 可选参数列表 |
| `required_host_params` | `array<string>` | 否 | Host 占位符必填参数列表（如 `<bucket_name>`） |
| `required_path_params` | `array<string>` | 否 | URL path 占位符必填参数列表（如 `<task_id>`） |
| `missing_required` | `array<string>` | 否 | 缺失的必填参数；使用 `body.xxx/query.xxx/host.xxx/path.xxx` 前缀 |
| `request_params_masked` | `object` | 否 | 脱敏后的请求参数 |
| `raw_response` | `string` | 否 | 原始响应文本 |
| `dry_run` | `boolean` | 否 | 是否 dry-run |
| `error` | `string` | 否 | 错误信息 |

输出约束：
- 必须返回 `resolved_action`。
- 允许扩展字段（`additionalProperties=true`）。

## 多语言自动调用规范

基于本文件的 `interface_name`、`input_schema`、`output_schema` 自动生成并执行请求。

### 鉴权规范

- 鉴权字段：`Access_key`、`Secret_key`。
- 凭证读取顺序：请求体显式字段 -> 环境变量。
- 环境变量名必须是：`Access_key`、`Secret_key`（区分大小写）。
- 签名算法：`HMAC-SHA1` + `Base64URL`。
- `Authorization` 格式：`Qiniu <AK>:<SIGN>`。

签名原文（`sign_data`）：

```text
有 body：
<METHOD> <PATH>[?<QUERY>]
Host: <HOST>
Content-Type: application/json

<BODY>

无 body：
<METHOD> <PATH>[?<QUERY>]
Host: <HOST>

```

其中：
- `QUERY` 为空时不拼接 `?`。
- `Host` 必须使用最终请求主机名参与签名；若接口 `domain` 含 `<bucket_name>`，必须先替换为真实值（如 `prod-live-hub.mls.cn-east-1.qiniumiku.com`）。
- 当参数为 `{}`（空参数）时，按“无 body”模式处理：请求中不带 `Content-Type`，不带 body。
- `curl` 在空参数场景不需要 `-d '{}'`。
- 请求头与签名必须一致：若 `sign_data` 中没有 `Content-Type`，实际请求也不要带 `Content-Type`，否则会鉴权失败。
- 无 body 时，`sign_data` 仍需保留头部结束空行（即 `Host: <HOST>` 后仍保留 `\n\n`）。
- 有 body 时，`sign_data` 才包含 `Content-Type: application/json` 与 `<BODY>`。
- `Base64URL` 仅执行 `+ -> -`、`/ -> _`；`=` 必须原样保留，不能删除或替换为空字符串。

按语言实现 `HMAC-SHA1`（运行时必须匹配当前语言）：
- `javascript`（纯前端）：`Web Crypto API`（`window.crypto.subtle.importKey/sign`）。
- `nodejs`：`crypto.createHmac('sha1', sk).update(sign_data).digest()`。
- `go`：`hmac.New(sha1.New, []byte(sk))`。
- `java`：`Mac.getInstance(\"HmacSHA1\")` + `SecretKeySpec`。
- `php`：`hash_hmac('sha1', $signData, $sk, true)`。
- `curl`：用系统命令（如 `openssl dgst -sha1 -hmac`）在 shell 内计算；不可依赖其他语言运行时。
- 所有语言必须生成同一 `sign_data` 字节序列；签名不一致时优先排查换行、UTF-8 编码、`Base64URL` 替换规则。
- 一致性校验（空间列表）：
  - `method`: `GET`
  - `host`: `mls.cn-east-1.qiniumiku.com`
  - `path`: `/`
  - `body`: 无
  - `content-type`: 无
  - 期望：同一凭证与同一请求下，多语言计算出的 `SIGN` 必须一致。

创建空间签名示例（避免 Host 漏替换）：
- 场景：创建直播空间 `prod-live-hub`（`bucket-management/create_bucket`）
- 请求：`PUT /`
- 正确 `Host`：`prod-live-hub.mls.cn-east-1.qiniumiku.com`
- `sign_data`（无 body）：
```text
PUT /
Host: prod-live-hub.mls.cn-east-1.qiniumiku.com

```
- 若错误使用 `Host: mls.cn-east-1.qiniumiku.com` 参与签名，会导致签名校验失败。

### 自动执行策略

1. 解析输入，得到 `interface_name` 与参数对象。
2. 按 `input_schema` 做类型与必填校验。
3. 组装标准请求：`method`、`host`、`path`、`query`、`body`、`headers`。
4. 按语言优先级执行，直到成功或全部失败。
5. 将响应映射到接口 `output_schema`。

### 高频意图直达规则

- 命中短语（任一命中即触发）：
  - `帮我获取到直播空间列表`
  - `直播空间有哪些`
  - `查询直播空间列表`
  - `获取空间列表`
- 固定映射：
  - `action_key`: `bucket-management/list_buckets`
  - `interface_name`: `list_buckets`
  - `params`: `{}`
- 返回要求：
  - 从 `raw_response` 提取 `buckets` 数组。
  - 输出 `bucket_count` 与 `bucket_names`。

直播空间列表结果 Schema：

```json
{
  "type": "object",
  "properties": {
    "resolved_action": { "type": "string", "const": "bucket-management/list_buckets" },
    "bucket_count": { "type": "integer" },
    "bucket_names": {
      "type": "array",
      "items": { "type": "string" }
    },
    "buckets": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "region": { "type": "string" },
          "status": { "type": "string" },
          "creationDate": { "type": "string" }
        },
        "required": ["name"],
        "additionalProperties": true
      }
    },
    "raw_response": { "type": "string" },
    "error": { "type": "string" }
  },
  "required": ["resolved_action"],
  "additionalProperties": true
}
```

### 语言优先级与回退

- 默认顺序：`curl` -> `javascript` -> `nodejs` -> `go` -> `java` -> `php`。
- `javascript` 指纯前端 JavaScript（浏览器环境），不依赖 Node.js。
- 若用户指定 `preferred_languages`，先按用户顺序执行，再按默认顺序补齐未尝试语言。
- 以下错误触发回退到下一语言：
  - 运行时不存在（命令缺失、编译器缺失、依赖缺失）。
  - 代码模板渲染失败。
  - 请求发送失败（连接错误、超时、TLS 错误）。
- 若已收到 `HTTP` 响应则不再切换语言，直接按响应返回。

### 最终请求示例（按 Host）

说明：
- 下方均展示“请求内容 + 对应 `sign_data` 原文”。
- `sign_data` 中的 `<BODY>` 必须与实际发送的 body 字符串完全一致（包含空格与换行差异）。
- 若 `sign_data` 没有 `Content-Type`，实际请求也不要带 `Content-Type`。

#### Host: `mls.cn-east-1.qiniumiku.com`

无 body（`bucket-management/list_buckets`）：

```http
GET / HTTP/1.1
Host: mls.cn-east-1.qiniumiku.com
Authorization: Qiniu <AK>:<SIGN>
```

```text
GET /
Host: mls.cn-east-1.qiniumiku.com

```

有 body（`live-stream-transcoding-template/add_transcoding_template`）：

```http
POST /?codecTemplate HTTP/1.1
Host: mls.cn-east-1.qiniumiku.com
Content-Type: application/json
Authorization: Qiniu <AK>:<SIGN>

{"name":"demo-template","vcodec":"h264"}
```

```text
POST /?codecTemplate
Host: mls.cn-east-1.qiniumiku.com
Content-Type: application/json

{"name":"demo-template","vcodec":"h264"}
```

#### Host: `<bucket_name>.mls.cn-east-1.qiniumiku.com`

无 body（`bucket-management/create_bucket`，示例 bucket：`prod-live-hub`）：

```http
PUT / HTTP/1.1
Host: prod-live-hub.mls.cn-east-1.qiniumiku.com
Authorization: Qiniu <AK>:<SIGN>
```

```text
PUT /
Host: prod-live-hub.mls.cn-east-1.qiniumiku.com

```

有 body（`bucket-management/update_bucket_config`）：

```http
PATCH /?config HTTP/1.1
Host: prod-live-hub.mls.cn-east-1.qiniumiku.com
Content-Type: application/json
Authorization: Qiniu <AK>:<SIGN>

{"publishSecurity":"dynamic"}
```

```text
PATCH /?config
Host: prod-live-hub.mls.cn-east-1.qiniumiku.com
Content-Type: application/json

{"publishSecurity":"dynamic"}
```

#### Host: `pub-manager.mikudns.com`

无 body（`pub-relay/query_pub_task`）：

```http
GET /tasks/<task_id> HTTP/1.1
Host: pub-manager.mikudns.com
Authorization: Qiniu <AK>:<SIGN>
```

```text
GET /tasks/<task_id>
Host: pub-manager.mikudns.com

```

有 body（`pub-relay/create_pub_task`）：

```http
POST /tasks HTTP/1.1
Host: pub-manager.mikudns.com
Content-Type: application/json
Authorization: Qiniu <AK>:<SIGN>

{"name":"relay-demo","src":"rtmp://src/live","dest":"rtmp://dest/live"}
```

```text
POST /tasks
Host: pub-manager.mikudns.com
Content-Type: application/json

{"name":"relay-demo","src":"rtmp://src/live","dest":"rtmp://dest/live"}
```

#### Host: `miku-statd.qiniuapi.com`

无 body（`statistics/query_downflow_stat`）：

```http
GET /statd/v1/traffic/stat/downflow?begin=2026-03-01T00:00:00Z HTTP/1.1
Host: miku-statd.qiniuapi.com
Authorization: Qiniu <AK>:<SIGN>
```

```text
GET /statd/v1/traffic/stat/downflow?begin=2026-03-01T00:00:00Z
Host: miku-statd.qiniuapi.com

```

有 body（签名模板示例；当前接口清单下该 Host 主要为无 body 查询接口）：

```http
POST /statd/v1/example HTTP/1.1
Host: miku-statd.qiniuapi.com
Content-Type: application/json
Authorization: Qiniu <AK>:<SIGN>

{"begin":"2026-03-01T00:00:00Z"}
```

```text
POST /statd/v1/example
Host: miku-statd.qiniuapi.com
Content-Type: application/json

{"begin":"2026-03-01T00:00:00Z"}
```

### 自动调用输入（运行配置）Schema

```json
{
  "type": "object",
  "properties": {
    "interface_name": { "type": "string" },
    "params": { "type": "object" },
    "ak": { "type": "string" },
    "sk": { "type": "string" },
    "preferred_languages": {
      "type": "array",
      "items": { "type": "string", "enum": ["curl", "javascript", "nodejs", "go", "java", "php"] }
    },
    "timeout_seconds": { "type": "integer", "minimum": 1, "default": 30 },
    "max_attempts": { "type": "integer", "minimum": 1, "default": 5 }
  },
  "required": ["interface_name", "params"],
  "additionalProperties": false
}
```

### 自动调用输出（运行结果）Schema

```json
{
  "type": "object",
  "properties": {
    "interface_name": { "type": "string" },
    "language_used": { "type": "string", "enum": ["curl", "javascript", "nodejs", "go", "java", "php"] },
    "attempted_languages": {
      "type": "array",
      "items": { "type": "string" }
    },
    "resolved_action": { "type": "string" },
    "required_params": {
      "type": "array",
      "items": { "type": "string" }
    },
    "optional_params": {
      "type": "array",
      "items": { "type": "string" }
    },
    "required_query_params": {
      "type": "array",
      "items": { "type": "string" }
    },
    "optional_query_params": {
      "type": "array",
      "items": { "type": "string" }
    },
    "required_host_params": {
      "type": "array",
      "items": { "type": "string" }
    },
    "required_path_params": {
      "type": "array",
      "items": { "type": "string" }
    },
    "missing_required": {
      "type": "array",
      "items": { "type": "string" }
    },
    "param_position_errors": {
      "type": "array",
      "items": { "type": "string" }
    },
    "request_params_masked": { "type": "object" },
    "raw_response": { "type": "string", "description": "HTTP <status>: <body>" },
    "error": { "type": "string" }
  },
  "required": ["interface_name", "attempted_languages", "resolved_action"],
  "additionalProperties": true
}
```

## 接口清单（可直接调用）

精简字段：`interface_name`、`action_key`、`function_name`、`method`、`domain`、`path`、`required_params`、`optional_params`、`required_query_params`、`optional_query_params`、`required_host_params`、`required_path_params`。

说明：
- `required_params` / `optional_params` 仅表示 body 参数（即 `required_body_params` / `optional_body_params`）。
- `required_query_params` / `optional_query_params` 仅表示 URL query 参数，不属于 body。
- `required_host_params` 仅表示 Host 占位符参数（例如 `<bucket_name>.mls...` 中的 `bucket_name`），不属于 body。
- `required_path_params` 仅表示 URL path 占位符参数（例如 `/tasks/<task_id>` 中的 `task_id`），不属于 body。
- `action_key` 必须是完整 action（`<module>/<interface_name>`）；接口定位优先使用 `action_key`。
- `function_name` 使用固定生成规则：`call_` + `action_key` 中的 `/`、`-` 替换为 `_`。
- 任何 query/path 参数都不能出现在 `required_params` / `optional_params`；出现即视为映射错误，必须纠正后再发请求。
- 对于 `domain` 含占位符（如 `<bucket_name>`）的接口，签名与真实请求必须使用替换后的 Host，不能用占位符或公共域名代替。
- 个别接口存在联动约束（例如 `domain`/`bucket_id` 二选一）；以该接口行内 `required` 说明为准。
- 表格中的 `interface_name` 使用短名（不带 `xxx/` 前缀），仅作可读别名；`action_key` 作为唯一定位键。
- 一致性自检：
  - `path` 含 `?key=<param>` 或 `[&key=<param>]` 时，query 键名 `key` 必须与模板字面量一致（含大小写）；`<param>` 是参数名。
  - `*_query_params` 列记录的是参数名（占位符名），不是 query 键名。示例：`streamKey=<stream_key>` 中参数名是 `stream_key`。
  - `domain` 含 `<k>` 时，`k` 必须出现在 `required_host_params`，不能出现在 `required_params`。
  - `path` 含 `/<id>` 占位符时，`id` 必须出现在 `required_path_params`，不能出现在 `required_params`。
  - `GET`/`DELETE` 接口默认 body 为空；若无文档明确要求 body，`required_params` 应为 `-`。
  - 同名参数仅在接口模板显式要求时允许跨位置重复（例如既出现在 path 又出现在 query）。
  - query 键名必须与模板字面量完全一致（区分大小写），例如 `streamKey` 不能改写为 `stream_key`。

### 参数归位必跑流程（最高优先级）

1. 从接口行读取 5 组参数：`body`、`query`、`host`、`path`、`extra(optional)`。
2. 先替换 Host 占位符（`required_host_params`），再替换 path 占位符（`required_path_params`）。
3. 仅把 `required_query_params`/`optional_query_params` 放入 URL query。
4. 仅把 `required_params`/`optional_params` 放入 JSON body。
5. 任一参数放错位置时立即报错 `PARAM_POSITION_MISMATCH`，禁止“自动挪位补救”后继续请求。
6. 若输入参数出现未在四类参数（body/query/host/path）声明的字段，立即报错 `UNDECLARED_PARAM`。
7. 同名参数要求跨位置一致（如同一接口同时在 query/path/host 使用 `stream_key`）；值不一致时报错 `PARAM_VALUE_CONFLICT`。
8. 报错时返回位置化缺失信息，例如：`missing_required=["query.begin","path.task_id"]`。

### 参数位置示例（错误/正确）

| action | 错误写法 | 正确写法 |
| --- | --- | --- |
| `statistics/query_downflow_stat` | 把 `begin` 放到 body：`{"begin":"..."}` | 把 `begin` 放到 query：`...?begin=...`，body 为空 |
| `pub-relay/query_pub_task` | 把 `task_id` 放到 query：`/tasks?task_id=123` | 把 `task_id` 放到 path：`/tasks/123`，body 为空 |
| `domain-management/get_downstream_domain_config` | 把 `domain` 放到 body | 把 `domain` 放到 query：`...?domainConfig&name=<domain>` |

### 接口索引（快速匹配 action_key）

| module | action_key 前缀 | interface_name 列表 |
| --- | --- | --- |
| `bucket-management` | `bucket-management/` | `create_bucket`、`delete_bucket`、`get_bucket_config`、`list_buckets`、`update_bucket_config` |
| `certificate-management` | `certificate-management/` | `delete_domain_certificate`、`list_domain_certificates`、`update_certificate`、`upload_domain_certificate` |
| `domain-management` | `domain-management/` | `bind_downstream_domain`、`bind_upstream_domain`、`get_downstream_domain_config`、`get_upstream_domain_config`、`list_downstream_domains`、`list_upstream_domains`、`unbind_downstream_domain`、`unbind_upstream_domain`、`update_downstream_domain_config`、`update_upstream_domain_config` |
| `live-stream-transcoding-template` | `live-stream-transcoding-template/` | `add_transcoding_template`、`delete_transcoding_template`、`get_template_info`、`get_template_list`、`update_transcoding_template` |
| `pub-relay` | `pub-relay/` | `create_pub_task`、`delete_pub_task`、`edit_pub_task`、`get_pub_list`、`query_pub_task`、`query_task_history`、`query_task_log`、`start_pub_task`、`stop_pub_task` |
| `recording-management` | `recording-management/` | `create_recording`、`snapshot` |
| `statistics` | `statistics/` | `query_downflow_stat`、`query_offline_log`、`query_split_offline_log`、`query_stream_history`、`query_upflow_stat` |
| `stream-management` | `stream-management/` | `ban_stream`、`create_stream`、`delete_stream`、`get_stream_info`、`get_stream_list`、`unban_stream` |
| `utilities` | `utilities/` | `create_apikey`、`delete_apikey`、`query_apikey_list`、`rename_apikey`、`query_play_domain`、`query_publish_domain` |

### bucket-management
| interface_name | action_key | function_name | method | domain | path | required_params | optional_params | required_query_params | optional_query_params | required_host_params | required_path_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `create_bucket` | `bucket-management/create_bucket` | `call_bucket_management_create_bucket` | `PUT` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/` | `-` | `-` | `-` | `-` | `bucket_name` | `-` |
| `delete_bucket` | `bucket-management/delete_bucket` | `call_bucket_management_delete_bucket` | `DELETE` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/` | `-` | `-` | `-` | `-` | `bucket_name` | `-` |
| `get_bucket_config` | `bucket-management/get_bucket_config` | `call_bucket_management_get_bucket_config` | `GET` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?config` | `-` | `-` | `-` | `with_config` | `bucket_name` | `-` |
| `list_buckets` | `bucket-management/list_buckets` | `call_bucket_management_list_buckets` | `GET` | `mls.cn-east-1.qiniumiku.com` | `/` | `-` | `-` | `-` | `-` | `-` | `-` |
| `update_bucket_config` | `bucket-management/update_bucket_config` | `call_bucket_management_update_bucket_config` | `PATCH` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?config` | `config_data` | `-` | `-` | `-` | `bucket_name` | `-` |

### certificate-management
| interface_name | action_key | function_name | method | domain | path | required_params | optional_params | required_query_params | optional_query_params | required_host_params | required_path_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `delete_domain_certificate` | `certificate-management/delete_domain_certificate` | `call_certificate_management_delete_domain_certificate` | `DELETE` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?domainCertificate&domain=<domain>&certName=<cert_name>` | `-` | `-` | `domain`、`cert_name` | `-` | `bucket_name` | `-` |
| `list_domain_certificates` | `certificate-management/list_domain_certificates` | `call_certificate_management_list_domain_certificates` | `GET` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?domainCertificate&domain=<domain>` | `-` | `-` | `domain` | `-` | `bucket_name` | `-` |
| `update_certificate` | `certificate-management/update_certificate` | `call_certificate_management_update_certificate` | `PATCH` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?domainCertificate&domain=<domain>&certName=<cert_name>` | `update_data` | `-` | `domain`、`cert_name` | `-` | `bucket_name` | `-` |
| `upload_domain_certificate` | `certificate-management/upload_domain_certificate` | `call_certificate_management_upload_domain_certificate` | `POST` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?domainCertificate` | `certificate_data` | `-` | `-` | `-` | `bucket_name` | `-` |

### domain-management
| interface_name | action_key | function_name | method | domain | path | required_params | optional_params | required_query_params | optional_query_params | required_host_params | required_path_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `bind_downstream_domain` | `domain-management/bind_downstream_domain` | `call_domain_management_bind_downstream_domain` | `POST` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?domain` | `domain` | `domain_type` | `-` | `-` | `bucket_name` | `-` |
| `bind_upstream_domain` | `domain-management/bind_upstream_domain` | `call_domain_management_bind_upstream_domain` | `POST` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?pushDomain` | `domain`、`domain_type` | `-` | `-` | `-` | `bucket_name` | `-` |
| `get_downstream_domain_config` | `domain-management/get_downstream_domain_config` | `call_domain_management_get_downstream_domain_config` | `GET` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?domainConfig&name=<domain>` | `-` | `-` | `domain` | `-` | `bucket_name` | `-` |
| `get_upstream_domain_config` | `domain-management/get_upstream_domain_config` | `call_domain_management_get_upstream_domain_config` | `GET` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?pushDomainConfig&name=<domain>` | `-` | `-` | `domain` | `-` | `bucket_name` | `-` |
| `list_downstream_domains` | `domain-management/list_downstream_domains` | `call_domain_management_list_downstream_domains` | `GET` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?domain` | `-` | `-` | `-` | `-` | `bucket_name` | `-` |
| `list_upstream_domains` | `domain-management/list_upstream_domains` | `call_domain_management_list_upstream_domains` | `GET` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?pushDomain` | `-` | `-` | `-` | `-` | `bucket_name` | `-` |
| `unbind_downstream_domain` | `domain-management/unbind_downstream_domain` | `call_domain_management_unbind_downstream_domain` | `DELETE` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?domain&name=<domain>` | `-` | `-` | `domain` | `-` | `bucket_name` | `-` |
| `unbind_upstream_domain` | `domain-management/unbind_upstream_domain` | `call_domain_management_unbind_upstream_domain` | `DELETE` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?pushDomain&name=<domain>` | `-` | `-` | `domain` | `-` | `bucket_name` | `-` |
| `update_downstream_domain_config` | `domain-management/update_downstream_domain_config` | `call_domain_management_update_downstream_domain_config` | `PATCH` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?domainConfig&name=<domain>[&fields=<fields>]` | `config_data` | `-` | `domain` | `fields` | `bucket_name` | `-` |
| `update_upstream_domain_config` | `domain-management/update_upstream_domain_config` | `call_domain_management_update_upstream_domain_config` | `PATCH` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/?pushDomainConfig&name=<domain>[&fields=<fields>]` | `config_data` | `-` | `domain` | `fields` | `bucket_name` | `-` |

### live-stream-transcoding-template
| interface_name | action_key | function_name | method | domain | path | required_params | optional_params | required_query_params | optional_query_params | required_host_params | required_path_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `add_transcoding_template` | `live-stream-transcoding-template/add_transcoding_template` | `call_live_stream_transcoding_template_add_transcoding_template` | `POST` | `mls.cn-east-1.qiniumiku.com` | `/?codecTemplate` | `template_body` | `host` | `-` | `-` | `-` | `-` |
| `delete_transcoding_template` | `live-stream-transcoding-template/delete_transcoding_template` | `call_live_stream_transcoding_template_delete_transcoding_template` | `DELETE` | `mls.cn-east-1.qiniumiku.com` | `/?codecTemplate&name=<name>` | `-` | `host` | `name` | `-` | `-` | `-` |
| `get_template_info` | `live-stream-transcoding-template/get_template_info` | `call_live_stream_transcoding_template_get_template_info` | `GET` | `mls.cn-east-1.qiniumiku.com` | `/?codecTemplate&name=<name>` | `-` | `host` | `name` | `-` | `-` | `-` |
| `get_template_list` | `live-stream-transcoding-template/get_template_list` | `call_live_stream_transcoding_template_get_template_list` | `GET` | `mls.cn-east-1.qiniumiku.com` | `/?codecTemplates[&content=<content>&limit=<limit>&offset=<offset>]` | `-` | `host` | `-` | `content`、`limit`、`offset` | `-` | `-` |
| `update_transcoding_template` | `live-stream-transcoding-template/update_transcoding_template` | `call_live_stream_transcoding_template_update_transcoding_template` | `PATCH` | `mls.cn-east-1.qiniumiku.com` | `/?codecTemplate` | `template_body` | `host` | `-` | `-` | `-` | `-` |

### pub-relay
| interface_name | action_key | function_name | method | domain | path | required_params | optional_params | required_query_params | optional_query_params | required_host_params | required_path_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `create_pub_task` | `pub-relay/create_pub_task` | `call_pub_relay_create_pub_task` | `POST` | `pub-manager.mikudns.com` | `/tasks` | `task_body` | `-` | `-` | `-` | `-` | `-` |
| `delete_pub_task` | `pub-relay/delete_pub_task` | `call_pub_relay_delete_pub_task` | `DELETE` | `pub-manager.mikudns.com` | `/tasks/<task_id>` | `-` | `-` | `-` | `-` | `-` | `task_id` |
| `edit_pub_task` | `pub-relay/edit_pub_task` | `call_pub_relay_edit_pub_task` | `POST` | `pub-manager.mikudns.com` | `/tasks/<task_id>` | `task_body` | `-` | `-` | `-` | `-` | `task_id` |
| `get_pub_list` | `pub-relay/get_pub_list` | `call_pub_relay_get_pub_list` | `GET` | `pub-manager.mikudns.com` | `/tasks[?marker=<marker>&limit=<limit>&name=<name>]` | `-` | `-` | `-` | `marker`、`limit`、`name` | `-` | `-` |
| `query_pub_task` | `pub-relay/query_pub_task` | `call_pub_relay_query_pub_task` | `GET` | `pub-manager.mikudns.com` | `/tasks/<task_id>` | `-` | `-` | `-` | `-` | `-` | `task_id` |
| `query_task_history` | `pub-relay/query_task_history` | `call_pub_relay_query_task_history` | `GET` | `pub-manager.mikudns.com` | `/history[?marker=<marker>&limit=<limit>&name=<name>&start=<start>&end=<end>]` | `-` | `-` | `-` | `marker`、`limit`、`name`、`start`、`end` | `-` | `-` |
| `query_task_log` | `pub-relay/query_task_log` | `call_pub_relay_query_task_log` | `GET` | `pub-manager.mikudns.com` | `/tasks/<task_id>/runinfo` | `-` | `-` | `-` | `-` | `-` | `task_id` |
| `start_pub_task` | `pub-relay/start_pub_task` | `call_pub_relay_start_pub_task` | `POST` | `pub-manager.mikudns.com` | `/tasks/<task_id>/start` | `-` | `-` | `-` | `-` | `-` | `task_id` |
| `stop_pub_task` | `pub-relay/stop_pub_task` | `call_pub_relay_stop_pub_task` | `POST` | `pub-manager.mikudns.com` | `/tasks/<task_id>/stop` | `-` | `-` | `-` | `-` | `-` | `task_id` |

### recording-management
| interface_name | action_key | function_name | method | domain | path | required_params | optional_params | required_query_params | optional_query_params | required_host_params | required_path_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `create_recording` | `recording-management/create_recording` | `call_recording_management_create_recording` | `POST` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/<stream_name>?recordingFile` | `start_time`、`end_time` | `fmt`、`fname`、`pipeline`、`expire_days`、`first_segment_type`、`persistent_delete_after_days`、`notify`、`host`、`timeout` | `-` | `-` | `bucket_name` | `stream_name` |
| `snapshot` | `recording-management/snapshot` | `call_recording_management_snapshot` | `POST` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/<stream_name>?snapshot` | `-` | `time`、`fname`、`img_format`、`pipeline`、`notify`、`delete_after_days` | `-` | `-` | `bucket_name` | `stream_name` |

### statistics
| interface_name | action_key | function_name | method | domain | path | required_params | optional_params | required_query_params | optional_query_params | required_host_params | required_path_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `query_downflow_stat` | `statistics/query_downflow_stat` | `call_statistics_query_downflow_stat` | `GET` | `miku-statd.qiniuapi.com` | `/statd/v1/traffic/stat/downflow` | `-` | `-` | `begin` | `end`、`granularity`、`group`、`hub`、`domain`、`stream_name`、`area`、`select` | `-` | `-` |
| `query_offline_log` | `statistics/query_offline_log` | `call_statistics_query_offline_log` | `GET` | `miku-statd.qiniuapi.com` | `/statd/v1/livelog` | `-` | `-` | `domain`、`start`、`end` | `-` | `-` | `-` |
| `query_split_offline_log` | `statistics/query_split_offline_log` | `call_statistics_query_split_offline_log` | `GET` | `miku-statd.qiniuapi.com` | `/statd/v1/livelog/split` | `-` | `-` | `domain`、`start`、`end` | `-` | `-` | `-` |
| `query_stream_history` | `statistics/query_stream_history` | `call_statistics_query_stream_history` | `GET` | `mls.cn-east-1.qiniumiku.com` | `/?streamStats&start=<start>&end=<end>&stream=<stream>[&domain=<domain> 或 &bucket=<bucket>][&g=<granularity>]` | `-` | `-` | `start`、`end`、`stream`、`domain` 或 `bucket`（至少一项） | `granularity` | `-` | `-` |
| `query_upflow_stat` | `statistics/query_upflow_stat` | `call_statistics_query_upflow_stat` | `GET` | `miku-statd.qiniuapi.com` | `/statd/v1/traffic/stat/upflow` | `-` | `-` | `begin` | `end`、`granularity`、`group`、`hub`、`domain`、`stream_name`、`area`、`select` | `-` | `-` |

### stream-management
| interface_name | action_key | function_name | method | domain | path | required_params | optional_params | required_query_params | optional_query_params | required_host_params | required_path_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ban_stream` | `stream-management/ban_stream` | `call_stream_management_ban_stream` | `POST` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/<stream_key>?forbid&bucket=<bucket_name>&streamKey=<stream_key>` | `-` | `forbidden_till` | `bucket_name`、`stream_key` | `-` | `bucket_name` | `stream_key` |
| `create_stream` | `stream-management/create_stream` | `call_stream_management_create_stream` | `PUT` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/<stream_key>`（即 `/<stream_name>`） | `-` | `-` | `-` | `-` | `bucket_name` | `stream_key` |
| `delete_stream` | `stream-management/delete_stream` | `call_stream_management_delete_stream` | `DELETE` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/<stream_key>` | `-` | `-` | `-` | `-` | `bucket_name` | `stream_key` |
| `get_stream_info` | `stream-management/get_stream_info` | `call_stream_management_get_stream_info` | `GET` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/<stream_key>?info=` | `-` | `-` | `-` | `-` | `bucket_name` | `stream_key` |
| `get_stream_list` | `stream-management/get_stream_list` | `call_stream_management_get_stream_list` | `GET` | `mls.cn-east-1.qiniumiku.com` | `/?streamlist[&prefix=<prefix>&offset=<offset>&limit=<limit>&domain=<domain>&start=<start>&end=<end>&bucketId=<bucketId>&isForbid=<isForbid>]` | `-` | `-` | `domain` 或 `bucketId`（至少一项） | `prefix`、`offset`、`limit`、`start`、`end`、`isForbid` | `-` | `-` |
| `unban_stream` | `stream-management/unban_stream` | `call_stream_management_unban_stream` | `POST` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/<stream_key>?release` | `-` | `-` | `-` | `-` | `bucket_name` | `stream_key` |

### utilities
| interface_name | action_key | function_name | method | domain | path | required_params | optional_params | required_query_params | optional_query_params | required_host_params | required_path_params |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `create_apikey` | `utilities/create_apikey` | `call_utilities_create_apikey` | `POST` | `mls.cn-east-1.qiniumiku.com` | `/?apikey` | `name` | `-` | `-` | `-` | `-` | `-` |
| `delete_apikey` | `utilities/delete_apikey` | `call_utilities_delete_apikey` | `DELETE` | `mls.cn-east-1.qiniumiku.com` | `/?apikey` | `apikey_id` | `-` | `-` | `-` | `-` | `-` |
| `query_apikey_list` | `utilities/query_apikey_list` | `call_utilities_query_apikey_list` | `GET` | `mls.cn-east-1.qiniumiku.com` | `/?apikeys` | `-` | `-` | `-` | `-` | `-` | `-` |
| `rename_apikey` | `utilities/rename_apikey` | `call_utilities_rename_apikey` | `POST` | `mls.cn-east-1.qiniumiku.com` | `/?apikeyRename` | `apikey_id`、`new_name` | `-` | `-` | `-` | `-` | `-` |
| `query_play_domain` | `utilities/query_play_domain` | `call_utilities_query_play_domain` | `POST` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/<stream_key>?playUrl` | `domain` | `expire_time` | `-` | `-` | `bucket_name` | `stream_key` |
| `query_publish_domain` | `utilities/query_publish_domain` | `call_utilities_query_publish_domain` | `POST` | `<bucket_name>.mls.cn-east-1.qiniumiku.com` | `/<stream_key>?publishUrl` | `domain` | `expire_time` | `-` | `-` | `bucket_name` | `stream_key` |

## 请求示例（JSON）

```json
{
  "intent": "获取空间列表",
  "params_json": {},
  "topk": 5,
  "dry_run": false
}
```

```json
{
  "action": "domain-management/bind_downstream_domain",
  "params_json": {
    "bucket_name": "example-bucket",
    "domain": "live.example.com"
  }
}
```

## 凭证与安全

- 使用 `Access_key`、`Secret_key` 作为鉴权凭证。
- 若未在请求中显式传入 `ak/sk`，运行环境必须存在 `Access_key` 和 `Secret_key` 两个环境变量。
- 缺少 AK/SK 时，不执行真实调用。
- 不输出完整私钥、证书、Token 或敏感 header。
- 用户未明确批量执行时，一次仅执行一个 action。
- 删除/解绑/停止类操作仅在意图明确时执行；不明确时先确认目标资源。
