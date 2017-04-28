#!/usr/bin/env python3

import config
import templating

def main():
    # TODO: Read configuration from the file
    cfg = config.FakeConfig()

    # Fire up templater
    project_templater = templating.ProjectTemplater(cfg)
    try:
        project_templater.run()
    except templating.FatalError as exc:
        print(exc)


if __name__ == "__main__":
    main()
