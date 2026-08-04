from .multi_sync import LaunchpadDuoSync


def create_instance(c_instance):
    return LaunchpadDuoSync(c_instance)
