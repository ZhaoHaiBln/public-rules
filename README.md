# public-rules · Stash / 塔台

面向塔台生成 Stash 配置的精简方案。通用分流采用 ACL4SSR，Google、国内及独立流媒体采用 blackmatrix7 的成熟规则来源。

导入地址仍为：

https://raw.githubusercontent.com/ZhaoHaiBln/public-rules/main/custom_full.ini

## 使用

1. 在塔台重新导入上述方案地址，再选择 Stash 生成配置。更新 GitHub 文件不会自动改写已经生成的旧配置；更换方案后需要重新生成。
2. 建议新建一份 Stash 配置进行验证，保留旧配置便于切回；各端使用同一份方案，节点订阅仍在塔台管理。
3. 先选择一个已知可用的节点，在“🌐 Google服务”中选择它。Google 搜索、账号、Play / Pay / Wallet 与 YouTube 共用该组的实际出口；“Google Play”“YouTube”是只有一个成员的入口，不再各自选不同节点。
4. 依次检查 Google 搜索、YouTube 首页和播放、Play 下载、Telegram、AI，以及京东、一号店、红果。确认正常后再考虑启用广告拦截。

不要把订阅地址、节点密码、UUID、密钥或付款资料提交到这个公开仓库。

## 分组与偏好

| 服务 | 默认首选 |
| --- | --- |
| Google / Play / Pay / Wallet / YouTube | Google服务 → 美国 IEPL |
| AI、PrimeVideo、Max、PayPal | 美国 IEPL |
| Telegram、Emby | 香港 IEPL |
| 国外信息、Netflix、Disney+ | 新加坡 IEPL |
| 国内直连、国内漏网 | DIRECT |
| 广告拦截 | DIRECT（关闭拦截）；可手动改为 REJECT |
| 国外漏网 | 国外信息 |

IEPL 地区组只匹配含 IEPL 标记的节点；只有“专线”或 IPLC 标记的节点不进入 IEPL 组。地区名和 IEPL 标记可按任意顺序出现。

地区自动组与手动节点池都带 REJECT 作为空池的保护策略，避免无匹配节点时被塔台 1.0.21 默认为 DIRECT。REJECT 不是额外的代理节点。某地区没有节点时，应选择存在节点的地区或手动选择；方案不会凭空创建节点。

## 规则来源与顺序

1. 明确私网网段与 `.lan` / `.local`，不把 `198.18.0.0/16` Fake IP 地址池作为直连规则。
2. 京东 / 一号店的成熟集合，及少量番茄 / 短剧业务补充。
3. ACL4SSR AI 集合，外加精确 Gemini API 等业务域名；不使用 `apis.google.com` 后缀作为 Gemini 专用规则。
4. Telegram、PayPal、Netflix、Disney+、PrimeVideo、Max、Emby 专用集合。
5. YouTube 核心与 Play 接口，再到 Google 共用 API / CDN 和 Google 完整集合。它们共用一个实际出口。
6. `.cn` 和 China 国内综合集合。
7. 可选 BanAD、ProxyGFWlist、中国 IP 和国外代理兜底。

共有 13 个远程规则源，全部来自下面两个公开项目，不再引用本仓库旧版自建列表。上游集合仍包含各自的关键词、IP 或进程规则；本方案没有宣称所有上游规则都不存在宽泛匹配。进程规则在部分 Stash 平台上可能被忽略，主要分流不依赖进程名。

- [ACL4SSR](https://github.com/ACL4SSR/ACL4SSR)：通用国外、AI 与可选广告集合，CC BY-SA 4.0。
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)：Google、China、京东、Telegram、PayPal、流媒体集合，遵循上游许可与使用声明。
- Google 共用下载接口 / CDN 补充参考 [Android Enterprise 网络要求](https://support.google.com/work/android/answer/10513641?hl=en)。
- 番茄 / 短剧补充来源 [ByteDance 列表](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/ByteDance/ByteDance.list)。这不是完整的红果连接清单，是否覆盖当前 App 仍需实测。

没有整份导入国内公司的海外云 IP、宽泛下载匹配、国际版国内媒体列表，也不继续维护旧版的大型自建 AI / 国内 / 国外 / 媒体 / 广告集合。

## DNS 与塔台 1.0.21

方案末尾的 `[General]` 段提供 IPv6 和 DNS 参数。已核对塔台官方 `v1.0.21` 源码：该版本会读取 `ipv6`、`dns-server`、`encrypted-dns-server`、`proxy-test-url` 并映射到生成配置。

- 本方案默认关闭 IPv6，提供两个国内基础 DNS 与两个国内 DoH。
- 目的是使节点域名解析和国内直连的基础解析可用，并避免原默认配置中的国外 DoH 直连依赖；代理流量的域名处理由 Stash / 塔台生成模式负责。
- 塔台中的全局网络设置可能覆盖方案值。生成后应检查 `ipv6: false`、`dns.nameserver` 和 `dns.proxy-server-nameserver` 是否与方案对应。
- 不强制启用 DNS follow-rule，不自行添加全局 QUIC 拦截，不嵌入节点凭据。

官方 subconverter 能验证规则和策略组，但不会应用这里的 `[General]` 网络段。此方案的使用入口是塔台，不是将普通 subconverter 输出直接视为最终 Stash 文件。

## 检查与验证边界

运行 `python check_config.py` 可离线检查结构、引用、环路、共享 Google 出口、空节点保护和兜底位置；加 `--online` 可读取公开规则源检查 URL / 内容。

本轮重建验证：

- 13 个实际使用的公开规则 URL 返回正常。
- 官方 subconverter v0.9.0，虚拟节点与规则快照：57 个域名检查、4 种节点场景通过；24 个分组、14,096 条生成规则。
- 官方 Mihomo v1.19.32 实际加载完整测试配置通过，包括规则、策略组和已映射的 DNS。
- 塔台 `v1.0.21` 的 INI / 网络参数与空组行为已做源码核对。

这些不等于实际执行塔台 App 或在 Stash Android 1.1.5、iOS、macOS 等设备上成功联网。节点质量、账号地区、运营商网络、DNS 模式和应用缓存仍会影响结果；本仓库不承诺“全端已实测”。

## 仓库清理与回退

当前入口保留 `custom_full.ini`。旧版 `ai.list`、`domestic.list`、`foreign.list`、`media.list`、`reject.list` 从当前版本移除；旧内容仍在 Git 历史中。外部若直接订阅这些旧 `.list` URL，需要改为新方案入口；旧 URL 删除后不会继续提供规则。

重建前最后版本为 `924cec452f08e572272e2ebd3ca42b113c1a5e9c`。如需回退，优先 revert 重建提交，并在塔台重新生成旧方案，而不是强制推送覆盖后续改动。
