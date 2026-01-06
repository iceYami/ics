def dump_all_tags(target_ip):
    """
    Dump all tag values from Logix controller
    """
    from pycomm3 import LogixDriver

    with LogixDriver(target_ip) as plc:
        tags = plc.get_tag_list()

        results = {}
        for tag in tags:
            try:
                value = plc.read(tag['tag_name'])
                results[tag['tag_name']] = value.value
            except Exception as e:
                results[tag['tag_name']] = f"Error: {e}"

        return results

# Usage: data = dump_all_tags('192.168.1.100')
