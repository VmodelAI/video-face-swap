[简体中文](README_zh-CN.md)

# Video Face Swap

## 1. Project Overview

This project is an open-source video face swapping tool developed based on `roop`. By leveraging **Cog** for containerization, it seamlessly integrates with the **Replicate** cloud platform, allowing anyone to deploy and run it with ease. The project integrates the `inswapper_128.onnx` face-swapping model and the `GFPGANv1.4.pth` face enhancement model, aiming to provide AI enthusiasts and researchers with a simple and user-friendly video face-swapping solution.

**Important Declaration**: This project is intended for academic research and educational purposes only. Commercial use is strictly prohibited. All users must comply with the terms outlined in the "Ethics and License" section.

## 2. Core Features

-   **High-Quality Face Swapping**: Utilizes the powerful `inswapper_128.onnx` model for core face detection and replacement. This model, derived from the advanced `insightface` library, ensures accuracy and robustness in the swapping process.

-   **AI-Driven Face Enhancement**: Integrates the industry-leading `GFPGANv1.4.pth` model to automatically restore and enhance the swapped faces. This step significantly improves the clarity and realism of the output video, effectively reducing artifacts.

-   **Cog Containerization**: The project is packaged using `cog`, an open-source tool developed by Replicate. Through a simple `cog.yaml` configuration file, `cog` automatically handles all system dependencies, Python packages, and CUDA environments, completely eliminating the "CUDA hell" and ensuring consistency and reproducibility across any machine.

-   **One-Click Cloud Deployment**: Fully compliant with the Replicate platform's deployment standards. Users can deploy this tool to the cloud with a single command, creating a private, scalable API service without needing any server operations knowledge.

-   **End-to-End Video Processing**: Supports a target video and a source face image as input to directly generate a complete output video that has undergone both face swapping and quality enhancement.

## 3. Quick Start: Running Locally with Cog

This section provides a direct, actionable tutorial for running this model on your own computer.

### 3.1. Prerequisites

-   **Docker**: You must have Docker installed on your system. Cog relies on Docker to build and run the containerized model environment.
-   **NVIDIA GPU (Highly Recommended)**: While the model can theoretically run on a CPU, video processing will be extremely slow. An NVIDIA GPU with CUDA support is strongly recommended for acceptable performance.
-   **Cog**: Install Cog using the command for your operating system.

    ```bash
    # macOS (using Homebrew)
    brew install cog
    
    # Linux
    sudo curl -o /usr/local/bin/cog -L "[https://github.com/replicate/cog/releases/latest/download/cog_$(uname](https://github.com/replicate/cog/releases/latest/download/cog_$(uname) -s)_$(uname -m)"
    sudo chmod +x /usr/local/bin/cog
    ```

### 3.2. Step 1: Clone the Repository

```bash
git clone [https://github.com/VmodelAI/video-face-swap.git](https://github.com/VmodelAI/video-face-swap.git)
cd video-face-swap
```

### 3.3. Step 2: Prepare Model Files (Automatic Download)

This project is configured with `model_manager.py` for automatic model downloading. The first time you run a prediction, the script will check if the required model files (`inswapper_128.onnx` and `GFPGANv1.4.pth`) exist in the root directory. If not, they will be automatically downloaded from a preset URL. You do not need to download anything manually.

### 3.4. Step 3: Run Prediction

Cog simplifies the complex prediction process into a single command. The `cog predict` command will first build the Docker image based on `cog.yaml` (if not already built) and then execute the `predict()` function in `predict.py`.

-   **Command Format**:
    Inputs can be local file paths (prefixed with `@`) or publicly accessible URLs.

    ```bash
    cog predict \
      -i source="<URL_to_source_face_image>" \
      -i target="<URL_to_target_video>" \
      -i is_enhancer="<True_or_False>"
    ```

-   **Example Command**:

    ```bash
    cog predict \
      -i source="[https://vmodel.ai/data/model/vmodel/photo-face-swap-pro/target_image.png](https://vmodel.ai/data/model/vmodel/photo-face-swap-pro/target_image.png)" \
      -i target="[https://raw.githubusercontent.com/VmodelAI/video-face-swap/main/examples/target.mp4](https://raw.githubusercontent.com/VmodelAI/video-face-swap/main/examples/target.mp4)" \
      -i is_enhancer="True"
    ```

    After the command finishes, the resulting video will be saved as `output.mp4` (or another filename defined in `predict.py`).

