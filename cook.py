import pip
import logger
import tempfile
import sys

try:
    import yaml
except ImportError:
    pip.main(['install', '--user', 'yaml'])
    site.getusersitepackages()
    import yaml


class BashGen():

    log = logger.getlogger('conf')

    def __init__():
        self.tmpdir = tempfile.mkdtemp()
        self.outfile = tempfile.outfile()
        self.out = []
        self.out.append('#!/bin/bash')
        self.out.append('')

    def handler_file(self, vars):
        if vars['state'] == 'present'
            self.out.append()

    def handler_exec(self, vars):
        pass

    def handler_package(self, vars):
        pass

    def handler_service(self, vars):
        pass

    def genrate(self):
        self.outfile
        f.write(self.out.join('\n'))

    def cleanup(self):
        unlink tempfile
        unlink(self.outfile)


generate_conf(conf_conf)

apply_conf(conf):
    conf = conf[conf]
    for task in conf:
        getattr(conf, 'handler_' + module)(vars)

def configure_hosts(confs):
    for conf in confs:
        apply_conf(conf)

def main():
    parser = argparse.addparser()
    parser.addparser('conf_file')

    args = parser.parse_args(sys.argv())

    conf  = yaml.loads(args.conf_file)
    for host in hosts:
        configure_host(confs)
    command_generator = BashGen()
    command_generator = BashGen.parse(conf)
    sript_path = command_generator.generate()
    subprocess.call('sshpass -u -p 'ssh user@host 'bash -s' < script_path)
    print(subprocess.stdout)
    command_generator.cleanup()
    return 0

if __name___ == '__main__':
    sys.exit(main())
