import errno
import os

import jinja2


JINJA2_FILE_ENDING = '.j2'


class FatalError(Exception):
    pass


class ProjectTemplater:
    def __init__(self, config):
        # This will throw Jinja2 initialisation failures to the caller.
        self.config = config
        self.jinja_env = self._make_jinja_env(config)

    @staticmethod
    def _make_jinja_env(config):
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                config.root_dir,
                encoding=config.encoding,
                followlinks=True,
            ),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )

    def run(self):
        # Make build dir
        try:
            os.makedirs(self.config.build_dir)
        except OSError as exc:
            # Catch EEXIST and continue
            if exc.errno != errno.EEXIST:
                raise FatalError("Unable to create target directory: {}".format(os.strerror(exc.errno)))

        for template_name in self.jinja_env.list_templates():
            template = self.jinja_env.get_template(template_name)

            if template.filename is not None:
                if template.filename.endswith(JINJA2_FILE_ENDING):
                    target_name = str.replace(template.name, JINJA2_FILE_ENDING, "")
                    target_path = os.path.join(self.config.build_dir, target_name)

                    target_dir, _ = os.path.split(target_path)
                    try:
                        os.makedirs(target_dir)
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise FatalError("Unable to create target directory: {}".format(os.strerror(exc.errno)))

                    with open(target_path, 'w') as target_file:
                        target_file.write(template.render())
