[English](README.md)

# Video Face Swap

## 1. 项目概述

本项目是一个基于 `roop` 开发的开源视频换脸工具。通过利用 **Cog** 进行容器化封装，实现了与 **Replicate** 云平台的无缝对接，让任何人都能够轻松部署和运行。项目集成了 `inswapper_128.onnx` 人脸替换模型和 `GFPGANv1.4.pth` 人脸增强模型，旨在为AI爱好者和研究人员提供一个简单易用的视频换脸解决方案。

**重要声明**: 本项目仅供学术研究和教育目的使用，严禁商业用途。所有使用者必须遵守“道德规范与许可协议”部分中列出的条款。

## 2. 核心功能

- **高质量人脸替换**: 采用强大的 `inswapper_128.onnx` 模型进行核心的人脸识别与替换操作。该模型源于先进的 `insightface` 库，确保了换脸的准确性和鲁棒性。

- **AI驱动的人脸增强**: 集成了业界领先的 `GFPGANv1.4.pth` 模型，能够自动修复和增强替换后的人脸。这一步骤极大地提升了输出视频的清晰度和真实感，有效减少了伪影。

- **Cog容器化封装**: 项目使用 Replicate 公司开发的开源工具 `cog` 进行封装。`cog` 通过一个简单的 `cog.yaml` 配置文件，便可自动处理所有系统依赖、Python包和CUDA环境，彻底告别了“CUDA地狱”，并保证了项目在任何机器上的一致性和可复现性。

- **一键云端部署**: 项目完全符合 Replicate 平台的部署标准。用户仅需一条命令，即可将此工具部署到云端，生成一个私有的、可扩展的API服务，无需任何服务器运维知识。

- **完整的视频处理流程**: 支持输入一个目标视频和一个包含源人脸的图片，直接生成一段完整的、经过换脸和画质增强处理的输出视频。

## 3. 快速上手: 使用Cog在本地运行

本节提供了一个直接、可操作的教程，引导用户在自己的计算机上运行此模型。

### 3.1. 前提条件

- **Docker**: 您的系统中必须安装Docker。Cog依赖Docker来构建和运行容器化的模型环境。
- **NVIDIA GPU (强烈推荐)**: 尽管模型理论上可以在CPU上运行，但处理视频的速度会极其缓慢。为了获得可接受的性能，强烈建议使用支持CUDA的NVIDIA GPU。
- **Cog**: 请根据您的操作系统，使用以下命令安装Cog。

  ```bash
  # macOS (使用 Homebrew)
  brew install cog
  
  # Linux
  sudo curl -o /usr/local/bin/cog -L "[https://github.com/replicate/cog/releases/latest/download/cog_$(uname](https://github.com/replicate/cog/releases/latest/download/cog_$(uname) -s)_$(uname -m)"
  sudo chmod +x /usr/local/bin/cog
  ```

### 3.2. 步骤 1: 克隆代码仓库

```bash
git clone [https://github.com/VmodelAI/video-face-swap.git](https://github.com/VmodelAI/video-face-swap.git)
cd video-face-swap
```

### 3.3. 步骤 2: 准备模型文件 (自动下载)

本项目通过 `model_manager.py` 配置了自动模型下载。当您首次运行预测时，如果脚本检测到根目录下不存在所需的模型文件（`inswapper_128.onnx` 和 `GFPGANv1.4.pth`），它将自动从预设的URL下载并放置到正确的位置。您无需手动进行任何下载操作。

### 3.4. 步骤 3: 运行预测

Cog将复杂的预测流程简化为一条命令。`cog predict` 命令在首次运行时，会根据 `cog.yaml` 的定义自动构建Docker镜像（如果尚未构建），然后执行 `predict.py` 中的 `predict()` 函数。

- **命令格式**:
  输入可以是本地文件路径（以`@`开头）或可公开访问的URL。

  ```bash
  cog predict \
    -i source="<URL_to_source_face_image>" \
    -i target="<URL_to_target_video>" \
    -i is_enhancer="<True_or_False>"
  ```

- **运行示例**:

  ```bash
  cog predict \
    -i source="[https://vmodel.ai/data/model/vmodel/photo-face-swap-pro/target_image.png](https://vmodel.ai/data/model/vmodel/photo-face-swap-pro/target_image.png)" \
    -i target="[https://raw.githubusercontent.com/VmodelAI/video-face-swap/main/examples/target.mp4](https://raw.githubusercontent.com/VmodelAI/video-face-swap/main/examples/target.mp4)" \
    -i is_enhancer="True"
  ```

  命令执行完毕后，生成的视频将保存为 `output.mp4`（或在 `predict.py` 中定义的其他输出文件名）。

## 4. 部署到 Replicate 云平台

