import asyncio
from asyncua import Client

async def enumerate_opcua_server(endpoint_url):
    """
    Enumerate OPC UA server nodes and variables
    """
    client = Client(endpoint_url)

    try:
        await client.connect()
        print(f"[+] Connected to {endpoint_url}")

        # Get server information
        server_node = client.get_node("i=2253")  # Server object
        server_array = await client.get_node("i=2254").read_value()  # Server array
        print(f"Servers: {server_array}")

        # Browse root objects
        root = client.get_root_node()
        objects = await root.get_child(["0:Objects"])

        # Recursively browse
        await browse_node(objects, depth=0, max_depth=3)

        await client.disconnect()

    except Exception as e:
        print(f"[-] Error: {e}")

async def browse_node(node, depth=0, max_depth=5):
    """
    Recursively browse OPC UA node tree
    """
    if depth > max_depth:
        return

    try:
        children = await node.get_children()
        for child in children:
            browse_name = await child.read_browse_name()
            node_class = await child.read_node_class()

            print("  " * depth + f"[{node_class.name}] {browse_name.Name}")

            # If it's a variable, read its value
            if node_class.value == 2:  # Variable
                try:
                    value = await child.read_value()
                    print("  " * depth + f"  → Value: {value}")
                except:
                    pass

            # Recurse for objects
            if node_class.value in [1, 2]:  # Object or Variable
                await browse_node(child, depth + 1, max_depth)

    except Exception as e:
        pass

# Usage
asyncio.run(enumerate_opcua_server("opc.tcp://192.168.1.100:4840"))
