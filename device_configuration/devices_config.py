from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result

nr = InitNornir(config_file="config.yaml", dry_run=True)


# TEST FUCNCTION
def hostname_config(task):
    var = task.run(task=text.template_file,
                   name="Switches hostname configuration",
                   template="hostnames.j2",
                   # current directory:
                   path="templates")
    task.host["hostname_config"] = var.result
    task.run(
    task=networking.netmiko_send_config, 
    name="Configure hostname on the device",
    config_commands=task.host["hostname_config"],
    )


# PRODUCTION FUCNCTION
def nexus_config(task):
    var = task.run(task=text.template_file,
                   name="Switches interface configuration",
                   template="nexus_config_template.j2",
                   # current directory:
                   path="templates")
    task.host["nexus_config"] = var.result
    task.run(
    networking.netmiko_send_config, 
    name="Loading Configuration on the device",
    config_commands=task.host["nexus_config"].splitlines()
    )


# TEST FUCNCTION
def send_ping(task):
    task.run(
    task=networking.netmiko_send_command, delay_factor=2, max_loops=500,
    command_string='ping 255.255.255.255',
    name="Sending Ping to the device"
    )


def main():
    print_title("Playbook to configure the network")
    task = nr.run(task=nexus_config)
    print_result(task)


if __name__ == "__main__":
    main()