本节面向希望为模型创建一个私有的、可扩展的API端点的用户。

### 4.1. 步骤 1: 创建 Replicate 账户和模型

1.  使用您的GitHub账户访问([https://replicate.com](https://replicate.com)) 并注册。
2.  访问 [replicate.com/create](https://replicate.com/create) 来创建一个新的模型页面。
3.  选择所有者（您的用户名或组织）、一个模型名称（例如 `video-face-swap`），并根据需要将可见性设置为“Private”（私有）。

### 4.2. 步骤 2: 本地 Cog 环境认证

在您的终端中，运行 `cog login` 命令。它会提示您输入一个从Replicate账户页面获取的API令牌。此命令会将您的凭据安全地保存在本地，以便后续推送模型。

```bash
cog login
```

### 4.3. 步骤 3: 推送模型到云端

这是最后一步。`cog push` 命令会将您的整个项目（包括代码和环境定义）打包、上传到Replicate的镜像仓库，并自动将其部署为一个实时API。

- **命令格式**:

  ```bash
  cog push r8.im/<your-replicate-username>/<your-model-name>
  ```

- **推送示例**:

  ```bash
  cog push r8.im/my-username/video-face-swap
  ```

推送成功后，您就可以通过Replicate网站的UI界面，或使用其为Python、cURL等多种语言提供的API客户端来调用您的模型了。


## 5. 对比: 本项目 vs. `video-face-swap-pro`

尽管这个开源项目为视频换脸技术提供了一个功能强大且易于上手的入口，但它的设计初衷主要是为了教育和探索。对于需要更高性能、更优画质以及商业使用授权的用户，我们推荐使用 `video-face-swap-pro`。

<img width="1600" height="900" alt="效果对比图" src="https://github.com/user-attachments/assets/a1139e9d-3466-4bd8-9eca-4109098555ee" />

| 特性 | 本项目 (开源) | `video-face-swap-pro` (商业版) |
| :--- | :--- | :--- |
| **处理速度** | 标准 | 针对速度进行深度优化 (渲染更快) |
| **输出质量** | 良好 (经GFPGAN增强) | 卓越 (伪影更少，细节更丰富) |
| **许可协议** | AGPL-3.0 (非商业) | 商业许可 (允许用于商业项目) |
| **主要应用场景** | 教育、研究、个人爱好者项目 | 专业视频制作、商业应用 |
| **技术支持** | 社区支持 (GitHub Issues) | 专属专业技术支持 |
| **了解更多** | *(您已在此处)* | **[点击此处访问 `video-face-swap-pro`](https://vmodel.ai/models/vmodel/video-face-swap-pro/)** |


## 6. 道德规范与许可协议

本节内容至关重要，旨在确保软件的负责任使用和法律合规性。

### 6.1. 免责声明: 必须负责任地使用

- 本软件仅可用于教育、艺术创作和学术研究目的。
- **用户对使用本软件生成的任何内容负全部责任。** 本项目的开发者不对任何用户生成的媒体内容承担任何法律责任。
- **禁止用途**: 严格禁止使用本软件创建任何诽谤、骚扰、色情、侵犯他人隐私或任何个人权利的内容。
- **授权是强制性的**: 如果您使用包含真实人物的图像或视频，您必须在使用他们的肖像前获得其明确的同意。在分享使用本工具创建的媒体时，您应当清晰地标注其为合成内容或“deepfake”。

### 6.2. 许可协议: GNU Affero General Public License v3.0 (AGPL-3.0)

- 本项目采用 **AGPL-3.0** 许可协议，该协议继承自其基础框架 `roop`。
- **这意味着**: 这是一个强“著佐权”（copyleft）许可。如果您修改此软件，或将其用作一个更大作品的一部分，您必须将您的修改和整个作品在相同的AGPL-3.0许可下发布。
- **网络使用条款**: AGPL的一个关键特性是，如果您在一个网络服务器上运行此软件的修改版本，并允许其他用户与其交互，您必须向这些用户提供您修改版本的完整源代码。

### 6.3. 使用限制: 仅限非商业用途

- 本项目严格限制于**非商业、教育和研究目的**。
- 此限制的设定，一方面是遵循 `roop` 项目的使用条款，另一方面也与核心模型库 `insightface` 的许可要求有关。

## 7. 致谢

本项目的实现离不开以下优秀开源项目和团队的杰出工作，在此表示衷心的感谢：

- **`roop`**: 提供了本项目所依赖的基础换脸框架。
- **`insightface`**: 提供了 `inswapper` 引擎背后的核心研究和模型。
- **`TencentARC/GFPGAN`**: 提供了强大的人脸修复模型，极大地提升了输出质量。
- **`replicate/cog`**: 提供了使模型封装和部署变得简单、可复现的关键工具。
