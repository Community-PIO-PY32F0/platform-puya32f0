import os
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

env.SConscript("_bare.py")

HAL_SDK_DIR = platform.get_package_dir("framework-puya-py32f0-hal-sdk")

env.Append(
    CPPPATH=[
        os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_Driver", "Src", ),
        os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_BSP", "Src"),
        os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_Driver", "Inc", ),
        os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_BSP", "Inc"),
    ],
    CPATH=[
        os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_Driver", "Src", ),
        os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_BSP", "Src"),
        os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_Driver", "Inc", ),
        os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_BSP", "Inc"),
    ],
    CPPDEFINES=[
        "USE_HAL_DRIVER",
    ],
    CDEFINES=[
        "USE_HAL_DRIVER",
    ],
)

env.BuildSources(
    os.path.join("$BUILD_DIR", "FrameworkHALDriver"), os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_Driver", "Src", ),
    src_filter=[
        "-<*>",
        "+<*.c>",
    ]
)

env.BuildSources(
    os.path.join("$BUILD_DIR", "FrameworkHALBSP"), os.path.join(HAL_SDK_DIR, "PY32F0xx_HAL_BSP", "Src", ),
    src_filter=[
        "-<*>",
        "+<*.c>",
    ]
)