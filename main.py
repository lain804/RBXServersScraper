from RBXServersScraper import ServerScraper, Server

# steal a brainrot
EXAMPLE_PLACE_ID = 109983668079237

scraper = ServerScraper(EXAMPLE_PLACE_ID)

servers:list[Server] = scraper.get_servers()

print(f"got {len(servers)} servers!")

for server in servers:
    print(server.get_link())
