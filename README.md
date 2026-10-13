# public-rules · ACL4SSR Full / Stash / 塔台

以 ACL4SSR 官方 `ACL4SSR_Online_Full.ini` 的全部业务分类为基础，blackmatrix7 补充 Google、京东、PayPal、Disney+、PrimeVideo、Max、Emby。不是把两个仓库所有列表重复拼接，也不承诺“规则越多越快”。

方案地址：https://raw.githubusercontent.com/ZhaoHaiBln/public-rules/main/custom_full.ini 。在塔台更新方案后重新生成 Stash 配置。建议保留已知可用的原版 ACL4SSR 配置进行同节点对比。

## 与官方 Full 的区别

- 保留其微软 Bing、OneDrive、微软、苹果、游戏、网易音乐、哔哩哔哩、巴哈姆特、国内外媒体、国内域名与企业 IP、下载、GFW、GEOIP CN、代理兜底分类。
- Google 搜索、FCM、GoogleCN、Play、Pay、Wallet、YouTube 共用 Google服务 的实际节点，默认美国入口。GoogleCN 从官方的直连改为此组，避免下载域名被拆分。
- AI、PrimeVideo、Max、PayPal 默认美国入口；Telegram、Emby 默认香港入口；Netflix、Disney+、通用国外默认新加坡入口。
- 三个机场分别用节点名中的 `Flower_Trojan`、`liangxin`、`api-linkcube` 识别；不按 IEPL、专线、IPLC 或实际代理协议区分。请在塔台保留这些订阅名称后缀，名称改变会影响识别。
- 每个机场各设香港、新加坡、美国三个自动测速池，共九个。香港、新加坡、美国入口可选择该地区的三个机场池；机场默认顺序为 api-linkcube、Flower_Trojan、liangxin，客户端可切换。
- 其他地区混合三个机场且排除香港、新加坡、美国；手动选择可查看全部节点。没有相应节点的池为 REJECT，需要切换到有节点的机场池。
- 官方局域网源含 `198.18.0.0/16`；为了不把 Stash Fake IP 范围当直连网段，本版改用明确私网规则，没有照搬此集合。
- 保留少量已核对的番茄/短剧域名与 Gemini 端点适配。没有整段导入 ByteDance 或云服务商 ASN。
- BanAD/BanProgramAD 保留为注释，默认不加载；广告组默认 DIRECT。确认基础业务可用后，可取消相应 ruleset 行的注释并将组改为 REJECT。取消注释后规则会改变，须重新验证。
- 沿用此前核对的塔台 1.0.21 General DNS 设置；塔台界面全局设置可能覆盖它。不是原版 ACL4SSR 的 DNS，须以实际导出配置为准。

## 使用与对比

在塔台 1.0.21 导入本 INI 生成新的 Stash 配置，保留原版 ACL4SSR 对照。不要直接把 INI 当作 Stash YAML。更新方案后需重新生成。

两份配置使用相同节点、网络与测试业务，比较 Google 搜索、Play/Pay 下载、YouTube 播放、Telegram、AI、京东、一号店、红果。先在 Google服务 和其他服务组选择你已知可用的节点，避免地区筛选没有节点导致误判。速度应以设备实测为准。

不要公开提交真实订阅地址、节点密码、UUID 或密钥。验证使用虚拟节点，不连接用户代理。

## 维护

公开规则直接引用上游，随上游更新；依赖网络可访问 GitHub raw。规则顺序按首次命中执行，同一个域名可能存在于多个上游集合，业务分类放在通用集合前。未导入 blackmatrix7 全量 China/Global 叠加覆盖 ACL 基础。

运行 `python check_config.py` 检查格式、引用、空池和偏好；`--online` 可检查公开源可访问性。检查和转换通过不等于 Stash 真机联网通过；无实际塔台导出与设备实测时不作此保证。

来源：[ACL4SSR 官方完整模板](https://github.com/ACL4SSR/ACL4SSR/blob/master/Clash/config/ACL4SSR_Online_Full.ini)、[blackmatrix7 分流规则](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Clash)。保留上游署名，使用遵循各上游许可与声明。ACL4SSR README 标注 CC BY-SA 4.0；blackmatrix7 仓库 LICENSE 与各目录许可、特别声明均适用。
