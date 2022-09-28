import subprocess
import tempfile
import time
from pathlib import Path
from typing import Optional

FUNNEL_GIT_SOURCE = "https://github.com/ohsu-comp-bio/funnel.git"
DEFAULT_SHUTDOWN_TIMEOUT = 5


class FunnelServer:
    _root: Path
    _shutdown_timeout: float
    _verbose: bool
    _proc = Optional[subprocess.Popen]

    def __init__(
        self,
        root=None,
        shutdown_timeout: float = DEFAULT_SHUTDOWN_TIMEOUT,
        verbose: bool = False,
    ):
        if root is None:
            root = tempfile.mkdtemp(prefix="pyfunnel")
        self._root = Path(root)
        self._verbose = verbose
        self._shutdown_timeout = shutdown_timeout

    def start(self):
        self._run(["git", "clone", FUNNEL_GIT_SOURCE, str(self._src_dir)])
        verbose_str = "-v" if self._verbose else ""
        self._run(["sh", "-c", f"cd '{self._src_dir}'; go build {verbose_str} ./"])
        proc = subprocess.Popen(
            [str(self._funnel_executable), "server", "run"],
            stdout=None,
            stderr=None,
        )
        self._proc = proc

    def stop(self):
        self._proc.terminate()
        self._proc.communicate(timeout=self._shutdown_timeout)

    def _run(self, commands) -> None:
        print(commands)
        completed_process = subprocess.run(commands)
        if completed_process.returncode != 0:
            stdout = self._bytes_as_str(completed_process.stdout)
            stderr = self._bytes_as_str(completed_process.stderr)
            raise Exception(
                f"Failed execute command [{commands}], stdout [{stdout}], stderr [{stderr}]"
            )

    def _bytes_as_str(self, as_bytes: Optional[bytes]) -> str:
        return as_bytes.decode("utf-8") if as_bytes else ""

    @property
    def _funnel_executable(self) -> Path:
        return self._src_dir / "funnel"

    @property
    def _src_dir(self) -> Path:
        return self._root / "src"


if __name__ == "__main__":
    server = FunnelServer()
    server.start()
    time.sleep(5)
    server.stop()
