import subprocess
import time
from prometheus_client import start_http_server, Gauge
import psutil

HOST_TYPE_INFO = Gauge(
    'host_type_info', 'Information about the host type', ['host_type'])
HOST_CPU_USAGE = Gauge('host_cpu_usage_percent',
                       'Current CPU usage percentage')
HOST_MEMORY_USAGE = Gauge('host_memory_usage_bytes',
                          'Current memory usage in bytes')
HOST_UPTIME = Gauge('host_uptime_seconds', 'System uptime in seconds')


def detect_host_type():
    def check_cgroup():
        try:
            with open('/proc/1/cgroup', 'r') as f:
                content = f.read()
                if any(x in content for x in ['docker', 'containerd', 'kubepods', 'lxc']):
                    return True
        except Exception:
            pass
        return False

    def check_mountinfo():
        try:
            with open('/proc/self/mountinfo', 'r') as f:
                for line in f:
                    if '/docker/' in line or '/containers/' in line:
                        return True
        except Exception:
            pass
        return False

    def check_systemd_detect_virt():
        try:
            result = subprocess.run(
                ['systemd-detect-virt', '--quiet'],
                check=False
            )
            if result.returncode == 0:
                result_name = subprocess.run(
                    ['systemd-detect-virt'],
                    capture_output=True, text=True, check=False
                ).stdout.strip()
                if result_name in ['docker', 'lxc', 'container-other']:
                    return 'container'
                else:
                    return 'vm'
        except FileNotFoundError:
            pass
        return None

    def check_dmi_vendor():
        try:
            with open('/sys/class/dmi/id/sys_vendor', 'r') as f:
                vendor = f.read().strip().lower()
                if any(x in vendor for x in ['vmware', 'virtualbox', 'kvm', 'qemu', 'xen', 'microsoft']):
                    return True
        except Exception:
            pass
        return False

    if check_cgroup() or check_mountinfo():
        return 'container'

    systemd_result = check_systemd_detect_virt()
    if systemd_result:
        return systemd_result

    if check_dmi_vendor():
        return 'vm'

    return 'physical'


def update_metrics():

    HOST_CPU_USAGE.set(psutil.cpu_percent(interval=1))

    memory = psutil.virtual_memory()
    HOST_MEMORY_USAGE.set(memory.used)

    HOST_UPTIME.set(time.time() - psutil.boot_time())


def main():
    host_type = detect_host_type()

    print(detect_host_type())
    start_http_server(8080)
    print("Prometheus metrics server started on port 8080")
    HOST_TYPE_INFO.labels(host_type=host_type).set(1)
    while True:
        update_metrics()
        time.sleep(10)


if __name__ == '__main__':
    main()
