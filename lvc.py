from xml.dom import minidom
import argparse
import os

'''
TODO:   -detect node types, instead of just dodging Multiploint Connection-1
        -test with and adapter to managed and non-managed switches instead of Multipoint Connection
        -clean up how directories are handled
        -validate data in the args
'''
def sanitize_extensions(dom):
    '''
    This function removes extensions we don't need. We're going to add all of the ones we need later.
    '''
    nodes = dom.getElementsByTagName('extensions')
    for node in nodes:
        parent = node.parentNode
        parent.removeChild(node)
def replace_interface_xml_node(dom):
    '''
    This function removes the interface tag from each node and adds it back. For some reason VIRL doesn't like the
    interface node above the extensions node. Probably something about XML I don't understand.
    '''
    interface_nodes = dom.getElementsByTagName('interface')
    for node in interface_nodes:
        if node.attributes._attrs[u'name'].value not in 'Multipoint Connection-1':
            parent = node.parentNode
            parent.removeChild(node)

    nodes = dom.getElementsByTagName('node')
    for node in nodes:
        if node.attributes._attrs[u'name'].value not in 'Multipoint Connection-1':
            interface = dom.createElement('interface')
            interface.setAttribute('id', '0')
            interface.setAttribute('name', 'GigabitEthernet0/1')
            node.appendChild(interface)

def main():
    parser = argparse.ArgumentParser(description="Process configurations and integrate them into a VIRL file.")
    parser.add_argument("virl_file", help="The VIRL topology file we're looking for.", type=str)
    parser.add_argument("configs_path", help="Path to the configuration files you want to add to the VIRL file. "
                                             "The VIRL topology nodes must have the same names as the configuration "
                                             "files' filenames. Ex. /home/configs/", type=str)
    parser.add_argument("new_virl_file", help="The VIRL topology file we're creating with the configurations in it.",
                        type=str)
    args = parser.parse_args()
    virl_file = args.virl_file
    configs_path = args.configs_path
    new_virl_file = args.new_virl_file

    dom = minidom.parse(virl_file)
    print 'Reading VIRL file %s.' % (virl_file)

    sanitize_extensions(dom)
    print 'Sanitizing extensions.'

    nodes = dom.getElementsByTagName('node')
    print 'Extracting nodes from %s' % (virl_file)
    for node in nodes:
        if node.attributes._attrs[u'name'].value not in 'Multipoint Connection-1':
            node_name = node.attributes._attrs[u'name'].value
            print 'Processing node %s.' % (node_name)
            for file in os.listdir(configs_path):
                f = open(configs_path + file, 'r')
                config = f.read()
                f.close()
                if file == node_name+'.txt':
                    print 'Merging %s into %s.' % (file,new_virl_file)
                    entry_config = dom.createElement('entry')
                    entry_anetkit = dom.createElement('entry')
                    entry_config.setAttribute('key', 'config')
                    entry_anetkit.setAttribute('key', 'Auto-generate config')
                    entry_config.setAttribute('type', 'string')
                    entry_anetkit.setAttribute('type', 'Boolean')
                    extensions = dom.createElement('extensions')
                    config_text = dom.createTextNode(config)
                    anetkit_text = dom.createTextNode('false')
                    entry_config.appendChild(config_text)
                    entry_anetkit.appendChild(anetkit_text)
                    extensions.appendChild(entry_config)
                    extensions.appendChild(entry_anetkit)
                    node.appendChild(extensions)

    print 'Changing the order of the XML interface nodes in the VIRL file.'
    replace_interface_xml_node(dom)
    print 'Writing out %s.' % (new_virl_file)
    ofile = open(new_virl_file, 'w')
    dom.writexml(ofile, encoding='UTF-8')
    ofile.close()
    print 'Complete.'

if __name__ == '__main__':
    main()