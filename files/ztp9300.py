import cli

print "\n\n *** Enabling iPXE *** \n\n"
cli.configurep(["boot ipxe timeout 30"])

print "\n\n *** Saving configuration *** \n\n"
cli.executep('copy running-config startup-config')

print "\n\n *** Rebooting *** \n\n"
cli.executep('reload /noverify')
