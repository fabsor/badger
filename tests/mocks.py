class MockEngine:
    """
    A fake web server engine. Keeps track of things that should
    have been verified.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        """
        Reset verified sites and servers.
        """
        self.verified_sites = []
        self.verified_platforms = []

    def restart(self):
        self.restarted = True
    
    def verify_site(self, site):
        self.verified_sites.append(site)
        return True

    def verify_platform(self, platform):
        self.verified_platforms.append(platform)
        return True

