import os
import argparse
from pi_assistant.log import logger
from pi_assistant.profile.Room import Room
from pi_assistant.profile.Group import Group
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
        "profile:update": "",
        "profile:delete": "",
        "room:create": create_room,
        "room:delete": "",
        "group:create": create_group,
        "group:delete": "",
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

    args = parser.parse_args()

    # Execute the right action based on the pos argument command input
    pos_arg_choice_map[args.command](args)


def run(args) -> None:
    if args.profile:
        profile = Profile().load_json_file(os.path.join(".", "resources", "profile", args.profile + ".json"))
        start_assistant(profile)
    else:
        # TODO perhaps a default profile should be loaded?
        start_assistant(None)


def create_profile(args) -> None:
    """
    Creates a new profile for a home.
    :param args:
    :return:
    """
    if not args.name:
        raise Exception("The --name argument must be specified when creating a new profile.")
    profile = Profile(name=args.name)
    profile.save()
    logger.info(f"Successfully created the new profile: {args.name}!")


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
    profile = Profile.load_json_file(args, os.path.join(".", "resources", "profiles", args.profile + ".json"))
    # TODO if room already exists in profile.rooms dont add it again
    profile.rooms.append(Room(name=args.name))
    profile.save()
    logger.info(f"Successfully created a new room: {args.name} and added it to the profile: {args.profile}")


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
    profile = Profile.load_json_file(args, os.path.join(".", "resources", "profiles", args.profile + ".json"))

    # TODO if group already exists in profile.groups dont add it again
    profile.groups.append(Group(name=args.name))
    profile.save()
    logger.info(f"Successfully created a new group: {args.name} and added it to the profile: {args.profile}")

if __name__ == "__main__":
    main()
