# 学完之后的最小仿真路线

此目录目前是规划，**没有安装环境、下载权重、训练模型或运行仿真**。本轮只完成阅读前的资料准备。

## 推荐次序

1. 先跑一个仿真环境自带示例，理解 observation、action、reset、step、终止和成功判据。不要立即下载多个大型模型。
2. 如果动作学习本身还不清楚，先做 ACT 的 Transfer Cube 或一个已有 BC 基线，观察动作块与闭环执行。
3. 想进入 VLA，优先考虑 **LIBERO + OpenVLA/OpenVLA-OFT 的官方预训练评测流程**；先复现一个套件的少量回合，再扩大到正式评测。
4. 明确基础流程后再考虑 openpi 的 LIBERO 示例。不同路线单独环境管理，按官方版本锁定依赖。

## 开始前必须确定的事项

|项目|需要确认|
|---|---|
|目标|纯推理评测还是微调？先选一个，不同时开展多个模型|
|资源|GPU 型号、可用显存、驱动、磁盘、权重下载权限|
|版本|代码 commit、环境版本、数据版本、模型权重与动作归一化键|
|接口|相机数量、图像尺寸、本体状态、动作坐标系和控制频率|
|评测|任务、种子、每任务回合数、最大步数、成功判据|
|输出|成功率、逐任务统计、失败轨迹视频、环境与模型版本记录|

官方 OpenVLA-OFT README 在本轮访问时列出 LIBERO 推理约需 16 GB 显存、ALOHA 推理约需 18 GB；训练配置需求另有范围。**这是某项目文档的参考，不是所有 VLA 的通用显存门槛**。准备实际运行时要以对应 commit、精度、输入和设备测试为准。

## 第一轮实验应该输出什么

保留至少一段成功轨迹和一段失败轨迹（如果有失败），写清试了多少回合。单个成功视频只能证明存在成功案例；不能声称达到论文平均成功率。固定观察、种子和评测参数后，再改变动作块或执行步数研究行为差异。

代码入口：

- [ACT](https://github.com/tonyzhaozh/act)：`sim_env.py`、`policy.py`、`imitate_episodes.py`。
- [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)。
- [OpenVLA](https://github.com/openvla/openvla)：先读官方 README 的 LIBERO 与微调部分。
- [OpenVLA-OFT](https://github.com/moojink/openvla-oft)：先读 `SETUP.md` 与官方评测说明。
- [openpi](https://github.com/Physical-Intelligence/openpi)：先读 `examples/libero/README.md`，核对配置与权重版本。

此处没有给未经执行的安装指令盖上「已验证」标签，也没有克隆代码仓库。等你决定开始仿真时，再基于可用硬件完成真正的环境安装和验证。
