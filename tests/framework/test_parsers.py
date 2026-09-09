"""Framework unit tests for parsers."""
import pytest
from framework.parsers.unix_parser import UnixParser, DfParser, PsParser


class TestUnixParser:
    """Test Unix command parsers."""

    def test_parse_ls_output(self):
        """Test parsing ls output."""
        output = """total 24
drwxr-xr-x  2 user group  4096 Jan  1 12:00 dir1
-rw-r--r--  1 user group   100 Jan  1 12:00 file1.txt
"""
        files = UnixParser.parse_ls_output(output)
        
        assert len(files) == 2
        assert files[0]['name'] == 'dir1'
        assert files[1]['name'] == 'file1.txt'
        assert files[0]['permissions'].startswith('d')
        assert files[1]['permissions'].startswith('-')


class TestDfParser:
    """Test df command parser."""

    def test_parse_df_output(self):
        """Test parsing df output."""
        output = """Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        20G   10G   10G  50% /
devtmpfs        16G     0   16G   0% /dev
"""
        filesystems = DfParser.parse_df_output(output)
        
        assert len(filesystems) == 2
        assert filesystems[0]['filesystem'] == '/dev/sda1'
        assert filesystems[0]['use_percent'] == '50%'
        assert filesystems[1]['mounted_on'] == '/dev'


class TestPsParser:
    """Test ps command parser."""

    def test_parse_ps_output(self):
        """Test parsing ps output."""
        output = """USER       PID  %CPU %MEM   VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0  1234  5678 ?    Ss   12:00   0:01 /sbin/init
user      1234  0.1  0.5  5678  9012 pts/0 S    12:01   0:02 bash
"""
        processes = PsParser.parse_ps_output(output)
        
        assert len(processes) == 2
        assert processes[0]['user'] == 'root'
        assert processes[0]['command'] == '/sbin/init'
        assert processes[1]['user'] == 'user'
        assert processes[1]['pid'] == '1234'

