# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 10:20:42 2017

@author: ASUS
"""

import os.path
try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

# In[]
from opcua import ua, uamethod, Server
server_addr = "opc.tcp://192.168.1.25:8000/freeopcua/server/"
script_dir = "Simple"

# In[]
@uamethod
def say_hello_xml(parent, happy):
    print("Calling say_hello_xml")
    if happy:
        result = "Yes, I'm happy (original XML)"
    else:
        result = "No, I'm not happy (original XML)"
    print(result)
    return result


@uamethod
def say_hello(parent, happy):
    if happy:
        result = "I'm happy (New hello)"
    else:
        result = "I'm not happy (New hello)"
    print(result)
    return result


@uamethod
def say_hello_array(parent, happy):
    if happy:
        result = "I'm happy (New Array)"
    else:
        result = "I'm not happy (New Array)"
    print(result)
    return [result, "Actually I am"]

@uamethod
def exe_calculator(parent, x1, x2):
    result = x1 * x2
    print(result)
    return result


# In[]
class HelloServer:
    def __init__(self, endpoint, name, model_filepath):
        self.server = Server()

        #  This need to be imported at the start or else it will overwrite the data
        self.server.import_xml(model_filepath)

        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)

        objects = self.server.get_objects_node()

        freeopcua_namespace = self.server.get_namespace_index("urn:freeopcua:python:server")
        hellower = objects.get_child("0:Hellower")
        hellower_say_hello = hellower.get_child("0:SayHello")
        hellower_exe_calculate = hellower.get_child("0:Calculator")

        self.server.link_method(hellower_say_hello, say_hello_xml)
        
        self.server.link_method(hellower_exe_calculate, exe_calculator)

        hellower.add_method(
            freeopcua_namespace, "SayHello2", say_hello, [ua.VariantType.Boolean], [ua.VariantType.String])

        hellower.add_method(
            freeopcua_namespace, "SayHelloArray", say_hello_array, [ua.VariantType.Boolean], [ua.VariantType.String])

    def __enter__(self):
        self.server.start()
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.stop()

# In[]
if __name__ == '__main__':
    
    with HelloServer(
            server_addr,
            "FreeOpcUa Example Server",
            os.path.join(script_dir, "simple.xml")) as server:
        embed()