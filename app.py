import argparse
from vcs import init, commit, revert, list_commits

def main():
    """Kullanıcının komut satırından girdiği komutları işler."""
    parser = argparse.ArgumentParser(description="Simple Version Control System")
    parser.add_argument('command', choices=['init', 'commit', 'revert', 'list'], help='Command to execute')
    parser.add_argument('message_or_hash', nargs='?', help='Commit message or commit hash')
    parser.add_argument('--user', required=True, help='Name of the user performing the action')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        init()
    elif args.command == 'commit':
        if not args.message_or_hash:
            print("Commit message is required for the commit command.")
        else:
            commit(args.message_or_hash, args.user)
    elif args.command == 'revert':
        if not args.message_or_hash:
            print("Commit hash is required for the revert command.")
        else:
            revert(args.message_or_hash)
    elif args.command == 'list':
        list_commits()

if __name__ == "__main__":
    main()
