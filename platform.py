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
from platformio.public import PlatformBase


class Py32f0Platform(PlatformBase):
    def get_boards(self, id_=None):
        result = super().get_boards(id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key in result:
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        upload_protocols = board.manifest.get("upload", {}).get("protocols", [])
        if "tools" not in debug:
            debug["tools"] = {}

        link = "cmsis-dap"
        
        if link in upload_protocols and link not in debug["tools"]:
            pyocd_target = board.manifest.get("build", {}).get("mcu", None).lower()
            assert pyocd_target, "Missed PyOCD target for %s" % board.id
            debug["tools"][link] = {
                "onboard": True,
                "server": {
                    "package": "tool-pyocd",
                    "executable": "$PYTHONEXE",
                    "arguments": ["pyocd-gdbserver.py", "-t", pyocd_target],
                    "ready_pattern": "GDB server started on port",
                },
            }
        board.manifest["debug"] = debug
        return board

    def configure_debug_session(self, debug_config):
        if debug_config.speed:
            if "openocd" in (debug_config.server or {}).get("executable", ""):
                debug_config.server["arguments"].extend(
                    ["-c", "adapter speed %s" % debug_config.speed]
                )


# type: ignore
