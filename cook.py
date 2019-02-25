import pip
import logging
import sys
import tempfile
import site
import subprocess
import shlex

try:
    import yaml
except ImportError:
    pip.main(['install', '--user', 'yaml'])
    site.getusersitepackages()
    import yaml


class BashGen():

    log = logging.getLogger('cook')

    def __init__(self, menu, triggers):
        with open("base-functions.sh") as f:
            self.script = f.read().splitlines()
        self.script.append("# Specific commands")
        self.triggers = triggers
        self.menu = menu

    def handler_trigger(self, trigger_name):
        trigger_conf = self.triggers[trigger_name]
        handler = "handler_{}".format(trigger_conf['module_name'])
        getattr(self, handler)(trigger_conf)



    def handler_file(self, args):
        _, temppath = tempfile.mkstemp()
        content = args['content'].split('\n')
        self.script.append("cat << EOF > {}".format(temppath))

        for line in content:
            self.script.append(line)

        self.script.append("EOF")

        command = "cook_file {} {} {}".format(args['action'], args['path'], temppath)
        self.script.append(command)
        try:
            command = "chown {} {}".format(args['owner'], args['path'])
            self.script.append(command)
        except KeyError:
            pass
        try:
            command = "chgrp {} {}".format(args['group'], args['path'])
            self.script.append(command)
        except KeyError:
            pass
        try:
            command = "chmod {} {}".format(args['mode'], args['path'])
            self.script.append(command)
        except KeyError:
            pass
        if "trigger" in args:
            self.handler_trigger(args['trigger'])
        self.script.append(command)

    def handler_exec(self, args):
        command = args['command']
        self.script.append(command)

    def handler_package(self, args):
        command = "cook_package {} {}".format(args['action'], args['package_name'])
        self.script.append(command)
        if "trigger" in args:
            self.handler_trigger(args['trigger'])

    def handler_service(self, args):
        command = "systemctl {} {}".format(args['action'], args['service_name'])
        self.script.append(command)

    def generate(self):
        for task_args in self.menu:
            handler = "handler_{}".format(task_args['module_name'])
            getattr(self, handler)(task_args)
        return '\n'.join(self.script)


class Host():
    def __init__(self, args, menus, triggers):
        self.manus = menus
        self.address =  args['address']
        self.port = args['port']
        self.username = args['username']
        self.password = args['password']
        self.triggers = triggers
        self.order = args['apply']

    def configure(self):
        for course_name in self.order:
            bash = BashGen(self.manus[course_name], self.triggers)
            print("applying configuration to host {}".format(self.address))
            command = 'sshpass -p {} ssh -p {} {}@{} bash -x -s'.format(self.password, self.port, self.username, self.address)
            command_args = shlex.split(command)
            streams = subprocess.Popen(command_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, _ = streams.communicate(bash.generate().encode('utf-8'))
            print(stdout.decode('utf-8'))

def main():

    with open('menu.yaml') as conf_file:
        conf  = yaml.load(conf_file)
    for host_conf in conf['hosts']:
        host = Host(host_conf, conf['menus'], conf['triggers'])
        host.configure()
    return 0

if __name__ == '__main__':
    sys.exit(main())
