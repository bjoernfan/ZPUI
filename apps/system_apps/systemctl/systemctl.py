from helpers import setup_logger
from pydbus import SystemBus

logger = setup_logger(__name__, "warning")

bus = SystemBus()
systemd = bus.get(".systemd1")

def list_units(unit_filter_field = None, unit_filter_value = None):
    units = []

    for unit in systemd.ListUnits():
        name, description, load, active, sub, follower, unit_object_path, job_queued, job_type, job_object_path = unit

        basename, type = name.rsplit('.', 1)

        # FIXME: eval() should probably be getattr() somehow
        if unit_filter_field is None or eval(unit_filter_field) in unit_filter_value:
            units.append({
                "name": name,
                "basename": basename,
                "type": type,
                "description": description,
                "load": load,
                "active": active,
                "sub": sub,
                "follower": follower,
                "unit_object_path": unit_object_path,
                "job_queued": job_queued,
                "job_type": job_type,
                "job_object_path": job_object_path
            })

    return units


def action_unit(action, unit):
    try:
        output = subprocess.check_output(["systemctl", action, unit])
        return True
    except subprocess.CalledProcessError:
        return False


if __name__ == "__main__":
    units_loaded = list_units('load', ['loaded'])
    units_active = list_units('active', ['active'])
    units_sub    = list_units('sub', ['sub'])

    for unit in units_loaded:
        print(unit["name"])

    for unit in units_active:
        print(unit["name"])

    for unit in units_sub:
        print(unit["name"])
