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
        "profile:update": "", # TODO
        "profile:delete": delete_profile,
        "room:create": create_room,
        "room:delete": delete_room,
        "group:create": create_group,
        "group:delete": delete_group,
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


def create_profile(args) -> None:
    """
    Creates a new profile for a home.
    :param args:
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
    # TODO if room already exists in profile.rooms dont add it again
    profile.rooms.append(Room(name=args.name))
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
    i = 0
    print(profile.rooms)
    for room in profile.rooms:
        if room['name'].lower() == args.name:
            break
        i += 1
    del profile.rooms[i]
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
    i = 0
    for group in profile.groups:
        if group['name'].lower() == args.name:
            break
        i += 1
    del profile.groups[i]
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

    # TODO if group already exists in profile.groups dont add it again
    profile.groups.append(Group(name=args.name))
    profile.save()
    logger.info(f"Successfully created a new group: {args.name} and added it to the profile: {args.profile}")


if __name__ == "__main__":
    main()
