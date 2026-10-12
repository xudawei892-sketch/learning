# 来源与核验范围

## 原文

所有论文的主来源与 PDF 地址记录在上一层 `manifest.json` 中。初次 arXiv 请求被网络代理以 `403 Forbidden` 拒绝；保存所需域名后重试成功。现在 **32 篇原始 PDF 均已取得，标题和摘要/首页已核对**：31 篇来自 arXiv，ALOHA Unleashed 来自作者项目。单篇目录保留 PDF 第 1–2 页的文本摘录。中文导读仍不是逐页精读；具体方法细节与全部实验需要继续读全文。

## 本轮实际取得的官方项目文档

|本地快照|来源仓库|与收录论文的关系|
|---|---|---|
|[openvla-README.md](openvla-README.md)|[openvla/openvla](https://github.com/openvla/openvla)|OpenVLA 编号、微调及 LIBERO 信息；也记录 FAST/OFT 的后续更新|
|[openpi-README.md](openpi-README.md)|[Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi)|π0、π0-FAST、π0.5 模型类别与使用入口|
|[octo-README.md](octo-README.md)|[octo-models/octo](https://github.com/octo-models/octo)|模块化通用策略、扩散动作头、条件输入|
|[diffusion_policy-README.md](diffusion_policy-README.md)|[real-stanford/diffusion_policy](https://github.com/real-stanford/diffusion_policy)|Diffusion Policy 官方实现入口|
|[act-README.md](act-README.md)|[tonyzhaozh/act](https://github.com/tonyzhaozh/act)|ACT、两种模拟任务与源码入口|
|[libero-README.md](libero-README.md)|[Lifelong-Robot-Learning/LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)|LIBERO 原文编号与项目入口|
|[simpler-README.md](simpler-README.md)|[simpler-env/SimplerEnv](https://github.com/simpler-env/SimplerEnv)|仿真评测资源入口|
|[openvla_oft-README.md](openvla_oft-README.md)|[moojink/openvla-oft](https://github.com/moojink/openvla-oft)|OFT 标题、编号、连续预测示例、项目资源需求|
|[spatialvla-README.md](spatialvla-README.md)|[SpatialVLA/SpatialVLA](https://github.com/SpatialVLA/SpatialVLA)|SpatialVLA 标题、编号与空间表示路线|
|[rdt-README.md](rdt-README.md)|[thu-ml/RoboticsDiffusionTransformer](https://github.com/thu-ml/RoboticsDiffusionTransformer)|RDT-1B 标题、编号、数据与动作接口说明|
|[groot-README.md](groot-README.md)|[NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)|N1 论文标题与编号；仓库当前文档已更新到后续版本|
|[smolvla-README.md](smolvla-README.md)|[huggingface/lerobot](https://github.com/huggingface/lerobot)|LeRobot 及 SmolVLA 的项目入口；不是 SmolVLA 论文全文|

快照从上述仓库 `main` 分支的官方 raw GitHub 路径取得，访问成功。访问日期为本轮 2026-10-12。原文件保留原貌，里面的相对链接和图片应在对应上游仓库查看；本包没有复制其完整目录、代码、许可证文件或模型权重。文档遵循上游许可，本地快照仅供来源核对。

这些文档并没有固定到论文发布时的 commit，**不能据当前 README 声称原始论文已经包含后续所有功能**。尤其 GR00T、openpi 和 LeRobot 的当前版本与早期论文之间有差异。快照内容 SHA-256 记录在 `source_manifest.json`；哈希只能定位本次保存的内容，不能替代 Git commit 或全文证据。

## 原文核验与后续精读

本轮逐篇比对标题和摘要/首页，并从 PDF 提取实际版本标识与页数。ALOHA Unleashed 初始编号不匹配，已经纠正为作者官网链接的官方 PDF；错误文件已移除，没有纳入最终资料包。作者项目来源是 `aloha-unleashed/aloha-unleashed.github.io` 的 `assets/aloha_unleashed.pdf`，对应网页快照保留在本目录。

仍待逐项精读确认：作者完整列表、正式会议版本、精确实验数字、图号和公式细节。本轮不编造作者列表、不输出未核验性能排名，也不声称已取得抖音视频或其评论区资源。
