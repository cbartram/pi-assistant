import os
import json
import argparse
from pi_assistant.log import logger
from collections import defaultdict
from pi_assistant.main import start_assistant
from pi_assistant.profile.Profile import Profile


__version__ = "0.0.1"


def main():
    """
    CLI Version of the application which handles creating profiles, rooms, and groups as well as starting the
    assistant with a specific profile.
    :return:
    """
    pos_arg_choice_map = {
        "app:start": run,
        "profile:create": create_profile,
        "profile:update": lambda x: x,  # TODO
        "profile:delete": delete_profile,
        "room:create": create_room,
        "room:delete": delete_room,
        "group:create": create_group,
        "group:delete": delete_group,
        "device:link": link_device,
        "device:unlink": lambda x: x  # TODO
    }
    parser = argparse.ArgumentParser(description='Pi Assistant - Smart Home Assistant')
    parser.add_argument('command', type=str, help='A required string positional argument'
                                                  ' which designates which service to invoke for the assistant. '
                                                  'This can be one of: "app", "profile", "room", "group".',
                        choices=pos_arg_choice_map.keys())
    parser.add_argument('--profile', type=str, help='The name of the profile the assistant should load and use.'
                                                             ' A profile designates a specific home, set of rooms, and'
                                                             ' groups which can be used in the voice commands the '
                                                             'assistant processes.',
                        required=False)
    parser.add_argument('--name', help='An argument used to give a name to a profile, room, or '
                                       'group that is being created.', required=False)

    parser.add_argument('--room', help='An argument used to specify a room name to add an IoT device to.',
                        required=False)

    args = parser.parse_args()

    # Execute the right action based on the pos argument command input
    pos_arg_choice_map[args.command](args)


def run(args) -> None:
    """
    Runs the primary assistant program and starts listening via the Microphone.
    :param: args:
    :return:
    """
    if args.profile:
        profile = Profile().load_json_file(os.path.join(".", "resources", "profile", args.profile + ".json"))
        start_assistant(profile)
    else:
        # TODO perhaps a default profile should be loaded?
        start_assistant(None)


def link_device(args) -> None:
    if not args.profile:
        raise Exception("You must specify the --profile option in order to add a device to a specific room.")

    if not args.name:
        raise Exception("The --name argument must be specified when linking a device to a room. "
                        "The name argument should be the name of the device.")

    if not args.room:
        raise Exception("The --room argument is required when linking a device to a specific room.")

    profile = Profile.load_json_file(os.path.join(".", "resources", "profiles", args.profile + ".json"))

    if args.room.lower() not in profile.rooms:
        raise Exception(f"No room could be found in the profile: {args.profile} with the name: {args.room.lower()}")

    current_devices = profile.rooms[args.room.lower()]
    try:
        with open(os.path.join('.', 'resources', 'devices.json'), 'r') as device_file:
            devices = json.loads(device_file.read())
            device_file.close()

        # Devices are keyed by the plugin name
        for k in devices.keys():
            for device in devices[k]:
                # TODO Should this be case sensitive?
                if device['name'].lower() == args.name.lower():
                    if device['name'].lower() in current_devices:
                        raise Exception(f"The device: {device['name'].lower()} "
                                        f"already belongs to the room: {args.room.lower()}.")
                    else:
                        current_devices[args.name.lower()] = device

        profile.rooms[args.room.lower()] = current_devices
        logger.info(f"Successfully linked device {args.name} to room {args.room} in profile: {args.profile}.")
        profile.save()
    except Exception as e:
        logger.error(f"Error thrown while attempting to link device: {args.name} to room: {args.room}. "
                     f"Error = {str(e)}")


def create_profile(args) -> None:
    """
    Creates a new profile for a home.
    :param: args:
    :return:
    """
    if not args.name:
        raise Exception("The --name argument must be specified when creating a new profile.")
    profile = Profile()
    profile.name = args.name
    profile.save()
    logger.info(f"Successfully created the new profile: {args.name}!")


def delete_profile(args):
    """
    Deletes a profile from the application.
    :param args:
    :return:
    """
    if not args.name:
        raise Exception("The --name argument must be specified when deleting an existing profile.")
    os.unlink(os.path.join(".", "resources", "profiles", args.name + ".json"))


def create_room(args) -> None:
    """
    Creates a new room and adds it to the specified profile.
    :param args:
    :return:
    """
    if not args.profile:
        raise Exception("You must specify the --profile option in order to add a room to a specific profile.")

    if not args.name:
        raise Exception("The --name argument must be specified when creating a new room.")
    profile = Profile.load_json_file(os.path.join(".", "resources", "profiles", args.profile + ".json"))

    if args.name.lower() in profile.rooms:
        raise Exception(f"The room name: {args.name} already exists in the profile: {args.profile}. "
                        f"Please use a new --name.")

    profile.rooms[args.name.lower()] = defaultdict(dict)
    profile.save()
    logger.info(f"Successfully created a new room: {args.name} and added it to the profile: {args.profile}")


def delete_room(args) -> None:
    """
    Removes a room from a given profile using the room's name.
    :param args:
    :return:
    """
    if not args.profile:
        raise Exception("You must specify the --profile option in order to delete a room to a specific profile.")

    if not args.name:
        raise Exception("The --name argument must be specified when deleting an existing room.")

    profile = Profile.load_json_file(os.path.join(".", "resources", "profiles", args.profile + ".json"))
    del profile.rooms[args.name.lower()]
    profile.save()


def delete_group(args) -> None:
    """
    Removes a group from a given profile using the groups's name.
    :param args:
    :return:
    """
    if not args.profile:
        raise Exception("You must specify the --profile option in order to delete a group to a specific profile.")

    if not args.name:
        raise Exception("The --name argument must be specified when deleting an existing group.")

    profile = Profile.load_json_file(os.path.join(".", "resources", "profiles", args.profile + ".json"))
    del profile.groups[args.name.lower()]
    profile.save()


def create_group(args) -> None:
    """
    Creates a new group and adds it to the specified profile.
    :param args:
    :return:
    """
    if not args.profile:
        raise Exception("You must specify the --profile option in order to add a group to a specific profile.")

    if not args.name:
        raise Exception("The --name argument must be specified when creating a new group.")
    profile = Profile.load_json_file(os.path.join(".", "resources", "profiles", args.profile + ".json"))

    if args.name.lower() in profile.groups:
        raise Exception(f"The group name: {args.name} already exists in the profile: {args.profile}. "
                        f"Please use a new --name.")

    profile.groups[args.name.lower()] = defaultdict(dict)
    profile.save()
    logger.info(f"Successfully created a new group: {args.name} and added it to the profile: {args.profile}")


if __name__ == "__main__":
    main()
