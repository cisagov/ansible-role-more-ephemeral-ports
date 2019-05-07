"""Module containing the tests for the default scenario."""

import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("directory", [{"path": "/etc/sysctl.d", "mode": "0o755"}])
def test_directories(host, directory):
    """Test that the appropriate directories were created."""
    assert host.file(directory["path"]).exists
    assert host.file(directory["path"]).is_directory
    if "mode" in directory:
        assert oct(host.file(directory["path"]).mode) == directory["mode"]


@pytest.mark.parametrize(
    "file,content",
    [
        (
            "/etc/sysctl.d/99-more_ephemeral_ports.conf",
            "^net.ipv4.ip_local_port_range = 1024 65535$",
        )
    ],
)
def test_files(host, file, content):
    """Test that config files were modified as expected."""
    f = host.file(file)

    assert f.exists
    assert f.contains(content)
