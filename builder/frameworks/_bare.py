# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Default flags for bare-metal programming (without any framework layers)
#
import os
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

CMSIS_DIR = platform.get_package_dir("framework-puya-py32f0-cmsis")
LDSCRIPTS_DIR = os.path.join(CMSIS_DIR, "LDScripts")
CMSIS_DEVICE_DIR = os.path.join(CMSIS_DIR, "CMSIS", "Device", "PY32F0xx")

assert all(os.path.isdir(d) for d in (CMSIS_DIR, CMSIS_DEVICE_DIR, LDSCRIPTS_DIR))

# MCU types: 
#   PY32F002Ax5
#   PY32F003x4, PY32F003x6, PY32F003x8,
#   PY32F030x6, PY32F030x8, 
#   PY32F072xB

# Not yet supported:
# PY32F002Bx5, PY32F072xB

mcu_type = str(board.get("build.mcu", "")).lower()
lib_flags = mcu_type
ld_script = os.path.join(LDSCRIPTS_DIR, f"{mcu_type}.ld")
startup_file_suffix = mcu_type.split("x")[0]

# Arch and target specified flags
ARCH_FLAGS = [
    "-mthumb",
    "-mcpu=cortex-m0plus",
]

OPTIMIZATION_FLAGS = [
    "-Os",  # optimize for size
]

env.Append(
    # ASM flags
    ASFLAGS=[
        *ARCH_FLAGS,
    ],

    # ASM with CPP flags 
    ASPPFLAGS=[
        *ARCH_FLAGS,
        "-x", "assembler-with-cpp",
    ],

    # C flags
    CFLAGS=[
        *ARCH_FLAGS,
        *OPTIMIZATION_FLAGS,
        "-std=c99",
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-Wall",
    ],

    # C++ flags
    CXXFLAGS=[
        *ARCH_FLAGS,
        *OPTIMIZATION_FLAGS,
        "-std=c++11",
        "-fno-rtti",
        "-fno-exceptions",
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-Wall",
    ],

    LINKFLAGS=[
        *ARCH_FLAGS,
        *OPTIMIZATION_FLAGS,
        "-specs=nano.specs",
        "-specs=nosys.specs",
        "-static",
        "-Wl,--gc-sections",
        "-Wl,--print-memory-usage",
        "-Wl,-Map=$BUILD_DIR/app.map",
        "-Wl,--no-warn-rwx-segments"
    ],

    CPPDEFINES=[
        mcu_type.upper().replace("X", "x"),
    ],

    CDEFINES=[
        mcu_type.upper().replace("X", "x"),
    ],

    LIBS=["c", "m"]
)

env.Replace(LDSCRIPT_PATH=ld_script)

env.Append(
    CPPPATH=[
        os.path.join(CMSIS_DIR, "CMSIS", "Core", "Include"),
        os.path.join(CMSIS_DEVICE_DIR, "Include")
    ],
    CPATH=[
        os.path.join(CMSIS_DIR, "CMSIS", "Core", "Include"),
        os.path.join(CMSIS_DEVICE_DIR, "Include")
    ],
)

sources_path = os.path.join(CMSIS_DEVICE_DIR, "Source")

env.BuildSources(
    os.path.join("$BUILD_DIR", "FrameworkCMSIS"), sources_path,
    src_filter=[
        "-<*>",
        # TODO: match system file properly
        "+<system_py32f0xx.c>",
        "+<gcc/startup_%s.s>"
        % startup_file_suffix
    ]
)
