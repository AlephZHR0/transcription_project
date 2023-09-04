import re
import subprocess
from typing import Tuple

MODELS = ["tiny", "base", "small", "medium", "large-v2"]


def get_gpu_info() -> Tuple[bool, str]:
    """
    Returns whether an Nvidia GPU is found and the output of the nvidia-smi command.

    Returns:
        A tuple containing:
            A boolean indicating whether an Nvidia GPU is found
            A string containing the output of the nvidia-smi command
    """
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        gpu_info = result.stdout
        is_nvidia = True
    except subprocess.CalledProcessError:
        is_nvidia = False
        gpu_info = ""
    return is_nvidia, gpu_info


def parse_gpu_info(gpu_info: str) -> Tuple[str, str]:
    """
    Parses gpu_info and returns gpu_name, available_memory

    Args:
        gpu_info (str): output of nvidia-smi command

    Returns:
        A tuple containing:
            gpu_name (str): Name of the GPU
            available_memory (str): Available memory in MiB
    """
    gpu_name = re.search(r"(?<=NVIDIA GeForce )\w+\s*\w*", gpu_info)
    gpu_name = gpu_name.group() if gpu_name else "N/A"

    available_memory = re.search(r"(?<=MiB /  )\d+", gpu_info)
    available_memory = available_memory.group() if available_memory else "N/A"

    return gpu_name, available_memory


def has_cuda(gpu_info: str) -> bool:
    """
    Returns whether CUDA is available

    Args:
        gpu_info (str): Output of nvidia-smi command

    Returns:
        bool: True if CUDA is available, False otherwise
    """
    return "CUDA Version" in gpu_info


def recommend_model(available_memory: str) -> str:
    """
    Returns the recommended model based on the available memory

    Args:
        available_memory (str): available memory in MiB

    Returns:
        str: recommended model
    """
    available_memory = int(available_memory) / 1024
    if available_memory > 10:
        return MODELS[4]
    elif available_memory > 5:
        return MODELS[3]
    elif available_memory > 2:
        return MODELS[2]
    elif available_memory > 1:
        return MODELS[1]
    else:
        return MODELS[0]


def get_specs_and_return_right_model() -> Tuple[str, str]:
    """
    Returns the recommended model and available memory of the Nvidia GPU if found, otherwise returns "tiny" and "N/A"

    Returns:
        A tuple containing:
            recommended model (str)
            available memory in MiB (str)
    """
    is_nvidia, gpu_info = get_gpu_info()
    if is_nvidia:
        gpu_name, available_memory = parse_gpu_info(gpu_info)
        print(f"""GPU Info:
Name: {gpu_name}
Available Memory: {available_memory} MiB
""")
        if has_cuda(gpu_info):
            print("Nvidia GPU with CUDA found.")
            model = recommend_model(available_memory)
            print(f"Recommended model: {model}")
            return model, available_memory
        else:
            print("No CUDA found.")
            return "tiny", "N/A"
    else:
        print("No Nvidia GPU found.")
        return "tiny", "N/A"
