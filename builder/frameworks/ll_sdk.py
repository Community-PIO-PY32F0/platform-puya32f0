import os
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

env.SConscript("_bare.py")

LL_SDK_DIR = platform.get_package_dir("framework-puya-py32f0-ll-sdk")

env.Append(
    CPPPATH=[
        os.path.join(LL_SDK_DIR, "PY32F0xx_LL_Driver", "Src", ),
        os.path.join(LL_SDK_DIR, "PY32F0xx_LL_BSP", "Src"),
        os.path.join(LL_SDK_DIR, "PY32F0xx_LL_Driver", "Inc", ),
        os.path.join(LL_SDK_DIR, "PY32F0xx_LL_BSP", "Inc"),
    ],
    CPATH=[
        os.path.join(LL_SDK_DIR, "PY32F0xx_LL_Driver", "Src", ),
        os.path.join(LL_SDK_DIR, "PY32F0xx_LL_BSP", "Src"),
        os.path.join(LL_SDK_DIR, "PY32F0xx_LL_Driver", "Inc", ),
        os.path.join(LL_SDK_DIR, "PY32F0xx_LL_BSP", "Inc"),
    ],
    CPPDEFINES=[
        "USE_FULL_LL_DRIVER",
    ],
    CDEFINES=[
        "USE_FULL_LL_DRIVER",
    ],
)