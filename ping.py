import sys

import asyncio



goods = []


async def ping_ip(ip):
    try:
        process = await asyncio.create_subprocess_exec(
            'ping', '-c', '1', ip,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await process.communicate()
        if process.returncode == 0:
            print(f"IP: {ip} is reachable.")
            goods.append(ip)
        else:
            print(f"IP: {ip} is unreachable.")
    except Exception as e:
        print(f"Error pinging IP: {ip}: {e}")


async def ping_ip_range(ip_range):
    tasks = [ping_ip(ip) for ip in ip_range]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ping.py <IP address prefix>")
    else:
        ip_prefix = sys.argv[1]
        ip_range = [f"{ip_prefix}.{i}" for i in range(1, 256)]
        asyncio.run(ping_ip_range(ip_range))

        with open('goods.txt', 'w') as file:
            file.writelines([f"{ip}\n" for ip in goods])