## 4. Deploying to Replicate Cloud Platform

This section is for users who want to create a private, scalable API endpoint for the model.

### 4.1. Step 1: Create a Replicate Account and Model

1.  Sign up for Replicate using your GitHub account at [https://replicate.com](https://replicate.com).
2.  Go to [replicate.com/create](https://replicate.com/create) to create a new model page.
3.  Select an owner (your username or an organization), a model name (e.g., `video-face-swap`), and set the visibility to "Private" as needed.

### 4.2. Step 2: Authenticate Your Local Cog Environment

In your terminal, run the `cog login` command. It will prompt you for an API token from your Replicate account page. This command securely stores your credentials locally for pushing models.

```bash
cog login
```

### 4.3. Step 3: Push the Model to the Cloud

This is the final step. The `cog push` command will package your entire project (code and environment definition), upload it to Replicate's registry, and automatically deploy it as a live API.

-   **Command Format**:

    ```bash
    cog push r8.im/<your-replicate-username>/<your-model-name>
    ```

-   **Example Push**:

    ```bash
    cog push r8.im/my-username/video-face-swap
    ```

After a successful push, you can call your model via the Replicate website UI or using their API clients for Python, cURL, and other languages.

## 5. Comparison: This Project vs. `video-face-swap-pro`

While this open-source project provides a powerful and accessible entry point into video face-swapping technology, it is primarily designed for educational and exploratory purposes. For users requiring higher performance, superior image quality, and a commercial license, we recommend `video-face-swap-pro`.

<img width="1600" height="900" alt="Comparison Image" src="https://github.com/user-attachments/assets/d43da18e-9e05-4a58-adf6-d5e8639ca535" />


| Feature | This Project (Open-Source) | `video-face-swap-pro` (Commercial) |
| :--- | :--- | :--- |
| **Processing Speed** | Standard | Highly optimized for speed (faster rendering) |
| **Output Quality** | Good (with GFPGAN enhancement) | Excellent (fewer artifacts, richer details) |
| **License** | AGPL-3.0 (Non-Commercial) | Commercial License (allows for commercial use) |
| **Primary Use Case** | Education, research, hobbyist projects | Professional video production, commercial apps |
| **Technical Support**| Community support (GitHub Issues) | Dedicated professional support |
| **Learn More** | *(You are here)* | **[Click here to visit `video-face-swap-pro`](https://vmodel.ai/models/vmodel/video-face-swap-pro/)** |

## 6. Ethics and License

This section is critically important to ensure responsible use and legal compliance.

### 6.1. Disclaimer: Responsible Use is Mandatory

-   This software is intended for educational, artistic, and academic purposes only.
-   **The user is solely responsible for any content created with this software.** The developers of this project assume no liability for any media generated by users.
-   **Prohibited Uses**: It is strictly forbidden to use this software to create content that is defamatory, harassing, pornographic, or that violates the privacy or any rights of any individual.
-   **Consent is Mandatory**: You must obtain explicit consent from any real person whose likeness you use in an image or video. When sharing media created with this tool, you should clearly label it as synthetic or a "deepfake."

### 6.2. License: GNU Affero General Public License v3.0 (AGPL-3.0)

-   This project is licensed under **AGPL-3.0**, a license inherited from its base framework, `roop`.
-   **What this means**: This is a strong "copyleft" license. If you modify this software or use it as part of a larger work, you must release your modifications and the entire work under the same AGPL-3.0 license.
-   **Network Use Clause**: A key feature of the AGPL is that if you run a modified version of this software on a network server and allow other users to interact with it, you must provide them with the full source code of your modified version.

### 6.3. Usage Restrictions: Non-Commercial Use Only

-   This project is strictly limited to **non-commercial, educational, and research purposes**.
-   This restriction is in place to comply with the terms of use of the `roop` project and the licensing requirements of the core `insightface` model library.

## 7. Acknowledgements

The realization of this project would not have been possible without the outstanding work of the following open-source projects and teams. We extend our sincere gratitude to:

-   **`s0md3v/roop`**: For providing the foundational face-swapping framework upon which this project is built.
-   **`deepinsight/insightface`**: For the core research and models behind the `inswapper` engine.
-   **`TencentARC/GFPGAN`**: For the powerful face restoration model that significantly improves output quality.
-   **`replicate/cog`**: For the essential tool that makes model packaging and deployment simple and reproducible.
