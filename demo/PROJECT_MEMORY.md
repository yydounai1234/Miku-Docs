# Project Memory (miku-docs/demo)

## 项目定位
- 这是七牛 Miku 直播服务 API 的 Python 示例/调试脚本仓库，不是完整应用服务。
- 代码按业务模块拆目录，脚本命名以 `test_*.py` 为主。

## 规模
- Python 脚本总数：56
- 主要模式：每个脚本独立完成参数组装、签名、HTTP 请求、响应打印。

## 统一技术特征
- 语言：Python
- 依赖：标准库为主（`os` `hmac` `hashlib` `base64` `json` `urllib.parse` `http.client`）
- 鉴权：环境变量 `Access_key` / `Secret_key`
- 签名算法：HMAC-SHA1，Authorization 格式 `Qiniu <AK>:<sign>`
- 请求方式：大量直连 `http://*.mls.cn-east-1.qiniumiku.com`，部分模块使用 HTTPS。

## 模块目录
- `空间管理`：空间增删改查
- `流管理`：流创建/禁用/解禁/删除/查询
- `域名管理`：上下行域名绑定、解绑、配置
- `证书管理`：证书上传、更新、查询、删除
- `录制管理`：录制文件生成、录制历史、截图
- `直播混流`：创建/停止混流
- `直播流转码模版`：转码模板增删改查
- `数据统计`：上下行流量、离线日志、流历史
- `pub转推`：转推任务增删改查与启动停止、历史日志
- `实用工具`：推拉流域名查询、API Key 管理
- `HTTPDNS`：HTTPDNS 解析

## 关键域名
- `mls.cn-east-1.qiniumiku.com`
- `miku-statd.qiniuapi.com`
- `pub-manager.mikudns.com`

## 已识别问题（后续优先修复）
- `证书管理/test_upload_domain_certificate.py` 含大段证书/私钥明文示例（高风险）
- `流管理/test_delete_stream.py` 中函数命名与行为不一致（删除函数名仍为 create）
- `数据统计/test_query_downflow_stat.py` 中函数名疑似复制错误（downflow 文件里叫 upflow）
- `pub转推/test_create_pub_task.py` 的 `use_oversea` 参数未实际生效

## 使用建议
- 建议抽取公共模块（签名/请求/错误处理）减少重复代码
- 建议补充统一 README（运行方式、环境变量、模块索引）
- 建议用环境变量或本地私密文件替代任何明文敏感示例数据

