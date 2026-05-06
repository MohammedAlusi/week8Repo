import re
import datetime

class LogParser:

    @staticmethod
    def parse_pfsense(log_line):
        try:
            parts = log_line.split(',')
            if 'filterlog' in log_line:
                return {
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "source_ip": parts[18] if len(parts) > 18 else "unknown",
                    "destination_ip": parts[19] if len(parts) > 19 else "unknown",
                    "event_type": "firewall_block" if "block" in log_line else "firewall_pass",
                    "severity": "high" if "block" in log_line else "low",
                    "raw_message": log_line,
                    "parsed_data": {
                        "interface": parts[4] if len(parts) > 4 else "unknown"
                    }
                }
        except Exception as e:
            return {"error": str(e)}

        return None

    @staticmethod
    def parse_auth_log(log_line):
        if "Failed password" in log_line:
            ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', log_line)
            return {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "source_ip": ip_match.group(1) if ip_match else "unknown",
                "destination_ip": "localhost",
                "event_type": "failed_login",
                "severity": "critical",
                "raw_message": log_line,
                "parsed_data": {
                    "service": "sshd"
                }
            }
        return None

    @staticmethod
    def parse_custom_log(log_line):
        try:
            pattern = r'\[(.*?)\] \[(.*?)\] \[(.*?)\] SRC:(.*?) DST:(.*?) MSG:(.*)'
            match = re.search(pattern, log_line)
            if match:
                return {
                    "timestamp": match.group(1),
                    "severity": match.group(2).lower(),
                    "event_type": match.group(3).lower(),
                    "source_ip": match.group(4),
                    "destination_ip": match.group(5),
                    "raw_message": log_line,
                    "parsed_data": {
                        "message": match.group(6)
                    }
                }
        except Exception as e:
            return {"error": str(e)}

        return None

    @classmethod
    def parse(cls, log_line, format_type='auto'):
        if format_type == 'pfsense' or ('filterlog' in log_line):
            result = cls.parse_pfsense(log_line)
            if result:
                return result

        if format_type == 'auth' or ('Failed password' in log_line):
            result = cls.parse_auth_log(log_line)
            if result:
                return result

        if format_type == 'custom' or log_line.startswith('['):
            result = cls.parse_custom_log(log_line)
            if result:
                return result

        return {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "source_ip": "unknown",
            "destination_ip": "unknown",
            "event_type": "unknown",
            "severity": "info",
            "raw_message": log_line,
            "parsed_data": {}
        }