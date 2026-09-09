"""Command output parsers for structured data extraction."""
import logging
import re
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class UnixParser:
    """Parse common Unix command outputs."""

    @staticmethod
    def parse_ls_output(output: str) -> List[Dict[str, str]]:
        """Parse 'ls -la' output.
        
        Args:
            output: Output from 'ls -la' command
            
        Returns:
            List of file dictionaries
        """
        files = []
        
        for line in output.strip().split('\n')[1:]:  # Skip header
            if not line.strip():
                continue
            
            parts = line.split()
            if len(parts) >= 9:
                files.append({
                    'permissions': parts[0],
                    'links': parts[1],
                    'owner': parts[2],
                    'group': parts[3],
                    'size': parts[4],
                    'month': parts[5],
                    'day': parts[6],
                    'time': parts[7],
                    'name': ' '.join(parts[8:])
                })
        
        return files


class DfParser:
    """Parse 'df' (disk free) output."""

    @staticmethod
    def parse_df_output(output: str) -> List[Dict[str, str]]:
        """Parse 'df -h' output.
        
        Args:
            output: Output from 'df -h' command
            
        Returns:
            List of filesystem dictionaries
        """
        filesystems = []
        
        for line in output.strip().split('\n')[1:]:  # Skip header
            if not line.strip():
                continue
            
            parts = line.split()
            if len(parts) >= 6:
                filesystems.append({
                    'filesystem': parts[0],
                    'size': parts[1],
                    'used': parts[2],
                    'available': parts[3],
                    'use_percent': parts[4],
                    'mounted_on': parts[5]
                })
        
        return filesystems


class PsParser:
    """Parse 'ps' (process status) output."""

    @staticmethod
    def parse_ps_output(output: str) -> List[Dict[str, str]]:
        """Parse 'ps aux' output.
        
        Args:
            output: Output from 'ps aux' command
            
        Returns:
            List of process dictionaries
        """
        processes = []
        
        for line in output.strip().split('\n')[1:]:  # Skip header
            if not line.strip():
                continue
            
            parts = line.split()
            if len(parts) >= 11:
                processes.append({
                    'user': parts[0],
                    'pid': parts[1],
                    'cpu': parts[2],
                    'mem': parts[3],
                    'vsz': parts[4],
                    'rss': parts[5],
                    'tty': parts[6],
                    'stat': parts[7],
                    'start': parts[8],
                    'time': parts[9],
                    'command': ' '.join(parts[10:])
                })
        
        return processes


class SystemctlParser:
    """Parse 'systemctl' output."""

    @staticmethod
    def parse_systemctl_status(output: str) -> Dict[str, Any]:
        """Parse 'systemctl status' output.
        
        Args:
            output: Output from 'systemctl status' command
            
        Returns:
            Dictionary with service status information
        """
        status_info = {}
        
        lines = output.strip().split('\n')
        
        for line in lines:
            if 'Loaded:' in line:
                status_info['loaded'] = line.split('Loaded:')[1].strip()
            elif 'Active:' in line:
                status_info['active'] = line.split('Active:')[1].strip()
            elif 'Process:' in line:
                status_info['process'] = line.split('Process:')[1].strip()
            elif 'CGroup:' in line:
                status_info['cgroup'] = line.split('CGroup:')[1].strip()
        
        return status_info
