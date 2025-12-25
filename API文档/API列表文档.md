本文为您介绍了七牛云直播服务的所有API列表，建议您使用服务端 SDK 进行调用

## 空间管理

| 接口名称 | 描述 |
|:--------|:-----|
| [创建空间](/mikustream/api/13094/mikustream-live-bucket-create-api) | 创建一个新的空间（Bucket） |
| [删除空间](/mikustream/api/13095/mikustream-live-bucket-delete-api) | 删除指定的空间（Bucket） |
| [列举空间](/mikustream/api/13093/mikustream-live-bucket-list-api) | 获取当前账号下所有空间（Bucket）的列表信息 |
| [修改空间配置](/mikustream/api/13096/mikustream-live-bucket-config-update-api) | 修改指定空间（Bucket）的配置 |
| [获取空间配置](/mikustream/api/13097/mikustream-live-bucket-config-api) | 获取指定直播空间（Bucket）的配置信息 |


## 域名管理

| 接口名称 | 描述 |
|:--------|:-----|
| [绑定上行域名](/mikustream/api/13177/mikustream-live-bind-upstream-domain-api) | 为指定直播空间绑定上行域名（推流域名） |
| [解绑上行域名](/mikustream/api/13178/mikustream-live-unbind-upstream-domain-api) | 为指定直播空间解绑上行域名（推流域名） |
| [列举上行域名](/mikustream/api/13179/mikustream-live-list-upstream-domain-api) | 列举指定直播空间的所有上行域名（推流域名） |
| [修改上行域名配置](/mikustream/api/13181/mikustream-live-update-upstream-domain-config-api) | 修改指定直播空间中某个上行域名的配置 |
| [获取上行域名配置](/mikustream/api/13180/mikustream-live-get-upstream-domain-config-api) | 获取指定直播空间中某个上行域名的详细配置信息 |
| [绑定下行域名](/mikustream/api/13182/mikustream-live-bind-downstream-domain-api) | 为指定直播空间绑定下行域名（播放域名） |
| [解绑下行域名](/mikustream/api/13183/mikustream-live-unbind-downstream-domain-api) | 为指定直播空间解绑下行域名（播放域名） |
| [列举下行域名](/mikustream/api/13184/mikustream-live-list-downstream-domain-api) | 列举指定直播空间的所有下行域名（播放域名） |
| [修改下行域名配置](/mikustream/api/13186/mikustream-live-update-downstream-domain-config-api) | 修改指定直播空间中某个下行域名的配置 |
| [获取下行域名配置](/mikustream/api/13185/mikustream-live-get-downstream-domain-config-api) | 获取指定直播空间中某个下行域名的详细配置信息 |

## 证书管理

| 接口名称 | 描述 |
|:--------|:-----|
| [上传域名证书](/mikustream/13204/mikustream-live-certificate-upload-api) | 为直播服务上传域名 SSL 证书） |
| [删除域名证书](/mikustream/13205/mikustream-live-certificate-delete-api) | 删除指定域名 SSL 证书 |
| [列举域名证书](/mikustream/13207/mikustream-live-certificate-list-api) | 列举所有已上传的域名 SSL 证书 |
| [更新证书](/mikustream/13206/mikustream-live-certificate-update-api) | 更新指定域名 SSL 证书内容 |

## 直播流管理

| 接口名称 | 描述 |
|:--------|:-----|
| [创建流](/mikustream/13218/mikustream-live-stream-create-api) | 在指定直播空间中创建一个新的直播流 |
| [获取流信息](/mikustream/13220/mikustream-live-stream-query-api) | 获取指定直播流的详细信息 |
| [删除流](/mikustream/13219/mikustream-live-stream-delete-api) | 删除指定的直播流 |
| [封禁流](/mikustream/13219/mikustream-live-stream-ban-api) | 封禁指定的直播流，禁止其推流和播放 |
| [解封流](/mikustream/13221/mikustream-live-stream-permit-api) | 解封指定的直播流，恢复其推流和播放功能 |
| [列举流列表](/mikustream/13222/mikustream-live-stream-query-list-api) | 列举指定直播空间中的活跃流信息 |

## Pub转推

| 接口名称 | 描述 |
|:--------|:-----|
| [创建任务](/mikustream/13226/mikustream-live-pub-create-api) | 在服务端创建一个 pub 转推任务 |
| [编辑任务](/mikustream/13225/mikustream-live-pub-edit-api) | 在服务端编辑一个 pub 转推任务 |
| [开始任务](/mikustream/13227/mikustream-live-pub-start-api) | 开始（启动）指定的 pub 转推任务 |
| [停止任务](/mikustream/13233/mikustream-live-pub-stop-api) | 停止（终止）指定的 pub 转推任务 |
| [删除任务](/mikustream/13232/mikustream-live-pub-delete-api) | 删除指定的 pub 转推任务 |
| [任务详情](/mikustream/13230/mikustream-live-pub-info-api) | 查询指定 pub 转推任务的详细信息 |
| [任务列表](/mikustream/13229/mikustream-live-pub-list-api) | 列举 pub 转推任务列表 |
| [任务运行日志](/mikustream/13231/mikustream-live-pub-log-api) | 查询指定 pub 转推任务的运行日志 |
| [任务历史记录](/mikustream/13228/mikustream-live-pub-history-api) | 查询 pub 转推任务的历史运行记录 |

