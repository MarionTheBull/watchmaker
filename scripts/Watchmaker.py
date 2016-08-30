#!/usr/bin/env python
import argparse

from watchmaker import Prepare

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--noreboot', dest='noreboot', action='store_true',
                        help='No reboot after provisioning.')
    parser.add_argument('--sourceiss3bucket', dest='sourceiss3bucket', action='store_true',
                        help='Use S3 buckets instead of internet locations for files.')
    parser.add_argument('--config', dest='config', default='config.yaml',
                        help='Path or URL to the config.yaml file.')
    parser.add_argument('--logger', dest='logger', action='store_true', default=False,
                        help='Use stream logger for debugging.')
    parser.add_argument('--log-path', dest='log_path', default=None,
                        help='Path to the logfile for stream logging.')
    parser.add_argument('--saltstates', dest='saltstates', default=None,
                        help='Define the saltstates to use.  Must be None, Highstate, or comma-separated-string')

    if parser.parse_args().saltstates:
        if parser.parse_args().saltstates.lower() not in ['None'.lower(),
                                                          'Highstate'.lower(),
                                                          'comma-separated-string'.lower()]:
            parser.print_help()

    systemprep = Prepare(parser.parse_args())
    systemprep.install_system()


def append_file(build, file_paths):
    # The version line must have the form
    # __version__ = 'ver'
    pattern = r"^(__version__ = ['\"])([^'\"]*)(['\"])"
    repl = r"\g<1>\g<2>.dev{0}\g<3>".format(build)
    version_file = os.path.join(PROJECT_ROOT, *file_paths)
    print(
        'Updating version in version_file "{0}" with build "{1}"'
        .format(version_file, build)
    )
    replace(version_file, pattern, repl, flags=re.M)

def main(args):
    skip = args.skip
    build = args.build
    file_paths = args.file_paths

    if skip:
        print(
            'Not updating version for this build, `skip` set to "{0}"'
            .format(skip)
        )
    else:
        append_file(build, file_paths)
